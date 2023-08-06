from typing import Any, Callable, Dict, Type, Union, List
from typing_extensions import Self
import pandas as pd
import logging

from .models import ProphetModel
from ..utility.check_utils import check_not_isinstance, check_not_in_iterable
from ..utility.resources import get_module_and_function, log_exception
from ..utility.tele_logger import logger

@log_exception(logger)
class ExperimentClass():
    def __init__(self,  model: str, params : Dict[str, Union[Dict[str, Union[int, float, str]], List[str]]] , config_path : str):
        """ Pass all the parameters that can be set as explicit keyword
        arguments.
        
        Parameters
        ----------
        model : str
            Parameter identifying model to use
        params : Dict[str, Union[Dict[str, Union[int, float, str]], List[str]]]         
            Dictionary representing the model parameters
        config_path : str
            Path in which resides the configuration files 
            
        """
        self.model_name = model.lower()
        self.config_path = config_path

        if self.model_name == 'prophet':
            log_del = logging.getLogger('cmdstanpy')
            log_del.addHandler(logging.NullHandler())
            log_del.propagate = False
            log_del.setLevel(logging.CRITICAL)

            self.Model = ProphetModel(params=params, config_path=self.config_path)
        else:
            raise Exception()


    def check_consistency(self, X: pd.DataFrame):
        """_summary_

        Parameters
        ----------
        X : pd.DataFrame
            _description_
        """

        check_not_isinstance(obj=X, data_type=pd.DataFrame, func=get_module_and_function())
        check_not_in_iterable(obj='unique_id', iterable=X.reset_index().columns, func=get_module_and_function())
        check_not_in_iterable(obj='ds', iterable=X.columns, func=get_module_and_function())
        check_not_in_iterable(obj='y', iterable=X.columns, func=get_module_and_function())

    def fit(self, X_train: pd.DataFrame, X_val: pd.DataFrame, y=None) -> Self:
        """_summary_

        Parameters
        ----------
        X_train : pd.DataFrame
            _description_
        X_val : pd.DataFrame
            _description_
        y : _type_, optional
            _description_, by default None

        """

        for x in [X_train,X_val]:
            self.check_consistency(X=x)
        
        self.Model.fit(X_train=X_train, X_val=X_val)

    
    def refit(self, X: pd.DataFrame):
        """_summary_

        Parameters
        ----------
        X : pd.DataFrame
            _description_

        Returns
        -------
        _type_
            _description_
        """
        
        self.check_consistency(X=X)

        self.Model.refit(X=X)
       

    def predict(self, X: pd.DataFrame, y=None) -> pd.DataFrame:
        """_summary_

        Parameters
        ----------
        X : pd.DataFrame
            _description_
        y : _type_, optional
            _description_, by default None

        Returns
        -------
        pd.DataFrame
            _description_
        """

        self.check_consistency(X=X)

        output = self.Model.predict(X=X)

        return output

    def fit_predict(self, X_train: pd.DataFrame,  X_val: pd.DataFrame, X_test: pd.DataFrame) -> pd.DataFrame:
        """_summary_

        Parameters
        ----------
        X_train : pd.DataFrame
            _description_
        X_val : pd.DataFrame
            _description_
        X_test : pd.DataFrame
            _description_

        Returns
        -------
        pd.DataFrame
            _description_
        """

        for x in [X_train, X_val, X_test]:
            self.check_consistency(X=x)
        
        output = self.Model.fit(X_train=X_train, X_val=X_val).predict(X=X_test)

        return output
    
    def create_hyperparameters_table(self, hyperparameters: dict[str, Any]) -> dict[str, Any]:
        """_summary_

        Parameters
        ----------
        hyperparameters : dict[str, Any]
            _description_

        Returns
        -------
        dict[str, Any]
            _description_
        """
        def get_params_to_log(model: Type[Callable], hyperparameters: list[str]) -> dict[str, Any]:
            """_summary_

            Parameters
            ----------
            model : Type[Callable]
                _description_
            hyperparameters : list[str]
                _description_

            Returns
            -------
            dict[str, Any]
                _description_
            """
            return {hyper: getattr(model, hyper) for hyper in hyperparameters}

        return {id_pred.replace('/', '_') : get_params_to_log(model=model, hyperparameters=list(hyperparameters.keys())) if model else None 
                for id_pred, model in self.Model.models_dict.items()}

    def score(self, X_true: pd.DataFrame, X_pred: pd.DataFrame, y=None, full_scoring=True) -> pd.DataFrame:
        """_summary_

        Parameters
        ----------
        X_true : pd.DataFrame
            _description_
        X_pred : pd.DataFrame
            _description_
        y : _type_, optional
            _description_, by default None
        full_scoring : bool, optional
            _description_, by default True

        Returns
        -------
        pd.DataFrame
            _description_
        """
        self.check_consistency(X=X_true)
        check_not_in_iterable(obj='Id_Pred', iterable=X_pred.columns, func=get_module_and_function())
        check_not_in_iterable(obj='Pred_Mean', iterable=X_pred.columns, func=get_module_and_function())
        check_not_in_iterable(obj='Pi_Upper_95', iterable=X_pred.columns, func=get_module_and_function())
        check_not_in_iterable(obj='Pi_Lower_95', iterable=X_pred.columns, func=get_module_and_function())

        logger.info(f"START Evaluating Model.", important=True)
        scores = self.Model.score(X_true=X_true, X_pred=X_pred)

        scores_aggr = scores.drop(columns='Id_Pred')
        scores_aggr = scores_aggr.mean()
        scores_aggr.name = 'Metrics'

        logger.info(f"DONE Evaluating Model.", important=True)

        if full_scoring:
            return scores_aggr, scores
        else:
            return scores_aggr, None
