# Based on YouTube: https://www.youtube.com/watch?v=_O4T5Vjmgeo&t=1s
# Based on GitHub: https://gist.github.com/arsalanaf/d10e0c9e2422dba94c91e478831acb12

from btgym import BTgymEnv
import IPython.display as Display
import PIL.Image as Image
from gym import spaces

import gym
import numpy as np
import random

from keras.models import Sequential, load_model
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.recurrent import LTSM
from keras.optimizers import RMSprop, Adam


from collections import deque

class DQN:
    def __init__(self, env):
        self.env = env
        self.memory = deque(maxlen=20000)
        self.gamma = 0.85
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.005
        self.tau = 0.125
        
        self.model = self.create_model()
        self.target_model = self.create_model()
        
    def create_model(self):
        model = Sequential()
        
        '''
        model.add(Dense(24, input_dim=state_shape[1], activation="relu"))
        model.add(Dense(48, activation="relu"))
        model.add(Dense(24, activation="relu"))
        model.add(Dense(self.env.action_space.n))
        model.compile(loss="mean_squared_error", optimier=Adam(lr=self.learning_rate))
        '''
        
        model.add(LSTM(64, input_shape=(4, 1), 
        # return_sequences=True,
        stateful=False))
        
        model.add(Dropout(0.5))
        
        model.add(Dense(self.env.action_space.n, init='lecun_uniform'))
        model.add(Activation('linear'))
        
        rms = RMSprop()
        adam = Adam()
        model.compile(loss='mose', optimizer=adam)
        
        return model
        
    def act(self, state):
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)
        
        if np.random.random() < self.epsilon:
            return self.env.action_space.sample()
        return np.argmax(self.model.predict(state)[0])
        
    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i] * self.tau + target_weights[i] * (1 - self.tau)
        self.target_model.set_weights(target_weights)
        
    def save_model(self, fn):
        self.model.save(fn)
        
    def show_rendered_image(self, rgb_array):
        Display.display(Image.fromarray(rgb_array))
        
    def render_all_modes(self, env):
        for mode in self.env.metadata['render.modes']:
            print('[{}] mode:'.format(mode))
            self.show_rendered_image(self.env.render(mode))
            
            
def main():
    env = BTgymEnv(filename='fix',
                    state_shape={'raw_state':spaces.Box(low=-100, high=100,shape=(30,4))},
                    skip_frames=5,
                    start_cash=100000,
                    broker_commission=0.02,
                    fixed_stake=100,
                    drawdown_call = 90,
                    render_ylabel='Price Lines',
                    render_size_episode=(12,8),
                    render_size_human=(8,3.5),
                    render_size_state=(10,3.5),
                    render_dpi=75,
                    verbose=0,)
                    
    gamma = 0.9
    epsilon = 0.95
    
    trials = 100
    trial_len = 1000
    
    dqn_agent = DQN(env=env)
    steps = []
    for trial in range(trials):
        cur_state = np.array(list(env.reset().items())[0][1])
        cur_state = np.reshape(cur_state, (30,4,1))
        for step in range()trial_len:
            action = dqn_agent.act(cur_state)
            new_state, reward, done, _ = env.step(action)
            reward = reward*10 if not done else -10
            new_state = list(new_state.items())[0][1]
            new_state = np.reshape(new_state, (30,4,1,))
            dqn_agent.target_train()
            
            cur_state = new_state 
            if done:
                break
        print("Completed trial #{}".format(trial))
        dqn_agent.render_all_modes(env)
        dqn_agent.save_model("model.model".format(trial))
            
if __name__ == "__main__":
    main()
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        