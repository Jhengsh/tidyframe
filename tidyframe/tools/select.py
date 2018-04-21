from copy import deepcopy

def select(df, columns_minus=None, copy=False):
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
    if columns_minus is not None:
        raw_col = {value:i for i, value in enumerate(df.columns)}
        for pop_key in columns_minus:
            raw_col.pop(pop_key)
        df_return = df[list(raw_col.keys())]
    if copy:
        return deepcopy(df_return)
    else:
        return df_return
