import pandas_datareader as pdr
import requests
import bs4 as bs
import pandas as pd
import quandl
import pickle
from os import listdir

# Pull Tickers
def sp500_tickers():
	resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
	soup = bs.BeautifulSoup(resp.text, 'lxml')
	table = soup.find('table', {'class': 'wikitable sortable'})
	tickers = []
	for row in table.findAll('tr')[1:]:
		ticker = row.findAll('td')[0].text
		tickers.append(ticker.rstrip('\n'))
		
	with open("Forecasting_Exp_1_Data\sp500_tickers.pickle","wb") as f:
		pickle.dump(tickers,f)
		
	return tickers

# Download S&P 500 Finance Data from Yahoo
def sp500_yahoo(tickers, start, end):
	yahoo_df = pd.DataFrame()
	date_string = '_from_' + str(start) + '_to_' + str(end)

	for i, ticker in enumerate(tickers):
		print("Collecting Yahoo data ", str(i+1), " of ", str(len(tickers)), ": ", ticker)
		try:
			ticker_data = pdr.get_data_yahoo(symbols=ticker, start=start, end=end)
			ticker_data['Ticker'] = ticker
			ticker_data.reset_index(inplace=True,drop=False)
			yahoo_df = yahoo_df.append(ticker_data)

		except:
			print("Exception")
			continue
			
	pickle_save_path = 'Forecasting_Exp_1_Data\sp500_yahoo' + date_string + '.pickle'
	with open(pickle_save_path,"wb") as f:
		pickle.dump(yahoo_df,f)
		
	excel_save_path = 'Forecasting_Exp_1_Data\sp500_yahoo' + date_string + '.xlsx'
	yahoo_df.to_excel(excel_save_path)

	return yahoo_df


# Collect Sentiment Data from Quandl
def get_sentiment(start, end):
	date_string = '_from_' + str(start) + '_to_' + str(end)

	sent_df = pd.DataFrame(quandl.get('AAII/AAII_SENTIMENT', start_date=start, end_date=end))
	sent_df.reset_index(inplace=True,drop=False)

	pickle_save_path = 'Forecasting_Exp_1_Data\sentiment' + date_string + '.pickle'
	with open(pickle_save_path,"wb") as f:
		pickle.dump(sent_df,f)
		
	excel_save_path = 'Forecasting_Exp_1_Data\sentiment' + date_string + '.xlsx'
	sent_df.to_excel(excel_save_path)
		
	return sent_df
	

# Update local datasets
def update_data(start, end, overwrite_all = 0, ticker_subset = None):
	'''
	Input: Dictionary of All Datasets
	Returns: Updated Data, or saved data
	'''
	date_string = '_from_' + str(start) + '_to_' + str(end)

	stored_files = listdir('Forecasting_Exp_1_Data')
	# print("Stored files: ", stored_files)

	data_dict = {}

	# Add sp500 tickers
	if ('sp500_tickers.pickle' in stored_files) and (overwrite_all == 0):
		print('Loading Tickers from file')
		with open('Forecasting_Exp_1_Data\sp500_tickers.pickle', 'rb') as f:
			data_dict['sp500_tickers'] = pickle.load(f)
	else:
		print('Pulling Tickers from web')
		data_dict['sp500_tickers'] = sp500_tickers()

	# Add yahoo data
	pickle_yahoo_path = "sp500_yahoo" + date_string + ".pickle"
	pickle_yahoo_dir_path = "Forecasting_Exp_1_Data\sp500_yahoo" + date_string + ".pickle"
	if (pickle_yahoo_path in stored_files) and (overwrite_all == 0):
		print('Loading Yahoo price data from file')
		with open(pickle_yahoo_dir_path, 'rb') as f:
			data_dict['sp500_yahoo'] = pickle.load(f)
	else:
		print('Pulling Yahoo price data from web')
		if ticker_subset is None:
			data_dict['sp500_yahoo'] = sp500_yahoo(data_dict['sp500_tickers'], start, end)
		else:
			data_dict['sp500_yahoo'] = sp500_yahoo(ticker_subset, start, end)


	# Add sentiment Data
	pickle_sent_path = "sentiment" + date_string + ".pickle"
	pickle_sent_dir_path = "Forecasting_Exp_1_Data\sentiment" + date_string + ".pickle"
	if (pickle_sent_path in stored_files) and (overwrite_all == 0):
		print('Loading sentiment data from file')
		with open(pickle_sent_dir_path, 'rb') as f:
			data_dict['sentiment'] = pickle.load(f)
	else:
		print('Pulling sentiment data from web')
		data_dict['sentiment'] = get_sentiment(start, end)
		
	return data_dict
