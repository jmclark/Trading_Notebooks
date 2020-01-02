from sklearn.preprocessing import StandardScaler, MinMaxScaler
import numpy as np
import matplotlib.pyplot as plt

def evaluate_performance(model, train_data_raw, test_data_raw, train_data_sm_sc, test_data_sm_sc, seq_length):

	'''
	print("Raw training data")
	print(train_data_raw.head())
	print("Raw testing data")
	print(test_data_raw.head())
	'''

	past_x_days = train_data_raw.tail(seq_length)
	df = past_x_days.append(test_data_raw, ignore_index = True)

	#df = df.drop(['Date', 'Adj Close', 'Ticker'], axis = 1)

	scaler = MinMaxScaler()

	inputs = scaler.fit_transform(df)

	X_test = []
	y_test = []

	for i in range(seq_length, inputs.shape[0]):
		X_test.append(inputs[i-seq_length:i])
		y_test.append(inputs[i, 0])
		
	X_test, y_test = np.array(X_test), np.array(y_test)

	y_pred = model.predict(X_test)

	scale_arr = scaler.scale_
	min_arr = scaler.data_min_

	y_pred /= scale_arr[3] 
	y_pred += min_arr[3]

	y_test /= scale_arr[3]
	y_test += min_arr[3]


	# Visualising the results
	plt.figure(figsize=(14,5))
	plt.plot(y_test, color = 'red', label = 'Real')
	plt.plot(y_pred, color = 'blue', label = 'Predicted')
	plt.title('Prediction')
	plt.xlabel('Time')
	plt.ylabel('Price')
	plt.legend()
	plt.show()

	return y_pred
