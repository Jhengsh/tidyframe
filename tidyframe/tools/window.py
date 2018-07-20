import pandas as pd


def apply_cum(series,
              cum_func=lambda x, y: x + y,
              judge_func=lambda x: False,
              init_value=0):
    """
    Apply Cumulative Function on Series or list

    series: list or series
    cum_func: cumulative function with two parameters
    judge_func: judge function which return value is True or False for reset cumulative value
    init_value: reset value if judge function result is True
    """
    index_first = [True] + [False] * (len(series) - 1)
    index_last = [False] * len(series)
    cum_value = []
    current_value = init_value
    for i, x in enumerate(series):
        current_value = cum_func(current_value, x)
        cum_value.append(current_value)
        if judge_func(current_value):
            current_value = init_value
            if i + 1 < len(series):
                index_first[i + 1] = True
                index_last[i] = True
            else:
                index_last[i] = True
    df_return = pd.DataFrame({
        'index_first': index_first,
        'index_last': index_last,
        'cum_value': cum_value
    })
    return df_return[['cum_value', 'index_first', 'index_last']]
