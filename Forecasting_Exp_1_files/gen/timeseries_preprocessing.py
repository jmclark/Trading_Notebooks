import numpy as np
import copy

def ltsm_sequence_generator(train_data, seq_length, y_col):
	
	X_train = []
	y_train = []
	
	for i in range(seq_length, train_data.shape[0]):
		X_train.append(np.asarray(train_data.iloc[i-seq_length:i]))
		y_train.append(train_data.iloc[i][y_col])
	
	return (np.asarray(X_train), np.asarray(y_train))	
	
def join_timeseries(df_list, fill_nan_fwd = 1, snip_incomplete = 1):

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
	
def gen_diff(df, cols, period = 1):

	"""
	Generates '<col>_difference' columns, which for all column keys provided as a list represents the col[t] - col[t-period] values
	
	:param df: main DataFrame
	:type df: pd.DataFrame
	
	param cols: list of strings
	type cols: list of column names in df
	
	param period: the distance (timestep) used to calculate each difference
	type period: int
	"""
	
	df_mod = copy.deepcopy(df)
	
	for col in cols:
		diff_col_name = col + '_diff_' + str(period)
		df_mod[diff_col_name] = df[col].diff(periods = period)
		df_mod[diff_col_name] = df_mod[diff_col_name].shift(periods = -1*period) 

	
	return df_mod