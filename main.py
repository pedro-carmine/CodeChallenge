import yfinance as yf
import pandas as pd

tickers = ["META", "AAPL", "MSFT", "TSLA", "AMZN", "SHEL", "NSRGY", "ROG.SW", "OR.PA", "AZN"]
tickers = (yf.Ticker(ticker) for ticker in tickers)

for ticker in tickers:
    print(ticker)