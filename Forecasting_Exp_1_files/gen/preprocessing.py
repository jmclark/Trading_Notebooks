from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pandas as pd
from math import floor
import numpy as np

def splitter(df, train_percent):

	df_length = df.shape[0]
	split_index = floor(train_percent * df_length)

	df_train = pd.DataFrame(df[0:split_index])
	df_test = pd.DataFrame(df[split_index:])


	return (df_train, df_test)

def smoother_scaler(train_data, test_data, EMA, gamma):

	"""
	train_data: [type: pandas DataFrame]
	"""
	train_data_sm_sc = pd.DataFrame()
	test_data_sm_sc = pd.DataFrame()

	for col in train_data.columns:
		scaler = MinMaxScaler()
		
		train_col = np.asarray(scaler.fit_transform(np.asarray(train_data[col]).reshape(-1, 1)))
		test_col = np.asarray(scaler.transform(np.asarray(test_data[col]).reshape(-1, 1)))
						
		for i in range(len(train_col)):
					EMA = gamma*train_col[i] + (1-gamma)*EMA
					train_col[i] = EMA
					
		train_col = train_col.reshape(-1)
		test_col = test_col.reshape(-1)
					
		train_data_sm_sc[col] = train_col
		test_data_sm_sc[col] = test_col


	return (train_data_sm_sc, test_data_sm_sc)