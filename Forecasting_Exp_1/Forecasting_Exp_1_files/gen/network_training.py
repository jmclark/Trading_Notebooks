from tensorflow.keras import Sequential, backend
from tensorflow.keras.callbacks import EarlyStopping

def train_Model(model, X_train, y_train, X_val, y_val, epochs, batch_size, early_stopping = 0):

	'''
	Train
	'''

	backend.clear_session()
	
	if early_stopping == 1:
		callback = EarlyStopping(monitor='val_loss', patience=2)
		history = model.fit(X_train, y_train, 
							epochs = epochs, 
							batch_size = batch_size,
							callbacks=[callback],
							validation_data = (X_val, y_val))
	elif len(y_val) > 0:
		history = model.fit(X_train, y_train, 
							epochs = epochs, 
							batch_size = batch_size,
							validation_data = (X_val, y_val))
	else: 
		history = model.fit(X_train, y_train, 
							epochs = epochs, 
							batch_size = batch_size)
	return model, history