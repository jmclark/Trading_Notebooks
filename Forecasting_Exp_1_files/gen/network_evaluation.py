from sklearn.preprocessing import StandardScaler, MinMaxScaler
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from .timeseries_preprocessing import ltsm_sequence_generator

def evaluate_performance(model, train_data_raw, test_data_raw, train_data_sm_sc, 
							test_data_sm_sc, seq_length, y_col):

	past_x_days = train_data_raw.tail(seq_length)
	df = past_x_days.append(test_data_raw, ignore_index = True)

	scaler = MinMaxScaler()

	inputs = scaler.fit_transform(df)
	
	# print(inputs.shape)
	
	inputs_df = pd.DataFrame()
	
	# print(train_data_raw.columns)
	
	for col in range(inputs.shape[1]):
		# print(train_data_raw.columns[col])
		# print(type(train_data_raw.columns[col]))
		inputs_df[train_data_raw.columns[col]] = inputs[:, col]
	
	# print("shapes ", df.shape, inputs.shape, inputs_df.shape)
	
	scale_index = train_data_raw.columns.get_loc(y_col)

	'''
	X_test = []
	y_test = []

	for i in range(seq_length, inputs.shape[0]):
		X_test.append(inputs[i-seq_length:i])
		y_test.append(inputs[i, 0])
		
	X_test, y_test = np.array(X_test), np.array(y_test)	
	'''

	X_test, y_test = ltsm_sequence_generator(inputs_df, seq_length, y_col)

	y_pred = model.predict(X_test).transpose()[0]

	scale_arr = scaler.scale_
	min_arr = scaler.data_min_

	y_pred /= scale_arr[scale_index] 
	y_pred += min_arr[scale_index]

	y_test /= scale_arr[scale_index]
	y_test += min_arr[scale_index]

	# Visualizing the prediction results
	plt.figure()
	fig, axs = plt.subplots(2, 1, figsize=(14,8))
	axs[0].plot(y_test, color = 'red', label = 'Real')
	axs[0].plot(y_pred, color = 'blue', label = 'Predicted')
	axs[0].set_title('Prediction')
	axs[0].set_xlabel('Time')
	axs[0].set_ylabel('Price')
	axs[0].legend()	
	
	plt.subplots_adjust(hspace = 0.5)
	# Visualizing autocorrelation

	x_corr = signal.correlate(y_test, y_pred, mode='full')
		
	horiz = np.array(range(x_corr.shape[0]))

	horiz -= y_test.shape[0]

	axs[1].plot(horiz, x_corr)
	axs[1].set_title('Cross-correlation')
	x_corr_max_x = np.argmax(x_corr) - y_test.shape[0]
	x_corr_max_y = x_corr.max()
	

	axs[1].plot([x_corr_max_x], [x_corr_max_y], marker='o', color='r',
		label=('lag: '+str(x_corr_max_x))) # 

	axs[1].legend()
		
	plt.show()
	
	return y_pred, fig
