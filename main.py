import yfinance as yf
import pandas as pd
import streamlit as st

tickers = ["META", "AAPL", "MSFT", "TSLA", "AMZN", "SHEL", "NSRGY", "ROG.SW", "OR.PA", "AZN"]
headers = ['Symbol', 'Name', 'Last Date', 'Last Close', 'Return 1D', 'Return 1W', 'Return 1M', 'Average 1M']


def get_names(tickers) -> list:
    names = []
    for ticker in tickers:
        try:
            data = yf.Ticker(ticker)
        except Exception as exception:
            print("An error occurred while fetching tickers:")
            raise exception

        names.append(data.info['longName'])
    return names


def get_last_close_dates(data, tickers) -> list:
    last_close_dates = []
    for ticker in tickers:
        last_close_dates.append(data[ticker].index.to_pydatetime()[-1].strftime("%Y-%m-%d"))
    return last_close_dates


def get_return_1d(data, tickers) -> list:
    returns_1d = []
    for ticker in tickers:
        returns_1d.append("%0.2f" % data[ticker]['Close'].pct_change()[::-1].head(1).values[0])
    return returns_1d


def get_return_1w(data, tickers) -> list:
    returns_1w = []
    for ticker in tickers:
        returns_1w.append(data[ticker]['Close'].pct_change(periods=5).values[-1])
    return returns_1w


def get_return_1m(data, tickers) -> list:
    returns_1m = []
    for ticker in tickers:
        returns_1m.append(data[ticker]['Close'].pct_change(periods=21, fill_method="bfill").values[-1])
    return returns_1m


def get_month_avg(data, tickers) -> list:
    avg = []
    for ticker in tickers:
        rows = data[ticker]['Close']
        avg.append(rows.sum() / rows.count())
    return avg


def get_last_closes(data, tickers) -> list:
    last_closes = []
    data = data[::-1]
    for ticker in tickers:
        last_closes.append(data[ticker]['Close'].head(1).values[0])
    return last_closes


def create_ts(data, tickers):
    ts = {}
    for ticker in tickers:
        pass


def get_marketcap(tickers) -> dict:
    countries_mkcap = {}
    count = 0

    for ticker in tickers:
        count += 1
        info = yf.Ticker(ticker).info
        country = info['country']
        mkcap = info['marketCap']

        if country in countries_mkcap:
            current = countries_mkcap[country]['mkcap']
            countries_mkcap[country]['mkcap'] = current + mkcap
            countries_mkcap[country]['count'] += 1
        else:
            country_dict = {'mkcap': mkcap, 'count': 1}
            countries_mkcap[country] = country_dict

    countries_mkcap['total_count'] = count
    return countries_mkcap


def get_prices(data, tickers) -> dict:
    prices = {}
    data = data[::-1]
    for ticker in tickers:
        prices[ticker] = data[ticker]['Close'].head(10).values.round(2)
    return prices


def country_statistics(mkcap: dict) -> dict:
    statistics = {}
    total_count = mkcap.pop('total_count')  # retrieves values and remove from the dict

    for key, val in mkcap.items():
        statistics[key] = {'Symbols': val['count'], 'Weighted Average Price': val['mkcap'] * val['count'] / total_count}

    return statistics


@st.experimental_memo
def load_data(df_data, headers):
    return pd.DataFrame(df_data, columns=headers).sort_values(by='Symbol')


try:
    data = yf.download(tickers=tickers, period='1mo', group_by='ticker')
except Exception as exception:
    print("An error occurred while fetching tickers:")
    raise exception

returns_1d = get_return_1d(data, tickers)
returns_1w = get_return_1w(data, tickers)
returns_1m = get_return_1m(data, tickers)
names = get_names(tickers)
last_close_dates = get_last_close_dates(data, tickers)
last_closes = get_last_closes(data, tickers)
average = get_month_avg(data, tickers)

df_data = list(zip(tickers, names, last_close_dates, last_closes, returns_1d, returns_1w, returns_1m, average))
df = load_data(df_data, headers)
print(df.to_string(index=False))
#
# newdict = get_prices(data, tickers)
# print(str(newdict))

# mkcap = get_marketcap(tickers)
# stats = country_statistics(mkcap)
#
# df2 = pd.DataFrame(stats)
# print(df2.transpose())

st.header("Dystematic Dashboard")
st.subheader("Companies")
st.dataframe(df, use_container_width=True)
