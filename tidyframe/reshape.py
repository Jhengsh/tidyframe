import pandas as pd

def gather(df, key_col=None, key='key', value='value', dropna=True):
    """Gather column to key-value pairs

    Parameters
    ----------
    df: DataFrame
    *args: return key-value of key columns
    key: return DataFrame column name of key
    value: return DataFrame column name fo value
    dropna : boolean, default True
        Whether to drop rows in the resulting Frame/Series with no valid values
    """
    if key_col is None:
        key_col = df.columns
        index = []
        df = df.reset_index()
    elif isinstance(key_col, str):
        key_col = [key_col]
        df = df.reset_index()
        index = df.columns.difference(key_col).values.tolist()
    elif isinstance(key_col, (list, pd.core.indexes.base.Index)):
        index = df.columns.difference(key_col).values.tolist()
    if len(index)>0:
        df_tmp = df.set_index(index)
        df_return = df_tmp[key_col].stack(dropna=dropna).reset_index()
        columns_return = df_return.columns.values.copy()
        columns_return[-1] = value
        columns_return[-2] = key
        df_return.columns = columns_return
        return df_return
    else:
        df_tmp = df
        raw_index_name = df.index.name
        if raw_index_name is None:
            raw_index_name = 'index'
        df_return = df_tmp[key_col].stack(dropna=dropna)
        df_return = df_return.to_frame().reset_index()
        df_return.columns = [raw_index_name, key, value]
        return df_return

def spread(df, row_index, key):
    """Spread key-value pair to multiple columns
    df: long format Dataframe
    row_index: transform to wide format row index column
    key: key column which return DataFrame column name
    """
    list_index = []
    if isinstance(row_index, list):
        list_index.extend(row_index)
    else:
        list_index.append(row_index)
    if isinstance(key, list):
        list_index.extend(key)
    else:
        list_index.append(key)
    df = df.set_index(list_index)
    df = df.unstack(-1)
    return df

