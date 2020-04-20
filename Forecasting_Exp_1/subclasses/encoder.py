class Encoder(tf.keras.layers.Layer): # Encoder inherits the superclass .Layer 
	def __init__(self, intermediate_dim):
		# super() alone returns a temporary object of the superclass that then allows you to call that superclass’s methods.
		# Here, you’ve used super() to call the __init__() of the Rectangle class, allowing you to use it in the Square class without repeating code. 
		super(Encoder, self).__init__() 
		
		self.hidden_layer = tf.keras.layers.Dense(
			units = intermediate_dim,
			activation = tf.nn.relu,
			kernel_initializer = 'he_uniform'
		)
		
		self.output_layer = tf.keras.layers.Dense(
			units = intermediate_dim,
			activation = tf.nn.sigmoid
		)
		
	def call(self, input_features):
		activation = self.hidden_layer(input_features)
		return self.output_layer(activation)
