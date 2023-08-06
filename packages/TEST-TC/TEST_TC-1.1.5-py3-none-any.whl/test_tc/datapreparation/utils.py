import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.base import BaseEstimator, TransformerMixin
from typing_extensions import Self
from typing import List, Tuple, Union, Dict
from hierarchicalforecast.utils import aggregate

from ..utility.tele_logger import logger
from ..utility.check_utils import check_not_isinstance, check_not_in_iterable
from ..utility.constants import code_to_region_name, code_to_speciality
from ..utility.resources import get_module_and_function

################# Transformer Functions #################
def map_columns(hierarchy: Dict[str, str], df: pd.DataFrame, 
                conversion: Dict[str, str]) -> pd.DataFrame:
    
    """
    Change the columns in the dataframe <df> according to a given <hierarchy> and <conversion> dictionary.
    The hierarchy and the conversion dictionaries MUST be specifed in the configuration file.

    Parameters
    ----------
    hierarchy : Dict[str, str]
        A dictionary mapping levels to the <df> column names.
    df : pd.DataFrame
        The input DataFrame to be mapped.
    conversion : Dict[str, str]
        A dictionary mapping levels to conversion names.

    Returns
    -------
    pd.DataFrame
        Containing the modified dataframe if there is a conversion to apply
    """
    # Verify that hierarchy is of type dict
    check_not_isinstance(obj = hierarchy, data_type = dict, func = get_module_and_function())
    # Verify that conversion is of type dict
    check_not_isinstance(obj = conversion, data_type = dict, func = get_module_and_function())
    # Verify that df is of type pd.DataFrame
    check_not_isinstance(obj = df, data_type = pd.DataFrame, func = get_module_and_function())

    df = df.copy()

    for conversion_level in conversion.keys():
        if conversion[conversion_level]:
            name_column = hierarchy[conversion_level]

            # Verify that name_column is a column in df
            check_not_in_iterable(obj = name_column, iterable = df.columns, func = get_module_and_function())

            dict_mapping = eval(conversion[conversion_level]) # Takes the conversion level string and reads it from utility.constants
            df[name_column] = df[name_column].apply(lambda x: dict_mapping[x])
    return df

def generate_time_series(df: pd.DataFrame, date_col: str,
                         time_granularity: str, hierarchy: Dict[str, str]) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, List[str]]]:
    """
    Sequential execution of transformations to obtain a DataFrame with a time series structure

    Parameters
    ----------
    df : pd.DataFrame
        Raw dataframe from which generates timeseries
    date_col : str
        Column name identifying the columns to index on
    time_granularity : str 
        Specifies temporal granularity
    hierarchy : Dict[str, str]
        A dictionary mapping levels to the <df> column names.

    Returns:
    Tuple[pd.DataFrame, pd.DataFrame, Dict[str, List[str]]]
        Returns a tuple with the following elements:
            - Y_df dataframe with the hierarchies as indexes
            - S_df binary matrix to understand the hierarchy levels
            - tags maps the hierarchy level to the hierarchy values 
    """
    
    # Verify that df is of type pd.DataFrame
    check_not_isinstance(obj = df, data_type = pd.DataFrame, func = get_module_and_function())
    # Verify that date_col is a column in df
    check_not_in_iterable(obj = date_col, iterable = df.columns, func = get_module_and_function())
    # Verify time granularity date type
    check_not_isinstance(obj = time_granularity, data_type = str, func = get_module_and_function())
    # Verify hierarchy date type
    check_not_isinstance(obj = hierarchy, data_type = dict, func = get_module_and_function())

    # Raw dataset from which to generate the time series
    df = df.copy()
    
    # Starting generating the time series
    hier_df = get_hierarchical_df(df = df, hierarchy = hierarchy, time_granularity = time_granularity, date_col = date_col)
    Y_df, S_df, tags = get_hierarchical_info(hier_df = hier_df)

    Y_df['y'] = Y_df['y'].replace(0, np.nan)

    return Y_df, S_df, tags

