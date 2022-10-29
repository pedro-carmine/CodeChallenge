import yfinance as yf
import pandas as pd

tickers = ["META", "AAPL", "MSFT", "TSLA", "AMZN", "SHEL", "NSRGY", "ROG.SW", "OR.PA", "AZN"]
try:
    tickers = (yf.Ticker(ticker) for ticker in tickers)
except Exception as exception:
    print(f"An error occurred while fetching tickers: {exception}")


for ticker in tickers:
    print(ticker)