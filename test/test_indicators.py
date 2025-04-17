import pandas as pd
from modules.indicators import yoy_growth

def test_yoy_growth():
    s1 = pd.Series([100, 120])
    s2 = pd.Series([ 80, 100])
    out = yoy_growth(s1, s2)
    assert list(out) == [25.0, 20.0]