def get_hierarchical_df(df: pd.DataFrame, hierarchy: Dict[str, str],
                        time_granularity: str, date_col: str) -> pd.DataFrame:
    """
    The function generates the dataframe suitable for obtaining hierarchical info. 
    It generates the dataframe starting from the input dataframe by using the information
    of the configuration file.

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe (typically inside .../data/input)
    hierarchy : Dict[str, str]
        Dictionary retrieved from the configuration file.
        it contains the hierarchy columns ordered by levels
    time_granularity : str
        String referring to the time granularity.
        Information retrieved from the configuration file.
    date_col : str
        The string referring to the date column of the dataframe
    Returns
    -------
    pd.DataFrame
        A dataframe of columns: ds|y|level0|level1|level2|level3
        level0 refers to Italia
        level1, level2, level3 are obtained from the hierarchy dict
    """
    
    output_df = df[[date_col]] # Grabs the time columns, output_df remains a dataframe
    output_df['level0'] = 'Italia' # Sets level0 as the macro hierarchy Italia
    output_df['y'] = 1 # Sets 1 for each observation

    # Transforms the dataframe based on a given time_granularity (e.g. 'H' (hours), 'D' (days), 'M' (months), ...)
    # and clips them to the said granularity in order to have multiple same dates to let the aggregate sum them up
    output_df[date_col] = output_df[date_col].dt.to_period(time_granularity).dt.to_timestamp()

    # For each level, attaches the column to the output_df
    for level, col_name in hierarchy.items():
        output_df[level] = df[col_name]
    output_df = output_df.rename(columns={date_col:'ds'}) # Normalize the date_col name into 'ds'
    return output_df

def get_hierarchical_info(hier_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, List[str]]]:
    """
    The function generates the hierarchical aggregation info
    starting from the hierarchical dataframe obtained by <get_hierarchical_df>

    Parameters
    ----------
    hier_df : pd.DataFrame
        Dataframe obtained by <get_hierarchical_df>

    Returns
    -------
    Tuple[pd.DataFrame, pd.DataFrame, Dict[str, List[str]])
        Returns a tuple with the following elements:
            - Y_df dataframe with the hierarchies as indexes
            - S_df binary matrix to understand the hierarchy levels
            - tags maps the hierarchy level to the hierarchy values 

    """
    # Filters and sorts the columns regarding hiherarchy's levels
    filtered_columns = [col for col in hier_df.columns if 'level' in col]
    filtered_columns.sort()

    spec = [filtered_columns[:i] for i in range(1, len(filtered_columns) + 1)] # Builds the spec needed for the aggregate function
    Y_df, S_df, tags = aggregate(df = hier_df, spec = spec) # Executes the aggregations based on timestamps

    return Y_df, S_df, tags

def missing_data_imputation(missing_data_strategy: Union[str,int,dict], df: pd.DataFrame) -> pd.DataFrame:
    """
    The function imputes the missing values of the dataframe <df> with a given strategy <missing_data_strategy>

    Parameters
    ----------
    missing_data_strategy : dict, str or int
        Identifies whether to impute missing values and if so using which strategy/value
        Allowed parameters: 
            if str:
                ""      : none of the missing values are replaced
                "mean"  : missing values are replaced with the mean of the known values in the dataset.
                "median": missing values are replaced with the median of the known values in the dataset.
                "zero"  : missing values are replaced with the 0.
                "bfill" : missing values are replaced with the next available value in the dataset.
                "ffill" : missing values are replaced with the most recent preceding value in the dataset.
            if int:
                replace NaN with the specified integer
            if dict:
                replace NaN using the specified interpolation method (allowed "polynomial" or "spline") and its order.

    df : pd.DataFrame
    The dataframe which target column will be filled with a given strategy

    Returns
    -------
    pd.DataFrame
        The dataframe afer the imputation

    Raises
    ------
    ValueError
        Invalid value for spline order
    """

    df = df.copy()
    if isinstance(missing_data_strategy, dict): 
        if missing_data_strategy['interpolation'] == "spline" and (df['y'].notna().sum() < missing_data_strategy['order'] or missing_data_strategy['order'] >5):
            logger.error('The number of data points must be larger than the spline degree k or k should be 1 <= k <= 5.')
            raise ValueError("Invalid value for spline order in 'datapreparation_utils.generate_time_series'")
        
    if missing_data_strategy == "":
        logger.info('No Missing Data Imputation applied.')
    else:
        logger.info(f'Missing Data Imputation with Strategy: {missing_data_strategy}')
        fillna = ReplacerNA(missing_data_strategy)
        df = fillna.fit_transform(df)
        df['y'] = df['y'].clip(lower=0)

    return df


