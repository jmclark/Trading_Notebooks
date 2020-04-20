'''
Reference: https://towardsdatascience.com/implementing-an-autoencoder-in-tensorflow-2-0-5e86126e9f7
Implementing an Autoencoder in TensorFlow 2.0 by Abien Fred Agarap
'''

class Autoencoder(tf.keras.Model):
	def __init__(self, intermediate_dim, original_dim):
		super(Autoencoder, self).__init__()
		self.encoder = Encoder(intermediate_dim = intermediate_dim)
		self.decoder = Decoder(intermediate_dim = intermediate_dim,
							   original_dim = original_dim)
							   
	def call(self, input_features):
		code = self.encoder(input_features)
		reconstructed = self.decoder(code)
		return reconstructed