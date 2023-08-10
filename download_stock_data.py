import logging

logging.basicConfig(filename='yfinance.log', level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s', force=True)

# import libraries

import datetime
import pandas as pd
import yfinance as yf

from get_data import get_index_constituents

# sp500 = get_index_constituents('sp500')
# ftse250 = get_index_constituents('ftse250')
# ftse100 = get_index_constituents('ftse100')
# stoxx = get_index_constituents('stoxx')
# cac_40 = get_index_constituents('cac_40')
# russell = get_index_constituents('russell')
# dax = get_index_constituents('dax')
#
# aex = get_index_constituents('aex')
# asx = get_index_constituents('asx')
#
# ftsemib = get_index_constituents('ftsemib')
# ibexnr = get_index_constituents('ibexnr')
#
# indices = get_index_constituents('indices')
#
# crypto = get_index_constituents('crypto')
# fx = get_index_constituents('fx')

nifty50 = get_index_constituents('nifty50')
nifty500 = get_index_constituents('nifty500')
niftymidcap150 = get_index_constituents('niftymidcap150')
niftysmallcap250 = get_index_constituents('niftysmallcap250')

nifty_str_convert_dict = {"nifty50": nifty50,
                          "nifty500": nifty500,
                          "niftymidcap150": niftymidcap150,
                          "niftysmallcap250": niftysmallcap250}

# str_convert_dict = {"aex": aex,
#                     "asx": asx,
#                     "cac_40": cac_40,
#                     "crypto": crypto,
#                     "dax": dax,
#                     "stoxx": stoxx,
#                     "ftse100": ftse100,
#                     "ftse250": ftse250,
#                     "ftsemib": ftsemib,
#                     "fx": fx,
#                     "ibexnr": ibexnr,
#                     "indices": indices,
#                     "sp500": sp500,
#                     "russell": russell
#                     }


def get_hourly_data(stock):
    # to get ticker
    ticker = yf.Ticker(stock)

    # get data for last 730 days
    start = (datetime.date.today() - datetime.timedelta(729)).strftime("%Y-%m-%d")
    end = datetime.date.today().strftime("%Y-%m-%d")

    data = ticker.history(start=start, end=end, interval="1H")
    data.index.names = ['Timestamp']
    data = data.reset_index()

    if data.empty:
        logging.error(f'No hourly data for {stock} from {start} to {end}.')
        return pd.DataFrame()

    data['Date'] = data['Timestamp'].dt.date

    return data


def add_hourly_data(stock, index):
    stock_head = stock.split('.')[0]
    try:
        data = pd.read_csv(r".\{}\1H\{}.csv".format(index, stock_head), index_col=0)
        data['Date'] = pd.to_datetime(data['Date']).apply(lambda x: x.date())
        data_to_add = get_hourly_data(stock)
        last_date = data['Date'].iloc[-1]

        prev_data = data.loc[data['Date'] < last_date]
        new_data = data_to_add.loc[data_to_add['Date'] >= last_date]

        final_data = pd.concat([prev_data, new_data])

        final_data.to_csv(f"./{index}/1H/{stock_head}.csv", mode='w', header=True)
        logging.info(f"Updating hourly data for index: '{index}', stock: '{stock_head}'")
    except FileNotFoundError:
        """data = get_hourly_data(stock)
        data.to_csv(f"./{index}/1H/{stock_head}.csv", mode='w', header=True)"""
        logging.error(f"Hourly data not added for index: '{index}', stock: '{stock_head}'")
    return


def get_5_minutewise_data(stock):
    # to get ticker
    ticker = yf.Ticker(stock)

    # get data for last 60 days
    start = (datetime.date.today() - datetime.timedelta(59)).strftime("%Y-%m-%d")
    end = datetime.date.today().strftime("%Y-%m-%d")

    data = ticker.history(start=start, end=end, interval="5m")
    data.index.names = ['Timestamp']
    data = data.reset_index()

    if data.empty:
        logging.error(f'No 5 minutewise data for {stock} from {start} to {end}.')
        return pd.DataFrame()

    data['Date'] = data['Timestamp'].dt.date

    return data


def add_5_minutewise_data(stock, index):
    stock_head = stock.split('.')[0]
    try:
        data = pd.read_csv(r".\{}\5m\{}.csv".format(index, stock_head), index_col=0)
        data['Date'] = pd.to_datetime(data['Date']).apply(lambda x: x.date())
        data_to_add = get_5_minutewise_data(stock)
        last_date = data['Date'].iloc[-1]

        prev_data = data.loc[data['Date'] < last_date]
        new_data = data_to_add.loc[data_to_add['Date'] >= last_date]

        final_data = pd.concat([prev_data, new_data])

        final_data.to_csv(f"./{index}/5m/{stock_head}.csv", mode='w', header=True)
        logging.info(f"Updating 5 minutewise data for index: '{index}', stock: '{stock_head}'")
    except FileNotFoundError:
        """data = get_5_minutewise_data(stock)
        data.to_csv(f"./{index}/5m/{stock_head}.csv", mode='w', header=True)"""
        logging.error(f"5 minutewise data not added for index: '{index}', stock: '{stock_head}'")
    return


def get_minutewise_data(stock):
    # to get ticker
    ticker = yf.Ticker(stock)

    last_start_date = (datetime.datetime.today() - datetime.timedelta(days=29)).strftime("%Y-%m-%d")
    last_end_date = (datetime.datetime.today() - datetime.timedelta(days=28)).strftime("%Y-%m-%d")
    data = ticker.history(start=last_start_date, end=last_end_date, interval="1m")

    if data.empty:
        logging.error(f'No data for {stock} from {last_start_date} to {last_end_date}.')

    data.index.names = ['Timestamp']
    data = data.reset_index()

    for i in range(27, 0, -7):
        new_start_date = (datetime.datetime.today() - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        new_end_date = (datetime.datetime.today() - datetime.timedelta(days=i - 6)).strftime("%Y-%m-%d")
        data_to_add = ticker.history(start=new_start_date, end=new_end_date, interval="1m")

        if data_to_add.empty:
            logging.error(f'No data for {stock} from {new_start_date} to {new_end_date}.')
            continue

        data_to_add.index.names = ['Timestamp']
        data_to_add = data_to_add.reset_index()
        data = pd.concat([data, data_to_add], axis=0)

    if data.empty:
        logging.error(f'No data for {stock} from {last_start_date} to {new_end_date}.')
        return pd.DataFrame()

    data['Date'] = data['Timestamp'].dt.date

    return data


def add_minutewise_data(stock, index):
    stock_head = stock.split('.')[0]
    try:
        data = pd.read_csv(r".\{}\1m\{}.csv".format(index, stock_head), index_col=0)
        data['Date'] = pd.to_datetime(data['Date']).apply(lambda x: x.date())
        data_to_add = get_minutewise_data(stock)
        last_date = data['Date'].iloc[-1]

        prev_data = data.loc[data['Date'] < last_date]
        new_data = data_to_add.loc[data_to_add['Date'] >= last_date]

        final_data = pd.concat([prev_data, new_data])

        final_data.to_csv(f"./{index}/1m/{stock_head}.csv", mode='w', header=True)
        logging.info(f"Updating minutewise data for index: '{index}', stock: '{stock_head}'")
    except FileNotFoundError:
        """data = get_minutewise_data(stock)
        data.to_csv(f"./{index}/1m/{stock_head}.csv", mode='w', header=True)"""
        logging.error(f"Minutewise data not added for index: '{index}', stock: '{stock_head}'")
    return


if __name__ == '__main__':

    ### Download Nifty indices stock data

    for index, component in nifty_str_convert_dict.items():
        for ticker in component:
            # add_hourly_data(ticker, index)
            # add_5_minutewise_data(ticker, index)
            add_minutewise_data(ticker, index)

    ### Download Global indices stock data

    """for index, component in str_convert_dict.items():
        for ticker in component:
            add_hourly_data(ticker, index)
            add_5_minutewise_data(ticker, index)
            add_minutewise_data(ticker, index)"""

    ### Download currencies data

    """currencies = ['GBP', 'EUR', 'CHF', 'RMB', 'AUD', 'USD', 'CAD', '']
    for currency in currencies:
        if currency in ('USD', ''):
            continue
        for currency2 in currencies:
            if currency == currency2:
                continue
            index = 'fx'
            ticker = currency + currency2 + '=X'
    
            print(ticker)
    
            add_hourly_data(ticker, index)
            add_5_minutewise_data(ticker, index)
            add_minutewise_data(ticker, index)"""