################# Utils Teleconsulto  #################
def filter_target_col(df: pd.DataFrame, target_col: Union[str, List[str]]) -> pd.DataFrame:
    """
    The function filters the rows of the dataframe on the unique target_col 

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe
    target_col : Union[str, List[str]]
        The target column

    Returns
    -------
    pd.DataFrame
        The dataframe with the unique values for the target col
    """
    df = df.copy()
    df = df.drop_duplicates(subset=target_col)
    return df

################# Transformer Classes #################
class Normalizer(BaseEstimator, TransformerMixin):
    def __init__(self):
        """
        Normalize data to the range [0, 1].
        """
        pass

    def fit(self, X, y=None):
        """
        Fit the Normalizer to the data. No computations are needed in this case.

        Parameters:
        -----------
        X : array-like
            Input data.

        Returns:
        --------
        self : object
            Fitted Normalizer object.
        """
        
        self.min = np.min(X)
        self.max = np.max(X)
        return self

    def transform(self, X):
        """
        Normalize the input data to the range [0, 1].

        Parameters:
        -----------
        X : array-like
            Input data.

        Returns:
        --------
        X_normalized : array-like
            Normalized data obtained by scaling the values to the range [0, 1].
        """
        X_normalized = (X - self.min) / (self.max - self.min)
        return X_normalized

    def inverse_transform(self, X_normalized):
        """
        Reconstruct the original data from the normalized data by applying the inverse transformation.

        Parameters:
        -----------
        X_normalized : array-like
            Normalized data.

        Returns:
        --------
        X : array-like
            Reconstructed data obtained by applying the inverse transformation.
        """
        X = X_normalized * (self.max -self.min) + self.min
        return X
  

class ReplacerNA(TransformerMixin, BaseEstimator):

    def __init__(self, method: Union[str, int, Dict[str, Union[str, int]]]) -> Self:

        """Class for handling of NA

        Parameters
        ----------
        method : Union[str, int, Dict[str, Union[str, int]]]]
            If str specify the method to replace NA value (mean,median,zero), if int specify the value to replace NA value
            If dict specify which interpolation method to use between polynomial and spline and its order
        """
        
        self.method = method

    def fit(self, X: pd.DataFrame) -> Self:

        """Compute value useful for replacing NA

        Parameters
        ----------
        X : pd.DataFrame
            Dataframe containing two columns (timestamp and volumes of time series)         

        Returns
        -------
        self : object
            Fitted replacer
        """
        
        if self.method == "mean":
            self.value = X.iloc[:,1].mean()
            self.method_for_df = None
        elif self.method == "median":
            self.value = X.iloc[:,1].median()
            self.method_for_df = None
        elif self.method == "zero":
            self.value = 0
            self.method_for_df = None
        elif self.method == "bfill":
            self.value = None
            self.method_for_df = "bfill"
        elif self.method == "ffill":
            self.value = None
            self.method_for_df = "ffill"
        elif self.method == "interpolate":
            self.value = None
            self.method_for_df = "interpolate"
        elif isinstance(self.method, dict):
            self.value = self.method["order"]
            self.method_for_df = self.method["interpolation"].lower()

        else:
            self.value = self.method
            self.method_for_df = None

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        """Perform replacement of missing values

        Parameters
        ----------
        X : pd.DataFrame
            Dataframe containing two columns (timestamp and volumes of time series)

        Returns
        -------
        X : pd.DataFrame
            Transformed time series
        """
        if self.method_for_df in ["polynomial", "spline"]:
            # Create a temporary DataFrame with a DatetimeIndex
            temp_df = pd.DataFrame({X.columns[1]: X.iloc[:, 1]})
            temp_df.index = pd.to_datetime(X.iloc[:, 0])

            # Perform time-based interpolation in the temporary DataFrame
            temp_df.iloc[:, 0] = temp_df.iloc[:, 0].interpolate(method=self.method_for_df, order = self.value)

            # Assign the interpolated values to the original column in the X DataFrame
            X.iloc[:, 1] = temp_df.iloc[:, 0].values
        else:
            X.fillna(self.value, method=self.method_for_df, inplace=True)
        return X
    

