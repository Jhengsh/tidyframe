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
    coalesce column by list of column

    Parameters
    ----------
    df : Pandas DataFrame
    columns : list or pandas index
    default_value : value which replace None or NaN in return series 

    Returns
    -------
    return_series : Pandas DataFrame
    """
    return_series = df[columns[0]]
    for colmun in columns[1:]:
        return_series = getattr(return_series, 'combine_first')(df[colmun])
    if not pd.isna(default_value):
        return_series = return_series.fillna(default_value)
    return return_series
