import pickle
import os
from termcolor import colored

from .load_tickers import *

def get_api_call_counter(base_cache):
    # Create API call counter for today
    api_call_counter_file_path = base_cache / "api_call_counter_file.pickle"

    if not os.path.exists(base_cache):
        os.mkdir(base_cache)

    if not os.path.exists(api_call_counter_file_path):
        api_call_counter = 0
        with open(api_call_counter_file_path, 'wb') as f:
            pickle.dump(api_call_counter, f)
    else:
        with open(api_call_counter_file_path, 'rb') as f:
            api_call_counter = pickle.load(f)

    print("Value of api_call_counter: ", api_call_counter)
    return api_call_counter


def dump_api_call_counter(api_call_counter, base_cache):
    api_call_counter_file_path = base_cache / "api_call_counter_file.pickle"

    with open(api_call_counter_file_path, 'wb') as f:
        pickle.dump(api_call_counter, f)
    return

