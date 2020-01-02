from tensorflow.keras import Sequential, backend


def train_Model(model, X_train, y_train, epochs, batch_size):

	'''
	Train
	'''

	backend.clear_session()

	history = model.fit(X_train, y_train, 
						epochs = epochs, 
						batch_size = batch_size)
    
	return model, history