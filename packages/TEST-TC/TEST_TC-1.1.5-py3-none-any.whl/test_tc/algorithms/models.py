from typing import Dict, List, Callable, Tuple, Union
from typing_extensions import Self
import pandas as pd
from prophet import Prophet
import numpy as np

from hierarchicalforecast.core import HierarchicalReconciliation
from hierarchicalforecast.methods import BottomUp, MinTrace, TopDown

from .utils import model_tuning, create_zero_dataframe, grid_values_hyperparameters
from ..analytics.evaluationMetrics import EvaluateModel
from ..utility.tele_logger import logger
from ..utility.resources import log_exception, get_module_and_function, get_configuration
from ..utility.check_utils import check_not_in_iterable, check_not_isinstance


class ProphetModel():
    def __init__(self, params: Dict[str, Union[Dict[str, Union[int, float, str]], List[str]]], config_path: str, max_na_ratio: float = 0.5):
        """
        Initlization parameters for ProphetModel.

        Parameters
        ----------
        dic_param : Dict[str, Union[Dict[str, Union[int, float, str]], List[str]]]      
            The dictionary of hyperparameters from the config file
        max_na_ratio : float
            Maximum ratio of NaNs and not null permitted in order to fit the model
        """

        self.config_path = config_path
        self.max_na_ratio = max_na_ratio
        params.update({'interval_width':['0.95']}) # Update params with the 95% CI since default is 80%

        self.make_grid_params(params)


    def fit(self, X_train: pd.DataFrame, X_val: pd.DataFrame) -> Self:
        """Fits the models using a Train and Validations Set setting in the call arguments the 
        Dictionary of Best Parameters and Dictionary of Fitted models which used the respective Best Params.

        Parameters
        ----------
        X_train : pd.DataFrame
            Train Set to use for the model
        X_val : pd.DataFrame
            Validation Set to use for the model
        """
        logger.info(f"START Fitting Model.", important=True)

        count = 0
        total_runs = X_train.index.nunique()

        self.models_dict = {}
        self.models_best_params = {}

        for id_pred, df_train in X_train.groupby('unique_id'):
            self.models_dict[id_pred] = None
            self.models_best_params[id_pred] = {}

            logger.info(f"Training {id_pred}")

            if (df_train['y'] > 0).sum() / len(df_train) < self.max_na_ratio:
                logger.info(f"The train set for time series {id_pred} has more than {self.max_na_ratio*100}% null values, skipping it.")
                count += 1
                logger.info(f"Remaining number of iteration - {total_runs-count}")
                continue
            try:
                evaluator = EvaluateModel(date_true='ds', date_pred='ds', y_true='y', y_pred='yhat', upper_95='yhat_upper', lower_95='yhat_lower')
                # Tune if we have a non-empty validation set
                df_val = X_val[X_val.index==id_pred]
                
                # Find best params
                logger.info("Grid Searching Best Parameters.")
                best_params = model_tuning(model=Prophet, evaluator=evaluator, unique_id=id_pred, grid_params=self.grid_params, 
                                           train_df=df_train, validation_df=df_val,
                                           decision_function = 'rmse*0.5 + mape*0.5')

                logger.info(f"Best Parameters found: {best_params}")

                model = Prophet(**best_params)
                
                # Retrain on train and val data with best parameters
                logger.info(f"Fitting Prophet model using the Best Parameters")
                model.fit(pd.concat([df_train, df_val]))

                self.models_best_params[id_pred] = best_params
                self.models_dict[id_pred] = model
                
            except ValueError as e:
                logger.info(f"Skipping training {id_pred}, due to: {e}")
                count += 1
                logger.info(f"Remaining number of iteration - {total_runs-count}")
                continue

            count += 1
            logger.info(f"Remaining number of iteration - {total_runs-count}")
        
        logger.info(f"DONE Fitting Model.", important=True)

        # Check consinstency of models_dict
        count = 0
        breaker = len(self.models_dict.keys())
        for m in self.models_dict.values():
            if m != None:
                break
            else:
                count+=1

        if count == breaker:
            raise Exception('No models have been trained, check logs for insights on the reasoning.')

        return self


    def refit(self, X: pd.DataFrame) -> Self:
        """_summary_

        Parameters
        ----------
        X : pd.DataFrame
            _description_

        Returns
        -------
        Self
            _description_
        """

        logger.info(f"START Re-Fitting Model.", important=True)
        total_runs = X.index.nunique()

        count = 0
        for id_pred, df in X.groupby('unique_id'):
            logger.info(f"Training {id_pred}")

            # If the models exists and have been trained, execute the retrain on the whole dataset
            if isinstance(self.models_dict[id_pred], ProphetModel):
                model = Prophet(**self.models_best_params[id_pred])
                # Retrain on train and val data with best parameters
                model.fit(df)

                self.models_dict[id_pred] = model

            count += 1
            logger.info(f"Remaining number of iteration - {total_runs-count}")

        logger.info(f"DONE Re-Fitting Model.", important=True)
    

    def predict(self, X: pd.DataFrame) -> pd.DataFrame:
        """Makes predictions over an input Dataframe using the fitted Models

        Parameters
        ----------
        X : pd.DataFrame
            The Dataframe to use in order to predict

        Returns
        -------
        pd.DataFrame
            Pandas Dataframe with the predictions for every hierarchy
        """
        logger.info(f"START Predicting Model.", important=True)

        predictions = []
        pred_cols_template = ["Timestamp","Id_Pred","Pred_Mean","Sigma","Pi_Lower_95","Pi_Upper_95"]

        for id_pred, df in X.groupby('unique_id'):

            model = self.models_dict[id_pred]
            if model is None:
                logger.info(f"Skipping prediction for {id_pred}, as the model has not been trained")
                df_output = create_zero_dataframe(pred_cols_template, len(df))
                df_output['Id_Pred'] = id_pred
                df_output['Timestamp'] = list(df['ds'])

            else:
                try:
                    df_test_pred = model.predict(df)
                    df_output = self.prepare_output(predictions=df_test_pred, id_pred=id_pred)

                except ValueError as e:
                    logger.info(f"Skipping prediction for {id_pred}, due to: {e}")
                    df_output = create_zero_dataframe(pred_cols_template, len(df))
                    df_output['Id_Pred'] = id_pred
                    df_output['Timestamp'] = list(df['ds'])
                    
            # Appending predictions in the predictions list
            predictions.append(df_output)

        output = pd.concat(predictions).reset_index(drop=True)
        
        logger.info(f"DONE Predicting Model.", important=True)

        return output


    def score(self, X_true: pd.DataFrame, X_pred: pd.DataFrame) -> pd.DataFrame:
        """_summary_

        Parameters
        ----------
        X_true : pd.DataFrame
            _description_
        X_pred : pd.DataFrame
            _description_

        Returns
        -------
        pd.DataFrame
            _description_
        """

        evaluator = EvaluateModel(date_true='ds', date_pred='Timestamp', y_true='y', y_pred='Pred_Mean', upper_95='Pi_Upper_95', lower_95='Pi_Lower_95')
        evaluations = []
        
        for unique_id in X_pred['Id_Pred'].unique():
            df_real = X_true[X_true.index == unique_id]
            df_pred = X_pred[X_pred['Id_Pred'] == unique_id]

            if df_pred.Pred_Mean.sum() > 0:
                evaluations.append(evaluator.make_evaluation(df_real=df_real, df_pred=df_pred, id_pred=unique_id))
        
        return pd.concat(evaluations)
        

    def prepare_output(self, predictions: pd.DataFrame, id_pred: str) -> pd.DataFrame:
        """Prepares the output Dataframe with the requested format of:
            -'Timestamp' as Timestamp
            - 'Id_Pred' as Hierarchy
            - 'Pred_Mean' as Predicted Value
            - 'Sigma' as Standard Deviation of the Predicted Value
            - 'Pi_Lower_95' as 0.95 Percentile of the Predicted Value
            - 'Pi_Upper_95' as 0.5 Percentile of the Predicted Value

        Parameters
        ----------
        predictions : pd.DataFrame
            Dataframe containing the predictions
        id_pred : str
            String corresponding to the Hierarchy

        Returns
        -------
        pd.DataFrame
            Pandas DataFrame with the requested format
        """

        preproc_df = predictions[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
        preproc_df.columns = ['Timestamp', 'Pred_Mean', 'Pi_Lower_95', 'Pi_Upper_95']

        preproc_df['Id_Pred'] = id_pred

        # Evaluate Standard Deviation from .95 Percentiles using normality rule
        preproc_df['Sigma'] = (preproc_df['Pi_Upper_95'] - preproc_df['Pi_Lower_95']) / (2 * 1.96) 
        # Round the float values and set tham as integers
        preproc_df[['Pred_Mean', 'Sigma', 'Pi_Lower_95', 'Pi_Upper_95']] = preproc_df[['Pred_Mean', 'Sigma', 'Pi_Lower_95', 'Pi_Upper_95']].round().astype(int)
        
        return preproc_df[['Timestamp', 'Id_Pred', 'Pred_Mean', 'Sigma', 'Pi_Lower_95', 'Pi_Upper_95']]
    

    def make_grid_params(self, params: Dict[str, Union[Dict[str, Union[int, float, str]], List[str]]]):
        """The function takes as input the dictionary of the config file 
        and executes the grid_values_hyperparameters which generates the 
        combination of grid search parameters.

        Parameters
        ----------
        params : Dict[str, Union[Dict[str, Union[int, float, str]], List[str]]]
            The dictionary of hyperparameters from the config file
        """

        # LOAD DEFAULT STEPS  
        ############################################
        config_path = self.config_path
        default_steps_config = "default_steps.toml"
        default_steps = get_configuration('prophet', config_path, default_steps_config)
        ############################################

        self.grid_params = grid_values_hyperparameters(params, default_steps)



@log_exception(logger)
class HierarchicalReconcileModel():
    def __init__(self, model_name: str, S: pd.DataFrame, tags: Dict[str, List[str]], reconciler: List =None, max_na_ratio: float =0.5):
        """_summary_

        Parameters
        ----------
        model_name : str
            _description_
        S : pd.DataFrame
            _description_
        tags : Dict[str, List[str]]
            _description_
        reconciler : List, optional
            _description_, by default None
        """

        self.model_name = model_name
        self.S          = S
        self.tags       = tags

        self.max_na_ratio = max_na_ratio

        if reconciler == None:
            self.reconciler = [BottomUp(),
                        TopDown(method= 'average_proportions'),TopDown(method= 'proportion_averages')]
                    # MinTrace(method='mint_shrink'),MinTrace(method='ols')
        else:
            if isinstance(reconciler, str):
                self.reconciler = [eval(reconciler)]
            elif isinstance(reconciler, list):
                self.reconciler = reconciler
            else:
                self.reconciler = [reconciler]
    

    def fit(self, X_true: pd.DataFrame, X_pred: pd.DataFrame, X_future_pred: pd.DataFrame) -> Self:
        """_summary_

        Parameters
        ----------
        X_true : pd.DataFrame
            _description_
        X_pred : pd.DataFrame
            _description_
        X_future_pred : pd.DataFrame
            _description_

        Returns
        -------
        Self
            _description_
        """
        logger.info('Fitting Reconciliation Model.')
        self.hrec = HierarchicalReconciliation(reconcilers=self.reconciler)

        self.X     = self.prepare_dataframe_to_hf(X_pred=X_pred, model_name=self.model_name, X_true=X_true).fillna(0)
        self.X_hat = self.prepare_dataframe_to_hf(X_pred=X_future_pred, model_name=self.model_name).fillna(0)

        return self


    def predict(self, level: List =[95], as_output: bool =False) -> pd.DataFrame:
        """_summary_

        Parameters
        ----------
        level : List
            _description_
        as_output : bool
            _description_

        Returns
        -------
        pd.DataFrame
            _description_
        """
        logger.info('Predicting Reconciliation Model.')
        Y_rec = self.hrec.reconcile(Y_hat_df=self.X_hat, Y_df=self.X, S=self.S, tags=self.tags, 
                        level=level, intervals_method='bootstrap')
        
        if as_output:
            output = self.prepare_output(Y_rec=Y_rec)

            cols = output.select_dtypes(include=np.number).columns
            output[cols] = output[cols].clip(0)
            return output

        return Y_rec


    def fit_predict(self, X_true: pd.DataFrame, X_pred: pd.DataFrame, X_future_pred: pd.DataFrame, level: List =[95], as_output: bool =False) -> pd.DataFrame:
        """_summary_

        Parameters
        ----------
        X_true : pd.DataFrame
            _description_
        X_pred : pd.DataFrame
            _description_
        X_future_pred : pd.DataFrame
            _description_
        level : List, optional
            _description_, by default [95]
        as_output : bool
            _description_

        Returns
        -------
        pd.DataFrame
            _description_
        """

        Y_rec = self.fit(X_true=X_true, X_pred=X_pred, X_future_pred=X_future_pred).predict(level=level, as_output=as_output)
        
        return Y_rec
    

    def score(self, X_true: pd.DataFrame, X_pred: pd.DataFrame, check_model_pred: pd.DataFrame,
               hierarchical_output: bool =True, full_scoring: bool =True) -> Tuple[pd.Series, Union[pd.DataFrame, None]]:
        """_summary_

        Parameters
        ----------
        X_true : pd.DataFrame
            _description_
        X_pred : pd.DataFrame
            _description_
        check_model_pred : pd.DataFrame
            _description_
        hierarchical_output : bool, optional
            _description_, by default True
        full_scoring : bool, optional
            _description_, by default True

        Returns
        -------
        Tuple[pd.Series, Union[pd.DataFrame, None]]
            _description_
        """
        logger.info('Evaluating Reconciliation Model.')

        # Set the columns
        if hierarchical_output:
            date_pred = 'ds'
            col   = [c for c in X_pred.columns if c != 'ds' and '-hi-' not in c[-7:] and 'lo-' not in c[-7:] and '/' in c][0]
            upper = [c for c in X_pred.columns if c != 'ds' and '-hi-' in c[-7:]][0]
            lower = [c for c in X_pred.columns if c != 'ds' and '-lo-' in c[-7:]][0]
        else:
            date_pred = 'Timestamp'
            col   = 'Pred_Mean'
            upper = 'Pi_Upper_95'
            lower = 'Pi_Lower_95'
        
        # Instantiate the correct EvaluateModel
        evaluator = EvaluateModel(date_true='ds', date_pred=date_pred, y_true='y', y_pred=col, upper_95=upper, lower_95=lower)

        evals = []
        for unique_id in X_pred.index.unique(): # Iterate over Id_Preds
            df_real  = X_true[X_true.index == unique_id]
            df_pred  = X_pred[X_pred.index == unique_id]
            df_check = check_model_pred[check_model_pred.index == unique_id]

            # Evaluate if every prediction is 0 or hierarchies with more than 50% nulls, that would only insert bias in the evaluation
            if df_check['Pred_Mean'].sum() > 0:
                evals.append(evaluator.make_evaluation(df_real=df_real, df_pred=df_pred, id_pred=unique_id, verbose=False))
        
        scores = pd.concat(evals)

        scores_aggr = scores.drop(columns='Id_Pred')
        scores_aggr = scores_aggr.mean()
        scores_aggr.name = 'Metrics Reconciled'

        if full_scoring:
            return scores_aggr, scores
        else:
            return scores_aggr, None


    def best_reconciler(self, X_true: pd.DataFrame, X_pred: pd.DataFrame, X_future_true: pd.DataFrame, X_future_pred: pd.DataFrame,
                        level: List =[95], decision_function: str = 'rmse*0.5 + mae*0.5') -> Callable:
        """_summary_

        Parameters
        ----------
        X_true : pd.DataFrame
            _description_
        X_pred : pd.DataFrame
            _description_
        X_future_true : pd.DataFrame
            _description_
        X_future_pred : pd.DataFrame
            _description_
        level : List, optional
            _description_, by default [95]
        decision_function : str, optional
            _description_, by default 'rmse*0.5 + mae*0.5'

        Returns
        -------
        Callable
            _description_
        """
        
        logger.info('START Finding Best Reconciliation Method.')

        Y_rec = self.fit_predict(X_true=X_true, X_pred=X_pred, X_future_pred=X_future_pred, level=level)
        
        # Get reconcilers columns
        reconciler_cols = {}
        for rec in self.reconciler:
            try:
                reconciler_cols.update({rec: [c for c in Y_rec.columns if rec.__class__.__name__ in c and rec.method in c]+['ds']})
            except AttributeError:
                reconciler_cols.update({rec: [c for c in Y_rec.columns if rec.__class__.__name__ in c]+['ds']})
                continue
        
        get_minimum = {}
        for rec in reconciler_cols: # Iterate over the reconciler methods
            # Select only the corresponding reconciling columns
            preds = Y_rec[reconciler_cols[rec]] 

            # Concatenate the evaluations, drop the Id_Pred columns and evaluate the mean
            metrics, _ = self.score(X_true=X_future_true, X_pred=preds,
                                    check_model_pred=X_future_pred.set_index('Id_Pred'), full_scoring = False)

            # Set every metric as a variable
            for k in metrics.to_dict().keys():
                exec(f"{k.lower().replace(' ', '_')} = {metrics[k]}")
            
            # Update the dictionary with {score: reconciliation_method}
            get_minimum[eval(decision_function.lower())] = rec
        
        # Last run for the Original Predicted model
        metrics, _ = self.score(X_true=X_true, X_pred=X_pred.set_index('Id_Pred'),
                                check_model_pred=X_pred.set_index('Id_Pred'), hierarchical_output=False, full_scoring = False)
        # Set every metric as a variable
        for k in metrics.to_dict().keys():
            exec(f"{k.lower().replace(' ', '_')} = {metrics[k]}")
        # Update the dictionary with {score: reconciliation_method}
        get_minimum[eval(decision_function.lower())] = self.model_name.lower()

        # Check if the best reconciler is the base one
        # If that's the case, log a warning and calculate the second best reconciler
        minimum_error = np.min(list(get_minimum.keys()))
        if get_minimum[minimum_error] == self.model_name.lower():
            logger.warning('None of the reconcilers is better than the base model. Returns the second best reconciler')
            del get_minimum[minimum_error]

            minimum_error = np.min(list(get_minimum.keys()))
            best_reconciler = get_minimum[minimum_error]
        # If that's not the case, return the proper index of the reconciler by removing the model_name
        else:
            best_reconciler = get_minimum[minimum_error]
        
        logger.info('DONE Finding Best Reconciliation Method.')
        
        return best_reconciler
    

    def prepare_output(self, Y_rec: pd.DataFrame) -> pd.DataFrame:
        """Prepares the output Dataframe with the requested format of:
            -'Timestamp' as Timestamp
            - 'Id_Pred' as Hierarchy
            - 'Pred_Mean' as Predicted Value
            - 'Sigma' as Standard Deviation of the Predicted Value
            - 'Pi_Lower_95' as 0.95 Percentile of the Predicted Value
            - 'Pi_Upper_95' as 0.5 Percentile of the Predicted Value

        Parameters
        ----------
        Y_rec : pd.DataFrame
            Dataframe containing the predictions

        Returns
        -------
        pd.DataFrame
            Pandas DataFrame with the requested format
        """
        Y_rec = Y_rec.drop(columns=self.model_name.title())

        col   = [c for c in Y_rec.columns if c != 'ds' and '-hi-' not in c[-7:] and 'lo-' not in c[-7:]][0]
        upper = [c for c in Y_rec.columns if c != 'ds' and '-hi-' in c[-7:]][0]
        lower = [c for c in Y_rec.columns if c != 'ds' and '-lo-' in c[-7:]][0]

        preproc_df = Y_rec.reset_index()[['ds', 'unique_id', col, lower, upper]].copy()
        preproc_df.columns = ['Timestamp', 'Id_Pred', 'Pred_Mean', 'Pi_Lower_95', 'Pi_Upper_95']

        # Evaluate Standard Deviation from .95 Percentiles using normality rule
        preproc_df['Sigma'] = (preproc_df['Pi_Upper_95'] - preproc_df['Pi_Lower_95']) / (2 * 1.96) 
        # Round the float values and set tham as integers
        preproc_df[['Pred_Mean', 'Sigma', 'Pi_Lower_95', 'Pi_Upper_95']] = preproc_df[['Pred_Mean', 'Sigma', 'Pi_Lower_95', 'Pi_Upper_95']].round().astype(int)
        
        return preproc_df[['Timestamp', 'Id_Pred', 'Pred_Mean', 'Sigma', 'Pi_Lower_95', 'Pi_Upper_95']]
    

    def prepare_dataframe_to_hf(self, X_pred: pd.DataFrame, model_name: str, X_true: pd.DataFrame =None) -> pd.DataFrame:
        """Prepare the predicted Dataframe from a model from algorithms.models to be reconciled by one
        of HierarchicalForecast reconcilers.

        Parameters
        ----------
        X_pred : pd.DataFrame
            Pandas Dataframe containing the predictions of a model from algorithms.models
        model_name : str
            Name of the model applied to the X_pred
        X_true : pd.DataFrame, optional
            Pandas Dataframe containing the true data, by default None

        Returns
        -------
        pd.DataFrame
            Pandas Dataframe ready to be give to a HierarchicalForecast reconciler
        """
        
        check_not_isinstance(obj=X_pred, data_type=pd.DataFrame, func=get_module_and_function())
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
        
        if type(X_true) != type(None):
            check_not_isinstance(obj=X_true, data_type=pd.DataFrame, func=get_module_and_function())
            hier_pred['y'] = list(X_true['y'])
            
        return hier_pred
