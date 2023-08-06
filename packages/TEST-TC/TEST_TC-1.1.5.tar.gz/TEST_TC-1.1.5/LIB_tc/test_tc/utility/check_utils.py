from .exceptions import InputTypeError, ConversionError
from typing import Any, Iterable

def check_not_isinstance(obj: Any, data_type: Any, func: str, attached_message: str = ''):
    """
    The function check if an object is of a given data type

    Parameters
    ----------
    obj : Any
        The object that needs to be checked
    data_type : Any
        The reference data type 
    func: str
        String referring to the function which is raising the errors
    attached_message: str, Optional
        Additional message to attach to the error message, by default ''

    Raises
    ------
    InputTypeError
        If the object is not of the data type specified
    """
    if not isinstance(obj, data_type):
        m = f"Type input obj {type(obj)} must be {data_type}"
        if attached_message:
            m+=f' - {attached_message}'

        raise InputTypeError(func, message=m)

def check_not_in_iterable(obj: Any, iterable: Iterable, func: str, attached_message: str = ''):
    """
    The function check if an object is in an iterable

    Parameters
    ----------
    obj : Any
        The object that needs to be checked
    iterable : Iterable
        The reference iterable
    func: str
        String referring to the function which is raising the errors
    attached_message: str, Optional
        Additional message to attach to the error message, by default ''

    Raises
    ------
    InputTypeError
        If the object is not in the iterable specified
    """
    if obj not in iterable:
        m = f"Invalid value for {obj}. Value not found in {iterable}"
        if attached_message:
            m+=f' - {attached_message}'
            
        raise InputTypeError(func, message=f"Invalid value for {obj}. Value not found in {iterable} - {attached_message}")
    
def check_datatype_convertible(obj: Any, data_type_conversion: Any, func: str, attached_message: str = ''):
    """The function checks if an object can be casted to a given datatype

    Parameters
    ----------
    obj : Any
        The object that needs to be checked
    data_type_conversion : Any
        The data type convertion function
    func : str
        String referring to the function which is raising the errors
    attached_message : str, optional
        Additional message to attach to the error message, by default ''

    Raises
    ------
    ConversionError
        If the object can not be casted
    """
    try:
        data_type_conversion(obj)
    except (ValueError, TypeError):
        m = f'The object {obj} cannot be converted into data type {data_type_conversion}'
        if attached_message:
            m += f' - {attached_message}'
        raise ConversionError(func = func, message = m)
