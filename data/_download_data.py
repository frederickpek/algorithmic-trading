import pandas as pd
import yfinance as yf
from os.path import dirname, join


stocks = ['AAPL', 'GOOG', 'AMZN', 'TSLA', 'MCD', 'META']
forex  = ['EURUSD=X', 'GBPUSD=X', 'AUDUSD=X', 'SGDUSD=X']
crypto = ['BTC-USD', 'ETH-USD', 'LTC-USD', 'SOL-USD', 'DOGE-USD', 'ADA-USD']
tickers = stocks + forex + crypto


# df = yf.download(' '.join(tickers), start="2015-01-01", end="2023-08-01", group_by='tickers')
# 
# cols = ['Open', 'High', 'Low', 'Close', 'Volume']
# for ticker in tickers:
# 	ticker_df = df[ticker]
# 	ticker_df = ticker_df[cols]
# 	ticker_df = ticker_df.dropna()
# 	ticker_df.to_csv(f'./{ticker}.csv')


def _read_file(filename):
    return pd.read_csv(join(dirname(__file__), filename), index_col=0, parse_dates=True)


AAPL = _read_file('AAPL.csv')
GOOG = _read_file('GOOG.csv')
AMZN = _read_file('AMZN.csv')
TSLA = _read_file('TSLA.csv')
MCD = _read_file('MCD.csv')

EUR = _read_file('EURUSD=X.csv')
GBP = _read_file('GBPUSD=X.csv')
AUD = _read_file('AUDUSD=X.csv')
SGD = _read_file('SGDUSD=X.csv')

BTC = _read_file('BTC-USD.csv')
ETH = _read_file('ETH-USD.csv')
LTC = _read_file('LTC-USD.csv')
SOL = _read_file('SOL-USD.csv')
DOGE = _read_file('DOGE-USD.csv')
ADA = _read_file('ADA-USD.csv')
