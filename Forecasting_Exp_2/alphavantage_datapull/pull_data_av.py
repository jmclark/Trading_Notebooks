import pickle
import os
from termcolor import colored

from .load_tickers import *
from .pull_data_gen import *


def pull_stock_fund_intraday_av(tickers_df, ts, base_cache):
    data_cache = base_cache / "stock_fund/"
    # Create folder for today
    if not os.path.exists(data_cache):
        os.mkdir(data_cache)

    api_call_counter = get_api_call_counter(base_cache)

    counter_delta = 0
    for i, ticker in enumerate(tickers_df.ticker):

        if(api_call_counter == 500):
            print(colored("Reached the maximum api calls allowed for today", 'magenta'))
            break

        # Check if data already exists
        save_path_file = data_cache / (ticker + "_intraday_av.csv")
        if os.path.exists(save_path_file):
            print(colored("Data for " + ticker + " already exists", 'green'))
            continue

        # API call limit 5 / minute
        if((counter_delta % 5 == 0) and (counter_delta != 0)):
            print(colored("+ API call per min limit - Sleeping for one minute", 'yellow'))
            wait_1_minute()
            # time.sleep(60)

        # Pull data
        print("Pulling: ", ticker)
        try:
            data, meta_data = ts.get_intraday(
                ticker, interval="1min", outputsize='full')
        except ValueError:
            print(colored("- ValueError - Sleeping for one minute", 'red'))
            wait_1_minute()
            # time.sleep(60)
            try:
                data, meta_data = ts.get_intraday(
                    ticker, interval="1min", outputsize='full')
            except:
                print(colored(("- Exception - Could not pull " + ticker), 'red'))
                api_call_counter += 2
                counter_delta += 2
                continue

        save_path_file = data_cache / (ticker + "_intraday_av.csv")

        data.to_csv(save_path_file)

        api_call_counter += 1
        counter_delta += 1
        dump_api_call_counter(api_call_counter, base_cache)

    print(colored("*** Finished task ***", 'green'))
    print("Value of api_call_counter: ", api_call_counter)
    return


def pull_crypto_daily_av(tickers_df, cc, base_cache):
    data_cache = base_cache / "crypto/"
    # Create folder for today
    if not os.path.exists(data_cache):
        os.mkdir(data_cache)

    api_call_counter = get_api_call_counter(base_cache)

    counter_delta = 0
    for i, ticker in enumerate(tickers_df.ticker):

        if(api_call_counter == 500):
            print(colored("Reached the maximum api calls allowed for today", 'magenta'))
            break

        # Check if data already exists
        save_path_file = data_cache / (ticker + "_intraday_av.csv")
        if os.path.exists(save_path_file):
            print(colored("Data for " + ticker + " already exists", 'green'))
            continue

        # API call limit 5 / minute
        if((counter_delta % 5 == 0) and (counter_delta != 0)):
            print(colored("+ API call per min limit - Sleeping for one minute", 'yellow'))
            wait_1_minute()
            # time.sleep(60)

        # Pull data
        print("Pulling: ", ticker)
        try:
            data, meta_data = cc.get_digital_currency_daily(symbol=ticker, market='USD')
        except ValueError:
            print(colored("- ValueError - Sleeping for one minute", 'red'))
            wait_1_minute()
            # time.sleep(60)
            try:
                data, meta_data = cc.get_digital_currency_daily(symbol=ticker, market='USD')
            except:
                print(colored(("- Exception - Could not pull " + ticker), 'red'))
                api_call_counter += 2
                counter_delta += 2
                continue

        save_path_file = data_cache / (ticker + "_daily.csv")

        data.to_csv(save_path_file)

        api_call_counter += 1
        counter_delta += 1
        dump_api_call_counter(api_call_counter, base_cache)

    print(colored("*** Finished task ***", 'green'))
    print("Value of api_call_counter: ", api_call_counter)
    return