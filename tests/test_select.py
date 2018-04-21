from tidyframe import tools
import pandas as pd
import numpy as np

def test_select():
    df = pd.DataFrame(np.array(range(10)).reshape(2,5), columns=list('abcde'))
    tools.select(df, columns_minus=['b', 'd'])
