#######################################
# Dystematic Code Challenge           |
# Pedro Carmine                       |
#######################################

import yfinance as yf
import pandas as pd
import streamlit as st

tickers = ["META", "AAPL", "MSFT", "TSLA", "AMZN", "SHEL", "NSRGY", "ROG.SW", "OR.PA", "AZN"]
headers = ['Symbol', 'Name', 'Last Date', 'Last Close', 'Return 1D', 'Return 1W', 'Return 1M', 'Average 1M']


def get_names(tickers: list) -> list:
    """Gets the name of the tickers specified in the tickers list.

    Args:
        tickers: List of the strings of the tickers to be fetched.

    Returns:
        List with the names of each ticker.
    """
    names = []
    for ticker in tickers:
        try:
            data = yf.Ticker(ticker)
        except Exception as exception:
            print("An error occurred while fetching tickers:")
            raise exception

        names.append(data.info['longName'])
    return names


def get_last_close_dates(data: pd.DataFrame, tickers: list) -> list:
    """Gets the last close date for each ticker from the yfinance API.

    Args:
        data: Dataframe with downloaded information of the tickers.
        tickers: List of the strings of the tickers to be fetched.

    Returns:
        List with last close dates for each ticker.
    """
    last_close_dates = []
    for ticker in tickers:
        last_close_dates.append(data[ticker].index.to_pydatetime()[-1].strftime("%Y-%m-%d"))
    return last_close_dates


@st.cache
def get_return_1d(data: pd.DataFrame, tickers: list) -> list:
    """Gets the value of the return in one day for each ticker.

    Args:
        data: Dataframe with downloaded information of the tickers.
        tickers: List of the strings of the tickers to be fetched.

    Returns:
        List with the value of the one-day return for each ticker.
    """
    returns_1d = []
    for ticker in tickers:
        returns_1d.append("%0.2f" % data[ticker]['Close'].pct_change()[::-1].head(1).values[0])
    return returns_1d


@st.cache
def get_return_1w(data: pd.DataFrame, tickers: list) -> list:
    """Gets the value of the return in one week for each ticker.

    Args:
        data: Dataframe with downloaded information of the tickers.
        tickers: List of the strings of the tickers to be fetched.

    Returns:
        List with the value of the one-week return for each ticker.
    """
    returns_1w = []
    for ticker in tickers:
        returns_1w.append(data[ticker]['Close'].pct_change(periods=5).values[-1])
    return returns_1w


@st.cache
def get_return_1m(data: pd.DataFrame, tickers: list) -> list:
    """Gets the value of the return in one month for each ticker.

    Args:
        data: Dataframe with downloaded information of the tickers.
        tickers: List of the strings of the tickers to be fetched.

    Returns:
        List with the value of the one-month return for each ticker.
    """
    returns_1m = []
    for ticker in tickers:
        returns_1m.append(data[ticker]['Close'].pct_change(periods=21, fill_method="bfill").values[-1])
    return returns_1m


@st.cache
def get_month_avg(data: pd.DataFrame, tickers: list) -> list:
    """Sums up all the values and calculate the average value in the month of each ticker.
        This function can probably be improved to calculate the average using numpy.

    Args:
        data: Dataframe with downloaded information of the tickers.
        tickers: List of the strings of the tickers to be fetched.

    Returns:
        List with the month average value of each ticker.
    """
    avg = []
    for ticker in tickers:
        rows = data[ticker]['Close']
        avg.append(rows.sum() / rows.count())
    return avg


def get_last_closes(data: pd.DataFrame, tickers: list) -> list:
    """Gets the value of the last close of each ticker.

    Args:
        data: Dataframe with downloaded information of the tickers.
        tickers: List of the strings of the tickers to be fetched.

    Returns:
        List with the value of the last close of each ticker.
    """
    last_closes = []
    data = data[::-1]  # inverts the list so the first value is the most recent one.
    for ticker in tickers:
        last_closes.append(data[ticker]['Close'].head(1).values[0])  # adds the last close value to the list
    return last_closes


