from agent.agent import *
from functions import *

data = dataset_loader()
data = data[:50]
window_size = 10
episodes = 100

batch_size = 32
data_samples = len(data) - 1

trader = AI_Trader(window_size)
trader.model.summary()

for episode in range(1, episodes + 1):
  
    print("Episode: {}/{}".format(episode, episodes))
  
    state = state_creator(data, 0, window_size + 1)
  
    total_profit = 0
    trader.inventory = []
  
    # for t in tqdm(range(data_samples)):
    for t in range(data_samples):
        print("\tt: ", t)
        
        action = trader.trade(state)
            
        next_state = state_creator(data, t+1, window_size + 1)
        reward = 0
    
        if action == 1: #Buying
            trader.inventory.append(data[t])
            print("AI Trader bought: ", stock_price_format(data[t]))
      
        elif action == 2 and len(trader.inventory) > 0: #Selling
            buy_price = trader.inventory.pop(0)
      
            reward = max(data[t] - buy_price, 0)
            total_profit += data[t] - buy_price
            print("AI Trader sold: ", stock_price_format(data[t]), " Profit: " + stock_price_format(data[t] - buy_price) )
      
        if t == data_samples - 1:
            print("\t\tDone")
            done = True
        else:
            done = False
      
        trader.memory.append((state, action, reward, next_state, done))
    
        state = next_state
    
        if done:
            print("########################")
            print("TOTAL PROFIT: {}".format(total_profit))
            print("########################")
    
        if len(trader.memory) > batch_size:
            trader.batch_trade(batch_size)
      
    if episode % 10 == 0:
        trader.model.save("ai_trader_{}.h5".format(episode))