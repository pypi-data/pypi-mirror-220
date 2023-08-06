from sklearn.base import BaseEstimator, TransformerMixin
from typing_extensions import Self, Any
import pandas as pd
import pickle

from ..utility.tele_logger import logger
from ..utility.resources import log_exception
from ..datapreparation.utils import map_columns, generate_time_series, missing_data_imputation, filter_target_col


class PreprocessingClass(BaseEstimator, TransformerMixin):

    def __init__(self, usecase: str, model: str):
        """ Pass all the parameters that can be set as explicit keyword
        arguments.
        
        Parameters
        ----------
        usecase : str
            Parameter identifying usecase into account
        model : str
            Parameter identifying model to use
            
        """
        self.usecase = usecase.lower()
        self.model  = model.lower()
        # LOGGING INFO -- Instanciate the Preprocessing class
        logger.info(msg = f'Instantiated the Preprocessing class for usecase: {self.usecase} and model: {self.model}.')
    
    
    @log_exception(logger)
    def fit(self, X: pd.DataFrame, params: dict, y: Any = None) -> Self:
        """Learn parameters useful for transforming data.

        Parameters
        ----------
        X : pd.DataFrame
            The input DataFrame.
        parmas: dict 
            specifies prameters to initialize preprocessing
        y : None
            Ignored (only for compatibility).
        """

        for key, value in params.items():
            setattr(self, key, value)
      
        return self

    @log_exception(logger)
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Preparing Data to feed models"

        Must be called only after calling fit method.
        Parameters
        ----------
        X : pd.DataFrame
            The input DataFrame
            
        Returns
        -------
        pd.DataFrame 
            DataFrame identifying the timeseries 
        """
        logger.info(f'START Preprocessing.', important=True)
        X = map_columns(hierarchy = self.hierarchy, df = X, conversion = self.conversion)
        
        if self.usecase == "teleconsulto":
            X = filter_target_col(df = X, target_col = self.target_col)
            if self.model == "prophet":  
                # LOGGING INFO -- Creating the dataframe suitable for time series analysis
                logger.info(f'Creating hierachical Time Series Dataframe for Hierarchy: {"/".join(list(self.hierarchy.values()))} ' +
                            f'with Time Granularity: {self.time_granularity}')
                X, S, tags = generate_time_series(df = X, date_col = self.date_col, 
                                                  time_granularity = self.time_granularity, hierarchy = self.hierarchy)
                
                # LOGGING INFO -- Missing data imputation (inside the function)
                X = missing_data_imputation(missing_data_strategy = self.missing_data_strategy, df = X)

            else:
                pass
        elif self.usecase == "televisita":
            pass
        elif self.usecase == "teleassistenza":
            pass
        elif self.usecase == "telemonitoraggio":
            pass
        
        logger.info('DONE Preprocessing.', important=True)
        return X, S, tags
    

    def save(self, path: str) -> None:
        """Store instance to file.
        Parameters
        ----------
        path : str
            Path to the file where the object must be stored.
        """

        with open(path, 'wb') as f:
            pickle.dump(self, f)
        
        return


    @classmethod
    def load(cls, path: str) -> Self:
        """Load instance from file.
        Parameters
        ----------
        path : str
            Path to the file where the object must be stored.
        """
        with open(path, 'rb') as f:
            return pickle.load(f)