def create_ts(tickers: list) -> dict:
    """Creates a time series with date and

    Args:
        tickers: List of the strings of the tickers to be fetched.

    Returns:
        A dictionary containing the close and 1 month return for each ticker
    """
    ts = {}
    columns_to_be_dropped = ['Open', 'High', 'Low', 'Adj Close', 'Volume']
    for ticker in tickers:
        data = yf.download(tickers=ticker, period='1y')
        data = data.drop(columns=columns_to_be_dropped)
        data['Return 1M'] = data['Close'].pct_change(periods=21, fill_method='bfill')
        ts[ticker] = data
    return ts


def get_marketcap(tickers: list) -> dict:
    """Gets the marketcap for each country of the tickers.

    Args:
        tickers: List of the strings of the tickers to be fetched.

    Returns:
        A dictionary where the keys are the countries and the values are dictionaries
        containing the marketcap and the count of each country for future calculation.
    """
    countries_mkcap = {}
    count = 0

    for ticker in tickers:
        count += 1
        info = yf.Ticker(ticker).info
        country = info['country']
        mkcap = info['marketCap']

        if country in countries_mkcap:  # if the country is already in the dictionary, just sum the market cap and
            # increase the counter
            current = countries_mkcap[country]['mkcap']
            countries_mkcap[country]['mkcap'] = current + mkcap
            countries_mkcap[country]['count'] += 1
        else:  # creates a sub dictionary and add it to the main dictionary containing the new country
            country_dict = {'mkcap': mkcap, 'count': 1}
            countries_mkcap[country] = country_dict

    countries_mkcap['total_count'] = count  # stores the total count of the market cap (10 in this project) for
    # future weighted average calculation
    return countries_mkcap


def get_10_last_prices(data: pd.DataFrame, tickers: list) -> dict:
    """Gets the 10 last close prices for each ticker.

    Args:
        data: DataFrame containing data about each ticker
        tickers: List of the strings of the tickers to be fetched.

    Returns:
        A dictionary where the key is the ticker name and the value is a list with the 10 last close values.
    """
    prices = {}
    data = data[::-1]  # inverts the list so the most recent closes are listed first.
    for ticker in tickers:
        prices[ticker] = data[ticker]['Close'].head(10).values.round(2)  # filters 10 rows and rounds the value.
    return prices


def country_statistics(mkcap: dict) -> dict:
    """Calculates the statistics for the marketcap of each country.

    Args:
        mkcap: Dictionary where the key is the country name and the value is a dictionary with the total marketcap
    and ticker count.

    Returns:
        A dictionary containing the statistics for each country.
    """
    statistics = {}
    total_count = mkcap.pop('total_count')  # retrieves values and remove from the dict

    for key, val in mkcap.items():
        statistics[key] = {'Symbols': val['count'], 'Weighted Average Price': val['mkcap'] * val['count'] / total_count}

    return statistics


def chart(ticker: str, ts: dict) -> None:
    """Draws a line chart with the specified ticker.

    Args:
        ticker: String of the user input.
        ts: Dictionary containing the timeseries information.
    """
    if ticker.upper() in tickers:  # if the ticker is listed, it creates the line chart
        st.line_chart(ts[ticker.upper()]['Close'], use_container_width=True)
    elif ticker == '':  # when the input is none
        st.warning("Please insert a ticker")
    else:  # when the input is not valid
        st.error("Invalid ticker name")


@st.cache
def load_data(df_data, headers):
    return pd.DataFrame(df_data, columns=headers).sort_values(by='Symbol')


@st.cache
def loadup() -> list:
    """Loads up and download all the tickers data and process it.
        Values are cached using the @st.cache notation for streamlit.

    Returns:
        List with the dataframe and timeseries that will be displayed in the dashboard.
    """
    try:
        data = yf.download(tickers=tickers, period='1mo', group_by='ticker', progress=False)
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

    newdict = get_10_last_prices(data, tickers)
    print(str(newdict))

    mkcap = get_marketcap(tickers)
    stats = country_statistics(mkcap)

    df2 = pd.DataFrame(stats)
    print(df2.transpose())

    ts = create_ts(tickers)

    return [df, ts]


if __name__ == '__main__':
    [df, ts] = loadup()  # cached data, so it does not process all the data again
    st.header("Dystematic Dashboard")
    st.dataframe(df, use_container_width=True)  # main dataframe

    st.subheader("Companies")
    selected = st.text_input(label="Insert ticker")  # input box

    st.subheader("Prices")
    chart(selected, ts)  # chart with the timeseries
