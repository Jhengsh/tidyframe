""" Easy Select Column Method from Pandas DataFrame """

from copy import deepcopy

def select(df, columns=None, columns_minus=None, columns_between=None, copy=False):
    """
    Select Pandas DataFrame by minus

    Parameters
    ----------
    df : Pandas DataFrame
    columns_minus : column which want to remove
    copy : whether return deep copy DataFrame

    Returns
    -------
    df_return : Pandas DataFrame
    """
    if columns is not None:
        df_return = df[columns]
    if columns_minus is not None:
        raw_col = {value:i for i, value in enumerate(df.columns)}
        for pop_key in columns_minus:
            raw_col.pop(pop_key)
        df_return = df[list(raw_col.keys())]
    if columns_between is not None:
        columns_location = {column:i for i, column in enumerate(df.columns) }
        assert columns_location[columns_between[0]] < columns_location[columns_between[1]], 'first column location must less than second column location'
        df_return = df.iloc[:,range(columns_location[columns_between[0]], columns_location[columns_between[1]] + 1)]
    if copy:
        return deepcopy(df_return)
    else:
        return df_return
