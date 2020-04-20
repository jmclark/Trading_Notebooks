from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pandas as pd
from math import floor
import numpy as np

def splitter(df, train_percent, val_percent):

	df_length = df.shape[0]
	split_index_0 = floor(train_percent * df_length)
	split_index_1 = floor((train_percent + val_percent) * df_length)
	
	df_train = pd.DataFrame(df[0:split_index_0])
	df_val = pd.DataFrame(df[split_index_0:split_index_1])
	df_test = pd.DataFrame(df[split_index_1:])

	return (df_train, df_val, df_test)

def smoother_scaler(train_data, val_data, test_data, EMA, gamma):

	"""
	train_data: [type: pandas DataFrame]
	"""
	
	train_data_sm_sc = pd.DataFrame()
	val_data_sm_sc = pd.DataFrame()
	test_data_sm_sc = pd.DataFrame()

	if val_data.shape[0] == 0:
		val = 0
	else: 
		val = 1
	
	for col in train_data.columns:
		scaler = MinMaxScaler()
		
		train_col = np.asarray(scaler.fit_transform(np.asarray(train_data[col]).reshape(-1, 1)))
		if val: val_col = np.asarray(scaler.transform(np.asarray(val_data[col]).reshape(-1, 1)))
		test_col = np.asarray(scaler.transform(np.asarray(test_data[col]).reshape(-1, 1)))
						
		for i in range(len(train_col)):
			EMA = gamma*train_col[i] + (1-gamma)*EMA
			train_col[i] = EMA
					
		train_col = train_col.reshape(-1)
		if val: val_col = val_col.reshape(-1)
		test_col = test_col.reshape(-1)
					
		train_data_sm_sc[col] = train_col
		if val: val_data_sm_sc[col] = val_col
		test_data_sm_sc[col] = test_col

	return (train_data_sm_sc, val_data_sm_sc, test_data_sm_sc)