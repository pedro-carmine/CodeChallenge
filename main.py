import yfinance as yf
import pandas as pd

tickers = ["META", "AAPL", "MSFT", "TSLA", "AMZN", "SHEL", "NSRGY", "ROG.SW", "OR.PA", "AZN"]
headers = ['Symbol', 'Name', 'Last Date', 'Last Close', 'Return 1D', 'Return 1W', 'Return 1M', 'Average 1M']


def get_names(tickers):
    names = []
    for ticker in tickers:
        try:
            data = yf.Ticker(ticker)
        except Exception as exception:
            print(f"An error occurred while fetching tickers: {exception}")

        names.append(data.info['longName'])
    return names


def get_last_close_dates(data, tickers):
    last_close_dates = []
    for ticker in tickers:
        last_close_dates.append(data[ticker].index.to_pydatetime()[-1].strftime("%Y-%m-%d"))
    return last_close_dates


def get_return_1d(data, tickers):
    returns_1d = []
    for ticker in tickers:
        returns_1d.append("%0.2f" % data[ticker]['Close'].pct_change()[::-1].head(1).values[0])
    return returns_1d


def get_return_1w(data, tickers):
    returns_1w = []
    for ticker in tickers:
        returns_1w.append(data[ticker]['Close'].pct_change(periods=5).values[-1])
    return returns_1w


def get_return_1m(data, tickers):
    returns_1m = []
    for ticker in tickers:
        returns_1m.append(data[ticker]['Close'].pct_change(periods=21, fill_method="bfill").values[-1])
    return returns_1m


def get_month_avg(data, tickers):
    avg = []
    for ticker in tickers:
        rows = data[ticker]['Close']
        avg.append(rows.sum() / rows.count())
    return avg


def get_last_closes(data, tickers):
    last_closes = []
    data = data[::-1]
    for ticker in tickers:
        last_closes.append(data[ticker]['Close'].head(1).values[0])
    return last_closes


def create_ts(data, tickers):
    ts = {}
    for ticker in tickers:
        pass


def get_prices(data, tickers):
    prices = {}
    data = data[::-1]
    for ticker in tickers:
        prices[ticker] = data[ticker]['Close'].head(10).values.round(2)
    return prices


try:
    data = yf.download(tickers=tickers, period='1mo', group_by='ticker')
except Exception as exception:
    print(f"An error occurred while fetching tickers: {exception}")

returns_1d = get_return_1d(data, tickers)
returns_1w = get_return_1w(data, tickers)
returns_1m = get_return_1m(data, tickers)
names = get_names(tickers)
last_close_dates = get_last_close_dates(data, tickers)
last_closes = get_last_closes(data, tickers)
average = get_month_avg(data, tickers)

df_data = list(zip(tickers, names, last_close_dates, last_closes, returns_1d, returns_1w, returns_1m, average))
df = pd.DataFrame(df_data, columns=headers).sort_values(by='Symbol')
print(df.to_string(index=False))

newdict = get_prices(data, tickers)
print(str(newdict))
