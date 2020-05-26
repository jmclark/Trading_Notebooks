import pandas as pd
from pathlib import Path
import os
from IPython.display import clear_output
from IPython.display import display

import time

def load_sp100_tickers():
    ticker_path = r'D:\python_projects\Trading_Notebooks\Forecasting_Exp_2\tickers\sp100_tickers.xlsx'
    tickers_df = pd.read_excel(ticker_path, names = ['ticker', 'name'])
    return tickers_df

def load_physical_currency_tickers():
    ticker_path = r'D:\python_projects\Trading_Notebooks\Forecasting_Exp_2\tickers\physical_currency_list.csv'
    tickers_df = pd.read_csv(ticker_path, names = ['ticker', 'name'])
    return tickers_df

def load_digital_currency_tickers():
    ticker_path = r'D:\python_projects\Trading_Notebooks\Forecasting_Exp_2\tickers\digital_currency_list.csv'
    tickers_df = pd.read_csv(ticker_path, names = ['ticker', 'name'])
    return tickers_df

def load_digital_currency_top50_tickers():
    ticker_path = r'D:\python_projects\Trading_Notebooks\Forecasting_Exp_2\tickers\crypto_top50_av.xlsx'
    tickers_df = pd.read_excel(ticker_path, names = ['ticker', 'name'])
    return tickers_df

def open_single_intraday(ticker: str, data_cache):
    
    data_path = data_cache / "stock_fund" / (ticker + "_intraday_av.csv")
    # print("Opening path ", data_path)
    df = pd.read_csv(data_path)

    df['date'] =  pd.to_datetime(df['date'])
    df = df.sort_values(by='date').reset_index(drop = True)

    return df

def data_exists_single_intraday(ticker: str, data_cache) -> bool:
    return os.path.exists(data_cache / "stock_fund" / (ticker + "_intraday_av.csv"))

def wait_1_minute():
    number_of_elements = 60
    dh = display('', display_id=True)

    for i in range(number_of_elements + 1):
        time.sleep(1)   #Replace this with a real computation
        progress = i / number_of_elements
        bar_length = 20
        if isinstance(progress, int):
            progress = float(progress)
        if not isinstance(progress, float):
            progress = 0
        if progress < 0:
            progress = 0
        if progress >= 1:
            progress = 1

        block = int(round(bar_length * progress))

        text = "Progress: [{0}] {1:.1f}%".format( "#" * block + "-" * (bar_length - block), progress * 100)
        dh.update(text)

def ticker_inclusion(ticker_df_1, ticker_df_2):
    # Prints a list of tickers in 1 but not in 2
    # Ideally, ticker_df_1 is contained in ticker_df_2
    for i, ticker in enumerate(ticker_df_1.ticker):
        # print("Checking: ", ticker)
        if ticker_df_2.ticker[ticker_df_2.ticker.isin([ticker])].empty:
            print(ticker_df_1.name.iloc[i], " not in ticker_df_2")
    return