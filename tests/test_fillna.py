import pandas as pd
from tidyframe import fillna


def test_fillna_basic():
    result = fillna([None] * 3, [1, pd.np.NaN, None], [1, 2, 3])
    for x, y in zip(result, [1, 2, 3]):
        assert x == y, "fillna result not equal"
