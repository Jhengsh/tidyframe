import pandas as pd
from tidyframe.tools import nvl


def test_nvl_series():
    test_list = [0, 1, None, pd.np.NaN]
    test_series = pd.Series(test_list)
    nvl(test_series, 10)


def test_nvl_list():
    test_list = [0, 1, None, pd.np.NaN]
    nvl(test_list, 10)


def test_nvl_int():
    nvl(None, 10)


def test_nvl_str():
    nvl(None, 'abc')
