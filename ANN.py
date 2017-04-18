import numpy as np
class ANN(object):
    def __init__(self, num_inputs, num_hidden_nodes, num_outputs, weights):
        self.weights = weights
        self.num_inputs = num_inputs
        self.num_hidden_nodes = num_hidden_nodes
        self.num_outputs = num_outputs

         # list of weights (genome)
        num_hidden_weights = (num_inputs+1) * num_hidden_nodes

        #define layers:
        # 1) Between the input layer and the hidden layer
        # 2) Between the hidden layer and the output layer
        self.hidden_weights = np.array(weights[:num_hidden_weights]).reshape(num_hidden_nodes,num_inputs+1)
        self.output_weights = np.array(weights[num_hidden_weights:]).reshape(num_outputs,num_hidden_nodes+1)

    def activation(self, x):
        a = 4/(1+np.exp(-x))
        return a

    def evaluate(self,inputs):
        # Computes outputs from the ANN:
        # Output left_track and right_track
        inputs1 = np.insert(inputs, len(inputs), 1)
        vector1 = self.activation(np.dot(self.hidden_weights, inputs1))
        vector1 = np.insert(vector1, len(vector1), 1)
        np.reshape(vector1, (self.num_hidden_nodes+1, 1))
        vector2 = self.activation(np.dot(self.output_weights, vector1))
        return vector2.tolist()
