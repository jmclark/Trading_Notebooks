import numpy as np
from tensorflow.keras.activations import relu, tanh, exponential, softmax
from tensorflow.keras import Sequential, backend
from tensorflow.keras.layers import Dense, LSTM, Dropout, Flatten, TimeDistributed
from tensorflow.keras.utils import plot_model
import pydot
import graphviz 

def build_NN(train_data, batch_size, dropout):

	'''
	Define Model
	'''

	regressior = Sequential()

	input_shape = (train_data.shape[1], train_data.shape[2])
	regressior.add(LSTM(units = 64, activation = 'tanh', return_sequences = True, input_shape = input_shape))
	regressior.add(Dropout(dropout))

	regressior.add(LSTM(units = 128, activation = 'tanh', return_sequences = False))
	regressior.add(Dropout(dropout))

	# regressior.add(LSTM(units = 40, activation = relu, return_sequences = True))
	# regressior.add(Dropout(dropout))

	# regressior.add(Flatten())

	regressior.add(Dense(units=1, activation = 'tanh'))

	regressior.summary()

	# plot_model(regressior, "plot_model.png")

	return regressior

def model_mixer(train_data, batch_size, dropout, activation_case, layer_case, units_case):

	'''
	Composed of four layers (excluding posterior Flatten and Dense layers) up to four Dense or up to 
	'''	

	model = Sequential()

	input_shape = (train_data.shape[1], train_data.shape[2])

	
	activation_dict = {
		0: 'relu',
		1: 'tanh',
		2: 'softmax',
		3: 'exponential'
	}
	
	units_dict = {
		0: 40,
		1: 60,
		2: 80,
		3: 100,
		4: 120
	}
	
	first_layer_dict = {
		0: 'model.add(LSTM(units = {}, activation = {}, return_sequences = True, input_shape = input_shape))',
		1: 'model.add(TimeDistributed(Dense(units={}, activation = {}), input_shape = input_shape))'
	}
	
	second_layer_dict = {
		0: 'model.add(LSTM(units = {}, activation = {}, return_sequences = True))',
		1: 'model.add(TimeDistributed(Dense(units={}, activation = {})))'
	}
	
	third_layer_dict = {
		0: 'model.add(LSTM(units = {}, activation = {}, return_sequences = True))',
		1: 'model.add(TimeDistributed(Dense(units={}, activation = {})))',
		2: None
	}
	
	# Add first layer
	first_layer = first_layer_dict.get(layer_case[0])
	first_layer = first_layer.format(units_dict.get(units_case[0]), activation_dict.get(activation_case))
	eval(first_layer)
	model.add(Dropout(dropout))

	# Add second layer
	second_layer = second_layer_dict.get(layer_case[1])
	second_layer = second_layer.format(units_dict.get(units_case[1]), activation_dict.get(activation_case))
	eval(second_layer)
	model.add(Dropout(dropout))

	# Add third layer
	third_layer = third_layer_dict.get(layer_case[2])
	if third_layer is not None:
		third_layer = third_layer.format(units_dict.get(units_case[2]), activation_dict.get(activation_case))
		eval(third_layer)
		model.add(Dropout(dropout))


	# Add Flatten and Dense layers to all Models
	# model.add(Flatten())
	model.add(Dense(units=1))
	
	model.summary()	
	
	return model

def add_Optimizer(model):

	'''
	Optimizer
	'''
	model.compile(optimizer='adam', loss = 'mean_squared_error')

	return model

def save_model(model, filepath):
	model.save(
	filepath,
	overwrite=True,
	include_optimizer=True,
	save_format=None,
	signatures=None,
	options=None
	)