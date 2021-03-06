from functools import wraps
import pandas as pd
from copy import deepcopy as cp


def nvl(obj, default=pd.np.nan, copy=True):
    """
    replace None or NaN value by default

    Parameters
    ----------
    obj : Series, list, or primitive variable types
    default : defalut
    copy : copy list or not if obj is list type

    Returns
    -------
    series or list or primitive variable types

    Examples
    ---------
    >>> import pandas as pd
    >>> from tidyframe.tools import nvl
    >>> nvl(None, 10)
    10
    >>> test_list = [0, 1, None, pd.np.NaN]
    >>> test_series = pd.Series(test_list)
    >>> nvl(test_series, 10)
    0     0.0
    1     1.0
    2    10.0
    3    10.0
    dtype: float64
    """
    if isinstance(obj, pd.core.series.Series):
        return obj.fillna(default)
    elif isinstance(obj, list):
        if copy:
            obj_copy = cp(obj)
        bool_obj = pd.Series(obj_copy).isna()
        for i, x in enumerate(bool_obj):
            if x:
                obj_copy[i] = default
        return obj_copy
    else:
        if pd.isna(obj):
            return default
        else:
            return obj


def coalesce(df, columns, default_value=pd.np.nan):
    """
    Coalesce column by list of column

    Parameters
    ----------
    df : Pandas DataFrame
    columns : list or pandas index
    default_value : value which replace None or NaN in return series 

    Returns
    -------
    Pandas Series

    Examples
    ---------
    >>> import pandas as pd
    >>> from tidyframe import coalesce
    >>> df = pd.DataFrame()
    >>> df['a'] = [None, pd.np.NaN, pd.np.nan, pd.np.nan]
    >>> df['b'] = [None, 4, 6, pd.np.nan]
    >>> df['c'] = [None, pd.np.NaN, 6, pd.np.nan]
    >>> coalesce(df, ['a', 'b', 'c'], default_value=10)
    0    10.0
    1     4.0
    2     6.0
    3    10.0
    Name: a, dtype: float64
    """
    return_series = df[columns[0]]
    for colmun in columns[1:]:
        return_series = getattr(return_series, 'combine_first')(df[colmun])
    if not pd.isna(default_value):
        return_series = return_series.fillna(default_value)
    return return_series


def fillna(*args):
    """
    Fill non null value

    Parameters
    ----------
    *args : list or series

    Returns
    -------
    list

    Examples
    ---------
    >>> import pandas as pd
    >>> from tidyframe import fillna
    >>> fillna([None] * 3, [1, pd.np.NaN, None], [1, 2, 3])
    [1, 2, 3]
    """
    list_return = []
    for x in zip(*args):
        for i in x:
            non_null_value = pd.np.nan
            if pd.notna(i):
                non_null_value = i
                list_return.append(i)
                break
        if pd.isna(non_null_value):
            list_return.append(i)
    return list_return


def try_expect_raw(function):
    """
    A decorator which return first args when execpt happen

    Parameters
    ----------
    *args : list or series

    Returns
    -------
    list

    Examples
    ---------
    >>> from tidyframe import try_expect_raw
    >>> my_sum = try_expect_raw(lambda x, y: x + y)
    >>> my_sum(1, y='a')
    1
    """
    @wraps(function)
    def decorator_func(*args, **kwargs):
        try:
            result = function(*args, **kwargs)
            return result
        except:
            if args:
                return args[0]
            else:
                raise Exception('args is None')

    return decorator_func
