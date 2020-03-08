import pandas as pd
from tidyframe import try_expect_raw


def test_try_expect_raw_basic():
    my_sum = try_expect_raw(lambda x, y: x + y)
    assert my_sum(1, y='a') == 1