class Detrender(TransformerMixin, BaseEstimator):

    def __init__(self, period: int) -> Self:

        """Detrending time series

        Parameters
        ----------
        period : int
            Specify period considered for compute additive decomposition

        Returns
        -------
        self : object
        """

        self.period = period


    def fit(self, X: pd.DataFrame) -> Self:

        """Compute additive decomposition useful to detrend time series

        Parameters
        ----------
        X : pd.DataFrame
            Dataframe containing two columns (timestamp and volumes of time series)         

        Returns
        -------
        self : object
            Fitted detrender
        """

        additive_decomp = seasonal_decompose(X.iloc[:,1], model="additive", period=self.period, extrapolate_trend="freq")
        self.trend = additive_decomp.trend

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        """Perform detrending of time series

        Parameters
        ----------
        X : pd.DataFrame
            Dataframe containing two columns (timestamp and volumes of time series)

        Returns
        -------
        X : pd.DataFrame
            Transformed time series
        """

        detrend_time_series = X.iloc[:,1] - self.trend
        ris = pd.concat([X.iloc[:,0],detrend_time_series],axis=1)
        ris.columns = X.columns

        return  ris
    

class Deseasoner(TransformerMixin, BaseEstimator):

    def __init__(self, period: int) -> Self:

        """Deseasonalises time series

        Parameters
        ----------
        period : int
            Specify period considered for compute additive decomposition
        """

        self.period = period


    def fit(self, X: pd.DataFrame) -> Self:

        """Compute additive decomposition useful to deseasonalises time series

        Parameters
        ----------
        X : pd.DataFrame
            Dataframe containing two columns (timestamp and volumes of time series)         

        Returns
        -------
        self : object
            Fitted deseasoner
        """
        
        additive_decomp = seasonal_decompose(X.iloc[:,1], model="additive", period=self.period, extrapolate_trend="freq")
        self.seasonal = additive_decomp.seasonal

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        """Perform deseasonalises of time series

        Parameters
        ----------
        X : pd.DataFrame
            Dataframe containing two columns (timestamp and volumes of time series)

        Returns
        -------
        X : pd.DataFrame
            Transformed time series
        """

        deseason_time_series = X.iloc[:,1] - self.seasonal
        ris = pd.concat([X.iloc[:,0],deseason_time_series],axis=1)
        ris.columns = X.columns

        return ris


class Differencer(TransformerMixin, BaseEstimator):

    def __init__(self, lag: int) -> Self:

        """Differencing time series
        
        Parameters
        ----------
        lag : int
            Differencing time series lag

        Returns
        -------
        self : object
        """

        self.lag = lag

    def fit(self, X: pd.DataFrame) -> Self:

        """Compute value useful to compute differencing time series

        Parameters
        ----------
        X : pd.DataFrame
            Dataframe containing two columns (timestamp and volumes of time series)         

        Returns
        -------
        self : object
            Fitted normalizer
        """

        self.shape = X.shape[0]
        self.lag_time_series = X.iloc[:self.shape-self.lag,1]
        self.timestamp = X.iloc[self.lag:,0].reset_index(drop=True)

        return self
    
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        """Perform differencing time series

        Parameters
        ----------
        X : pd.DataFrame
            Dataframe containing two columns (timestamp and volumes of time series)

        Returns
        -------
        X : pd.DataFrame
            Transformed time series
        """

        time_series_lagged = X.iloc[self.lag:,1].reset_index(drop=True) - self.lag_time_series
        ris = pd.concat([self.timestamp,time_series_lagged], axis=1)
        ris.columns = X.columns
        
        return ris


