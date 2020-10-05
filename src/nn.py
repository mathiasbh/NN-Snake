
#from __future__ import absolute_import, division, print_function
import tensorflow as tf
import numpy as np




class NeuralNetwork(tf.keras.Model):
    """docstring for NeuralNetwork using TensorFlow """
	# Set Layers
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.in1 = tf.keras.layers.Dense(4, activation=tf.nn.relu)
        self.dense1 = tf.keras.layers.Dense(6, activation=tf.nn.relu)
        self.out = tf.keras.layers.Dense(3)

	# Forward pass
    def call(self, x):
        x = self.in1(x)
        x = self.dense1(x)
        x = self.out(x)
        # Manually updating weights
        x = tf.nn.softmax(x)
            
        return(x)
    

    def setWeights(self, inputmodel):
        self.set_weights(inputmodel.get_weights())
        return(self)

        
    def mutate(self, probability):
        wb = self.get_weights()
        
        # Weights
        for layer in range(0, len(wb), 2):
            # Mutate each neuron weight given probability
            for i in range(wb[layer].shape[0]):
                for j in range(wb[layer].shape[1]):
                    if np.random.rand() < probability:
                        wb[layer][i,j] = np.random.rand()*2 - 1
                        
        # Bias
        for layer in range(1, len(wb), 2):
            for i in range(wb[layer].size):
                if np.random.rand() < probability:
                    wb[layer][i] = np.random.rand()*2 - 1
                        
        self.set_weights(wb)
        return(self)
    
    
    
    def crossbreed(self, parent2):
        # Probability for inheriting from parent 1
        probability = np.random.rand()
        
        
        parent1_weights = self.get_weights()
        parent2_weights = parent2.get_weights()

        # Weight
        for layer in range(0, len(parent1_weights), 2):
            # Mutate each neuron weight given probability
            for i in range(parent1_weights[layer].shape[0]):
                for j in range(parent1_weights[layer].shape[1]):
                    if np.random.rand() > probability:
                        parent1_weights[layer][i,j] = parent2_weights[layer][i,j]

        # Bias
        for layer in range(1, len(parent1_weights), 2):
            # Mutate each neuron weight given probability
            for i in range(parent1_weights[layer].size):
                if np.random.rand() > probability:
                    parent1_weights[layer][i] = parent2_weights[layer][i]

        self.set_weights(parent1_weights)
            
        return(self)




