import yfinance as yf
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta


def get_names(tickers):
    names = []
    for ticker in tickers:
        data = yf.Ticker(ticker)
        names.append(data.info['longName'])
    return names

def get_return_1d(data, tickers):
    returns_1d = []
    for ticker in tickers:
        returns_1d.append(data[ticker]['Close'].pct_change()[::-1].head(1).values[0])
    return returns_1d
    

tickers = ["META", "AAPL", "MSFT", "TSLA", "AMZN", "SHEL", "NSRGY", "ROG.SW", "OR.PA", "AZN"]
try:
    data = yf.download(tickers=tickers, end=datetime.datetime.now(), start=datetime.datetime.now() - relativedelta(months=1), group_by='ticker')
except Exception as exception:
    print(f"An error occurred while fetching tickers: {exception}")

returns_1d = get_return_1d(data, tickers)
names = get_names(tickers)
print(returns_1d)
print(names)
#print(data['AMZN']['Close'].pct_change(periods=1, freq='M'))