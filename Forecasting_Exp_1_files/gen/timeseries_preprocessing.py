import numpy as np

def ltsm_sequence_generator(train_data, seq_length):

	train_data = np.asarray(train_data)

	X_train = []
	y_train = []
	for i in range(seq_length, train_data.shape[0]):
		X_train.append(train_data[i-seq_length:i])
		y_train.append(train_data[i, 0])
		
	return (np.asarray(X_train), np.asarray(y_train))
	
def join_timeseries(df_list, fill_nan_fwd = 0, snip_incomplete = 0):

	"""
	Join timeseries dataframes

	Positional arguments: 
	df_list -- [list] of [DataFrames]: to be joined  

	Keyword arguments:
	fill_nan_fwd -- [int]: fill NaN rows in joined dataframe by pulling non-NaN data 
					   forward until next non-NaN entry per column
					   
	snip_head -- [int]: delete (oldest) rows that represent incomplete features. Only works if fill_nan_fwd == 1
	"""

	if len(df_list) == 1:
		return df_list[0]
	else:
		df_joined = df_list[0]
		for df in df_list[1:]:
			df_joined = df_joined.merge(df, how='outer', on='Date', sort=True) 
		
		
	if fill_nan_fwd != 0:
		df_joined.fillna(method='ffill', inplace=True)    

		if snip_incomplete != 0 :
			df_joined.dropna(inplace=True)
			df_joined.reset_index(inplace=True, drop=True)

	return df_joined