class OutlierRemover(BaseEstimator, TransformerMixin):
    def __init__(self, lower_threshold_percentile: Union[int, float] =5, upper_threshold_percentile: Union[int, float]=95):
        """
        Remove outliers from a dataset by capping values above and below thresholds.

        Parameters:
        -----------
        lower_threshold_percentile : Union[int, float], optional 
            Percentile threshold below which values will be capped, by default 5
        upper_threshold_percentile : Union[int, float], optional
            Percentile threshold above which values will be capped, by default 95
        """
        self.upper_threshold_percentile = upper_threshold_percentile
        self.lower_threshold_percentile = lower_threshold_percentile
        self.upper_threshold = None
        self.lower_threshold = None

    def fit(self, X, y=None):
        """
        Compute the upper and lower thresholds based on percentiles of the input data.

        Parameters:
        -----------
        X : array-like
            Input data.

        Returns:
        --------
        self : object
            Fitted OutlierRemover object.
        """
        self.upper_threshold = np.percentile(X, self.upper_threshold_percentile)
        self.lower_threshold = np.percentile(X, self.lower_threshold_percentile)
        return self

    def transform(self, X):
        """
        Cap the values above the upper threshold and below the lower threshold.

        Parameters:
        -----------
        X : array-like
            Input data.

        Returns:
        --------
        X_transformed : array-like
            Transformed data with capped outlier values.
        """
        X[X > self.upper_threshold] = self.upper_threshold
        X[X < self.lower_threshold] = self.lower_threshold
        return X
    

class Smoother(BaseEstimator, TransformerMixin):
    def __init__(self, window_size: int):
        """
        Smoothes a time series by applying a moving average window.

        Parameters:
        -----------
        window_size : int
            Size of the moving average window.
        """
        self.window_size = window_size

    def fit(self, X, y=None):
        """
        Fit the Smoother to the data. No computations are needed in this case.

        Parameters:
        -----------
        X : array-like
            Input data.

        Returns:
        --------
        self : object
            Fitted Smoother object.
        """
        return self

    def transform(self, X):
        """
        Smooth the input data by applying a moving average window.

        Parameters:
        -----------
        X : array-like
            Input data.

        Returns:
        --------
        X_smoothed : array-like
            Smoothed data obtained by applying the moving average window.
        """
        
        X_smoothed = X.rolling(window=self.window_size, min_periods=1).mean()
        return X_smoothed


class Differentiator(BaseEstimator, TransformerMixin):
    def __init__(self, order: int):
        """
        Differentiates "order" times a time series by taking differences between consecutive values.

        Parameters:
        -----------
        order : int
            Order of differentiation.
        """
        self.order = order

    def fit(self, X, y=None):
        
        """
        Fit the Differentiator to the data. No computations are needed in this case.

        Parameters:
        -----------
        X : array-like
            Input data.

        Returns:
        --------
        self : object
            Fitted Differentiator object.
        """
        return self

    def transform(self, X):
        """
        Apply differentiation to the input data by taking differences between consecutive values.
 

        Parameters:
        -----------
        X : array-like
            Input data.


        Returns:
        --------
        X_transformed : array-like
            Transformed data obtained by taking differences between consecutive values.
        """
        X_transformed = X.copy()
        for _ in range(self.order):
            X_transformed = X_transformed.diff()
        X_transformed = np.nan_to_num(X_transformed, nan=0.0)
        return X_transformed


class LogTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        """
        Logarithmic transformation of data.
        """
        pass

    def fit(self, X, y=None):
        """
        Fit the LogTransformer to the data. No computations are needed in this case.

        Parameters:
        -----------
        X : array-like
            Input data.

        Returns:
        --------
        self : object
            Fitted LogTransformer object.
        """
        return self

    def transform(self, X):
        """
        Apply the logarithmic transformation to the input data.

        Parameters:
        -----------
        X : array-like
            Input data.

        Returns:
        --------
        X_transformed : array-like
            Transformed data obtained by applying the logarithmic transformation.
        """
        X_transformed = np.log1p(X)
        return X_transformed

    def inverse_transform(self, X_transformed):
        """
        Reconstruct the original data from the transformed data by applying the inverse logarithmic transformation.

        Parameters:
        -----------
        X_transformed : array-like
            Transformed data.

        Returns:
        --------
        X_reconstructed : array-like
            Reconstructed data obtained by applying the inverse logarithmic transformation.
        """
        X_reconstructed = np.expm1(X_transformed)
        return X_reconstructed
