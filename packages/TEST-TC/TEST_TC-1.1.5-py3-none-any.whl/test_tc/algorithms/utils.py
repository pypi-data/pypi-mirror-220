from __future__ import annotations

import itertools
import os
import shutil
from typing import Any, Callable, Dict, List, Tuple, Type, Union
import ast
import pandas as pd
import numpy as np
import mlflow
import json
import concurrent.futures

from ..datahandler.datahandler import DataHandler
from ..utility.check_utils import check_not_isinstance, check_not_in_iterable
from ..utility.resources import get_module_and_function, log_exception
from ..utility.tele_logger import logger
from ..analytics.evaluationMetrics import EvaluateModel


def train_val_test_split(X: pd.DataFrame, val_size : int, test_size : int) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Executes the splits on the given preprocessed Dataframe.

    Parameters
    ----------
    X : pd.DataFrame
        Preprocessed pd.DataFrame, it needs to be preprocessed by datapreparation.pred.PreprocessingClass beforehand
    val_size : int
        Number of observations based on frequecy for Validation set
    test_size : int
        Number of observations based on frequecy for Test set

    Returns
    -------
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]
        Returns three pd.DataFrames respectively, Train set, Validation set and Test set
    """
    # Parameters check
    #check_split_input(df = X, val_size = val_size, test_size = test_size)

    train_df = X.reset_index()

    test_df = train_df.groupby('unique_id').tail(test_size)
    train_df = train_df.drop(test_df.index)

    valid_df = train_df.groupby('unique_id').tail(val_size)
    train_df = train_df.drop(valid_df.index)

    test_df = test_df.set_index('unique_id')
    valid_df = valid_df.set_index('unique_id')
    train_df = train_df.set_index('unique_id')

    return train_df, valid_df, test_df

def literal_evaluation(values_list: List[str]) -> List[Any]:
    """
    The function evaluates the list values for the parameters: 'weekly_seasonality', 'yearly_seasonality'

    Parameters
    ----------
    values_lis : List[str]
        List of strings to be evaluates

    Returns
    -------
    List[Any]
        List of evaluated values
    """
    evaluated_params = []
    for val in values_list:
        try:
            val = ast.literal_eval(val)
        except:
            pass
        evaluated_params.append(val)
    return evaluated_params

def generate_values(dictionary: Dict[str, Dict[str, Union[int, float]]], default_step: Union[int, float]) -> List[Union[int, float]]:
    """
    The function generates the possible values of the numeric prophet parameters

    Parameters
    ----------
    Dictionary : Dict[str, Dict[str, Union[int, float]]]
        Dictionary format he config file with min, max and step
    Default_step, Union[int, float]
        The default step used if it's not specified in the config file

    Returns
    -------
    List[Union[int, float]]
        List of possible values

    Raises
    ------
    Exception
        If the parameter is missing a key among "min", "max" and "step"
    ValueError
        If the step is greater than the values range
    """
    
    if len(list(dictionary.keys())) == 3:
        for key in dictionary.keys():
            check_not_in_iterable(obj=key, iterable=['min', 'max', 'step'], func=get_module_and_function(),
                                attached_message="The parameter value must be of the following form: {min = <int or float>, max =<int or float>, step = [<int or float>, -1, 'None']}")
    else:
        raise Exception("The parameter value must be of the following form: {min = <int or float>, max =<int or float>, step = [<int or float>, -1, 'None']}")

    min_value = dictionary.get('min')
    max_value = dictionary.get('max')
    step = dictionary.get('step')
    if max_value <= min_value:
        raise ValueError(f'The max_value {max_value} must be greater than the min_value {min_value}')

    if step == 'None':
        step = default_step  # Use Default value as step

    check_not_isinstance(obj=min_value, data_type=(float, int), func=get_module_and_function())
    check_not_isinstance(obj=max_value, data_type=(float, int), func=get_module_and_function())
    check_not_isinstance(obj=step, data_type=(float, int), func=get_module_and_function())

    if step == -1 and min_value > 0:
        step = min_value  # Use min value as step
    elif step == -1 and min_value == 0:
        step = default_step
    elif step > (max_value - min_value):
        raise ValueError(f'The step {step} must be lower than the difference between max {max_value} and min {min_value}')

    values = list(np.arange(min_value, max_value, step))

    # Checks if max_value is already inside the grid
    if max_value not in values:
        values.append(max_value)

    return values

@log_exception(logger)
def grid_values_hyperparameters(config_hyperparameters: Dict[str, Union[List[str], Dict[str, Union[int, float]]]],
                                default_steps: Dict[str, Union[int, float]]) -> Dict[str, List[Union[str, bool, int, float]]]:
    """
    The function takes as input the dictionary of the config file
    and generates the combination of grid search parameters

    Parameters
    ----------
    config_hyperparameters: Dict[str, Union[Dict[str, Union[int, float, str]], List[str]]]
        The dictionary of hyperparameters from the config file
    default_steps: Dict[str, Union[int, float]]
        The default steps used if it's not specified in the config file

    Returns
    -------
    Dict[str, List[Union[str, bool, int, float]]]
        The grid search parameter dictionary
    """
 
    grid_parameters = {}
    for param in config_hyperparameters.keys():
        if type(config_hyperparameters[param]) == list:
            grid_parameters[param] = literal_evaluation(config_hyperparameters[param])

        elif type(config_hyperparameters[param]) == dict:
            check_not_in_iterable(obj=param, iterable=list(default_steps.keys()), func=get_module_and_function(),
                                  attached_message=f'Parameter {param} do NOT have a default setting, add it inside the config/default_steps.toml')

            grid_parameters[param] = generate_values(config_hyperparameters[param], default_step = default_steps[param])

        else:
            raise ValueError(f' The value datatype of {param} is not valid')
    return grid_parameters

def model_tuning(model: Type[Callable], evaluator: Type[EvaluateModel], unique_id: str,
                 grid_params: Dict[str, List[Union[str, bool, int, float]]], 
                 train_df: pd.DataFrame, validation_df: pd.DataFrame,
                 decision_function: str = 'rmse*0.5 + mae*0.5') -> Dict[str, Union[str, bool, int, float]]:
    """
    Performs the parameters selection on a given set of parameters grid

    Parameters
    ----------
    model : TypeType[Callable]
        Model to use in order to find its best parameters
    evaluator : Type[EvaluateModel]
        EvaluateModel class to use for the evaluations
    grid_params : Dict[str, List[Union[str, bool, int, float]]]
        The parameters grid space
    unique_id : str
        Hierarchys ID to be evaluated 
    train_df : pd.DataFrame
        The dataframe on which the model fit is applied 
    validation_df : pd.DataFrame
        The dataframe on which the model evaluation is applied
    decision_function : str, optional
        Decision function to minimize in order to find the best parameters, by default 'rmse*0.5 + mape*0.5'

        The Decision function can use ONLY the evaluation parameters, beware that if an evaluation parameter
        has a space " " in its name, inside the evaluation it MUST be written as a "_", for example if using
        Percentage Coverage instead of the rmse inside the default function, this becomes 'percentage_coverage*0.5 + mape*0.5'

    Returns
    -------
    Dict[str, Union[str, bool, int, float]]
        Dictionary of the best parameters

    Raises
    ------
    ValueError
        If the validation set is empty, after cleaning
    """  

    ######## FUNCTION TO PARALLELIZE ######## 
    def evaluate_params(params: Dict[str, Union[str, bool, int, float]], decision_func: str) -> float:
        """
        Evaluates the given parameter set.

        Parameters
        ----------
        params : Dict[str, Union[str, bool, int, float]]
            Dictionary of parameter values
        decision_function : str
            Decision function to minimize in order to find the best parameters

        Returns
        -------
        float
            Result of the evaluation
        """        

        m =  model(**params)
        m.fit(train_df)

        validation_df_clean = validation_df.dropna()
        if len(validation_df_clean) > 0:
            pred = m.predict(validation_df_clean)
            evals = evaluator.make_evaluation(df_real=validation_df_clean, df_pred=pred, id_pred=unique_id, verbose=False)

            for k in evals.drop(columns='Id_Pred').to_dict().keys():
                exec(f"{k.lower().replace(' ', '_')} = {evals[k][0]}")

            return {eval(decision_function.lower()): params}
        else:
            raise ValueError("After NaNs removal, Validation set is empty.")


    get_minimum = {}
    keys, values = zip(*grid_params.items())

    permutations_dicts = []
    for v in itertools.product(*values):
        if not isinstance(v, list):
            v = list(v)
        
        permutations_dicts.append(dict(zip(keys, v)))

    # Use ThreadPoolExecutor for parallel execution
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Map evaluate_params function to each parameter set in parallel
        results = executor.map(lambda params: evaluate_params(params, decision_function), permutations_dicts)
        # Collect the results

        for res in results:
            get_minimum.update(res)

    # Find the best parameters
    minimum_error = np.min(list(get_minimum.keys()))
    best_params = get_minimum[minimum_error]

    return best_params

def create_zero_dataframe(columns: List[str], n_rows: int) -> pd.DataFrame:
    """Creates a dataframe with the given columns and rows full of zeros.

    Parameters
    ----------
    columns : List[str]
        Column names
    n_rows : int
        Number of rows

    Returns
    -------
    pd.DataFrame
        dataframe
    """
    # Create a dictionary with the column names and values
    data = {col: np.zeros(n_rows).astype(int) for col in columns}

    # Create the dataframe
    df = pd.DataFrame(data)

    return df


def mlflow_log_artifact(predict_real_folder: str, experiment_name: str, 
                        df_to_save: List[Tuple[pd.DataFrame, str]] =None,
                        json_to_save: List[Tuple[Dict[str, List[str]], str]] =None):
    """The function logs, if provided, the dataframes and the jsons on MLFlow

    Parameters
    ----------
    predict_real_folder : str
        The local folder to temporary save the data
    experiment_name : str
        The name of the experiment
    df_to_save : List[Tuple[pd.DataFrame, str]], optional
        The list of tuples (dataframes, filename) to save , by default None
    json_to_save : List[Tuple[Dict[str, List[str]], str]], optional
        The list of tuples (dict, filename) to save, by default None
    """
        
    logger.info('START logging results.', important=True)

    save_data_folder = os.path.join(predict_real_folder, experiment_name)

    # If there are dataframes to save, apply the function
    if isinstance(df_to_save, list):
        format_ = '.parquet'
        df_to_save = [(D, N+format_) for D, N in df_to_save]

        write_dataframes_locally(to_save=df_to_save, save_data_folder=save_data_folder)

        for _, filename in df_to_save:
            mlflow.log_artifact(os.path.join(save_data_folder, filename), artifact_path="dataframes")

    # If there are dictionaries to save, apply the function
    if isinstance(json_to_save, list):
        format_ = '.json'
        json_to_save = [(D, N+format_) for D, N in json_to_save]

        write_json_locally(to_save=json_to_save, save_data_folder=save_data_folder)
        
        for _, filename in json_to_save:
            mlflow.log_artifact(os.path.join(save_data_folder, filename), artifact_path='dataframes')

    # If dataframes or dictionaries have been saved, apply the function
    if isinstance(df_to_save, list) or isinstance(json_to_save, list):
        remove_folder_locally(save_data_folder)

    logger.info('DONE logging results.', important=True)


def write_dataframes_locally(to_save: List[Tuple[pd.DataFrame, str]], save_data_folder: str):
    """Writes locally the dataframes needed by MLFlow in order to log them in its application.

    Parameters
    ----------
    to_save : List[Tuple[pd.DataFrame, str]]
        List of Tuples with pandas DataFrames and corresponding filenames that will be written
    save_data_folder : str
        Data folder where files will be written
    """
    os.makedirs(save_data_folder, exist_ok=True)
    DH = DataHandler(data_folder = save_data_folder)
    for D, N in to_save:
        DH.write(D, filename = N, folder = '')

def write_json_locally(to_save: List[Tuple[Dict[str, List[str]], str]], save_data_folder: str):
    """Writes locally the jsons needed by MLFlow in order to log them in its application.

    Parameters
    ----------
    to_save : List[Tuple[Dict[str, List[str]], str]]
        List of Tuples with Dictionaries and corresponding filenames that will be written
    save_data_folder : str
        Data folder where files will be written
    """
    os.makedirs(save_data_folder, exist_ok=True)
    for J, N in to_save:
        json_file = os.path.join(save_data_folder, N)
        tmp = {k: list(v) for k,v in J.items()}
        with open(json_file, 'w') as f:
            json.dump(tmp, f)


def remove_folder_locally(folder_to_remove: str):
    """Deletes the folder once the files are logged on MLFlow.

    Parameters
    ----------
    folder_to_remove : str
        Folder to be removed
    """
    shutil.rmtree(folder_to_remove)

def prepare_dataframe_to_hf(X_true: pd.DataFrame, X_pred: pd.DataFrame, model_name: str) -> pd.DataFrame:
    """Prepare the predicted Dataframe from a model from algorithms.models to be reconciled by one
    of HierarchicalForecast reconcilers.

    Parameters
    ----------
    X_true : pd,DataFrame
        Pandas Dataframe containing the true data
    X_pred : pd.DataFrame
        Pandas Dataframe containing the predictions of a model from algorithms.models
    model_name : str
        Name of the model applied to the X_pred

    Returns
    -------
    pd.DataFrame
        Pandas Dataframe ready to be give to a HierarchicalForecast reconciler
    """
    check_not_in_iterable(obj='Timestamp', iterable=X_pred.columns, func=get_module_and_function())
    check_not_in_iterable(obj='Pred_Mean', iterable=X_pred.columns, func=get_module_and_function())
    check_not_in_iterable(obj='Id_Pred', iterable=X_pred.columns, func=get_module_and_function())

    hier_pred = X_pred.rename(columns = {
        'Timestamp' : 'ds', 'Pred_Mean' : model_name.title(), 'Id_Pred': 'unique_id'
    })

    hier_pred = hier_pred.set_index('unique_id')
    for col in hier_pred.columns:
        if col not in ['ds', model_name.title()]:
            hier_pred = hier_pred.drop(col, axis = 1)
    
    hier_pred['y'] = list(X_true['y'])

    return hier_pred
