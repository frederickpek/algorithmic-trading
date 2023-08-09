import pandas as pd

def sma(arr: pd.Series, n: int) -> pd.Series:
    return pd.Series(arr).rolling(n).mean()

