import numpy as np
class ANN(object):
    def __init__(self, num_inputs, num_hidden_nodes, num_outputs, weights, num_hidden_layers):
        self.weights = weights
        self.num_inputs = num_inputs
        self.num_hidden_layers = num_hidden_layers
        self.num_hidden_nodes = num_hidden_nodes
        self.num_outputs = num_outputs

         # list of weights (genome)
        num_hidden_weights = (num_inputs+1) * num_hidden_nodes

        #define layers:
        # 1) Between the input layer and the hidden layer
        # 2) Between the hidden layer and the output layer

        #print num_hidden_weights
        count = self.num_hidden_nodes[0]*(self.num_inputs+1)
        self.hidden_weights = []
        self.hidden_weights.append(np.array(weights[:count]).reshape(self.num_hidden_nodes[0], self.num_inputs+1))
        for i in range(1, num_hidden_layers):
            temp = np.array(weights[count:count+(self.num_hidden_nodes[i]*(self.num_hidden_nodes[i-1]+1))]).reshape(self.num_hidden_nodes[i], (self.num_hidden_nodes[i-1]+1))
            count += self.num_hidden_nodes[i]*(self.num_hidden_nodes[i-1]+1)
            self.hidden_weights.append(temp)
            print len(temp)

        #print self.hidden_weights
        # print len(np.array(weights[count:]))
        # print num_outputs*(self.num_hidden_nodes[-1]+1)
        self.output_weights = np.array(weights[count:]).reshape(num_outputs,self.num_hidden_nodes[-1]+1)

    def activation(self, x):
        a = 4/(1+np.exp(-x))
        return a

    def evaluate(self,inputs):
        # Computes outputs from the ANN:
        # Output left_track and right_track\
        inputs.append(1)
        vector = np.array(inputs)
        for i in range(0, self.num_hidden_layers):
            vector = self.activation(np.dot(vector, self.hidden_weights[i].transpose()))
            vector = np.append(vector, [1])

        #inputs1 = np.insert(inputs, len(inputs), 1)
        # print 'hi'
        # print self.hidden_weights
        #np.reshape(vector1, (self.num_hidden_nodes+1, 1))
        vectorout = self.activation(np.dot(vector,self.output_weights.transpose()))
        return vectorout.tolist()
