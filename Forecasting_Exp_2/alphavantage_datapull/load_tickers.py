import pandas as pd
from pathlib import Path
import os

def load_sp100_tickers():
    ticker_path = r'D:\python_projects\trading_projects\forecasting_nn\sp100_tickers.xlsx'
    tickers_df = pd.read_excel(ticker_path, names = ['ticker', 'name'])
    return tickers_df

def open_single_intraday(ticker: str, data_cache):
    
    data_path = data_cache / (ticker + "_intraday.csv")
    print("Opening path ", data_path)
    df = pd.read_csv(data_path)

    df['date'] =  pd.to_datetime(df['date'])
    df = df.sort_values(by='date').reset_index(drop = True)
    df['date'] =  pd.to_datetime(df['date'])

    return df

def data_exists_single_intraday(ticker: str, data_cache) -> bool:
    return os.path.exists(data_cache / (ticker + "_intraday.csv"))
