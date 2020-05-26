import math
import pandas as pd
import numpy as np

'''
Two changes to make: 
1) Handle any stock from datapull
2) Return more than closing price (modify NN)
'''

def dataset_loader(stock_name="AMZN"):

    dataset = pd.read_csv("AMZN_intraday.csv")
    close = dataset['4. close']
  
    return close

def stock_price_format(n):
    if n < 0:
        return "- $ {0:2f}".format(abs(n))
    else:
        return "$ {0:2f}".format(abs(n))

def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def state_creator(data, timestep, window_size):
  
    starting_id = timestep - window_size + 1
  
    if starting_id >= 0:
        windowed_data = data[starting_id:timestep+1].reset_index(drop=True)
    else:
        windowed_data = -1*starting_id * [data[0]] + list(data[0:timestep+1])
    
    state = []
    for i in range(window_size - 1):
        state.append(sigmoid(windowed_data[i+1] - windowed_data[i]))
    
    return np.array([state])