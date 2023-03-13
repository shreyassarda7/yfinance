import pickle
import pandas as pd


def get_index_constituents(index, bool_all = True):
    if bool_all:
        with open(r"C:\systematic\shru_strat\yfinance\{}\all_constituents.pkl".format(index), "rb") as fp:   # Unpickling
            index_constituents = pickle.load(fp)
    with open(r"C:\systematic\shru_strat\yfinance\{}\latest_constituents.pkl".format(index), "rb") as fp:   # Unpickling
        index_constituents = pickle.load(fp)
              
    return sorted([i for i in index_constituents if type(i) == str])

def get_stock_data(ticker, index = 'sp500', timeframe='1D'):
    return pd.read_csv(r"C:\systematic\shru_strat\yfinance\{}\{}\{}.csv".format(index, timeframe, ticker)).rename(columns={'Unnamed: 0': 'Datetime'}).set_index('Datetime')
    
    
def get_stock_data_without_index_axis(ticker, index = 'sp500', timeframe='1H'):
        if timeframe in ('1D', '1m') :
            return pd.read_csv(r"C:\systematic\shru_strat\yfinance\{}\{}\{}.csv"
                       .format(index, timeframe, ticker))
        return pd.read_csv(r"C:\systematic\shru_strat\yfinance\{}\{}\{}.csv"
                       .format(index, timeframe, ticker)).rename(columns={'Unnamed: 0': 'Timestamp'})

def get_stock_data_by_year(stock, index = 'sp500', required_years = 2013):
    
    """
    'rquired_years' is a list of years we want the data for stock.
    We can use range as well(e.g. range(2010, 2015) for years 2010-2014)
    """
    
    data = get_stock_data(stock, index = index, timeframe='1D')
    data['Date'] = pd.to_datetime(data['Date'])
    data = data.set_index
    
    data = get_stock_data('stock')
    data['Date'] = pd.to_datetime(data['Date'])
    data['year'] = pd. DatetimeIndex(data['Date']).year
    
    if type(required_years) == int:
        return data[data['year'] == required_years].drop('year', axis=1).set_index('Date')
    
    return data[data['year'].isin(required_years)].drop('year', axis=1).set_index('Date')

def add_yest_data(df, open_flag=True, high_flag=True, low_flag=True, close_flag=True):
    
    """
    All False values: open_flag=False, high_flag=False, low_flag=False, close_flag=False
    """
    
    df_to_add = pd.DataFrame()
    if open_flag:
        df_to_add['yest_open'] = df['Open'].shift(1)
    if high_flag:
        df_to_add['yest_high'] = df['High'].shift(1)
    if low_flag:
        df_to_add['yest_low'] = df['Low'].shift(1)
    if close_flag:
        df_to_add['yest_close'] = df['Close'].shift(1)

    return pd.concat([df, df_to_add], axis=1)

def add_day_before_data(df, open_flag=True, high_flag=True, low_flag=True, close_flag=True):
    
    """
    All False values: open_flag=False, high_flag=False, low_flag=False, close_flag=False
    """
    
    df_to_add = pd.DataFrame()
    if open_flag:
        df_to_add['day_before_open'] = df['Open'].shift(2)
    if high_flag:
        df_to_add['day_before_high'] = df['High'].shift(2)
    if low_flag:
        df_to_add['day_before_low'] = df['Low'].shift(2)
    if close_flag:
        df_to_add['day_before_close'] = df['Close'].shift(2)
    return pd.concat([df, df_to_add], axis=1)

def add_second_day_before_data(df, open_flag=True, high_flag=True, low_flag=True, close_flag=True):
    
    """
    All False values: open_flag=False, high_flag=False, low_flag=False, close_flag=False
    """
    
    df_to_add = pd.DataFrame()
    if open_flag:
        df_to_add['second_day_before_open'] = df['Open'].shift(3)
    if high_flag:
        df_to_add['second_day_before_high'] = df['High'].shift(3)
    if low_flag:
        df_to_add['second_day_before_low'] = df['Low'].shift(3)
    if close_flag:
        df_to_add['second_day_before_close'] = df['Close'].shift(3)
    return pd.concat([df, df_to_add], axis=1)

def add_sp500_vix(df):
    data = pd.DataFrame()
    data['vix'] = get_stock_data('^VIX', 'indices').set_index('Date')['Close']
    data = pd.concat([df, data], axis=1)
    return data.dropna(subset=['Close'])

def add_index(df, index = '^GSPC'):
    data = get_stock_data(index, 'indices').set_index('Date')[['Open', 'Close']].rename({'Open': 'index_open', 'Close': 'index_close'}, axis=1)
    data = pd.concat([df, data], axis=1)
    return data.dropna(subset=['Close'])