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

tickers = ["META", "AAPL", "MSFT", "TSLA", "AMZN", "SHEL", "NSRGY", "ROG.SW", "OR.PA", "AZN"]
try:
    data = yf.download(tickers=tickers, end=datetime.datetime.now(), start=datetime.datetime.now() - relativedelta(months=1))
except Exception as exception:
    print(f"An error occurred while fetching tickers: {exception}")

data = data[::-1].head()

names = get_names(tickers)