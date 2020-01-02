import numpy as np
import matplotlib.pyplot as plt

def evaluate_model_AA001_day_ahead(y_pred, y_test, y_train, trade_percentage):
        
    y_pred = list(y_pred)
    y_test = list(y_test)
    y_train = list(y_train)

    '''
    - For each day, trade [trade_percentage] of initial capital
    - Given a day's predicted close price, if it is above the previous day's close price (current day open price),
      buy a position worth [trade_percentage] % of the current portfolio value 
      
    - Plot single day and cumulative percentage returns vs time
    
    '''
    
    # y_pred start at day 0 of test
    # y_test starts at day -1 of test (last day of train)
    # cumulative_percentages represents time series of portfolio value wrt trade_percentage
    # single_day_percentages, single_day_pred_changes are raw changes
    
    single_day_percentages = []
    single_day_pred_changes = []
    cumulative_percentages = [1]
    
    initial_capital = 1
    sum_percent_trading_error = 0
    
    # Add last value of training set to 
    y_test = np.insert(y_test, 0, y_train[-1:], axis=0)
    
    for i, pred in enumerate(y_pred):
        single_day_pred_changes.append((pred - y_test[i]) / y_test[i])

        if pred > y_test[i]: # Predicting that the stock will go 'up'
            single_day_change = np.float64((y_test[i + 1] - y_test[i]) / y_test[i]) 
            predicted_change = np.float64((pred - y_test[i]) / y_test[i])
                    
            single_day_percentages.append(single_day_change)
            cumulative_percentages.append(cumulative_percentages[i]*(1 + (single_day_change)*(trade_percentage)))
                        
            sum_percent_trading_error += abs(single_day_change - predicted_change)
            
        else:
            single_day_percentages.append(0)
            cumulative_percentages.append(cumulative_percentages[i])
            
            
    sum_percent_trading_error /= len(y_pred)
    
    cumulative_percentages = cumulative_percentages[1:]
    
    fig, axs = plt.subplots(figsize=(14,5))
    
    axs.plot(single_day_percentages, c = 'tab:orange')
    axs.plot(single_day_pred_changes, c = 'tab:red')
    axs1 = axs.twinx() 
    axs1.plot(cumulative_percentages, c = 'tab:blue')
    
    return single_day_percentages, single_day_pred_changes, cumulative_percentages, sum_percent_trading_error