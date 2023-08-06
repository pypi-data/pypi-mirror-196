import numpy as np


 
# Dense layer
class Layer_Dense:
    # Layer initialization
    def __init__(self, n_inputs, n_neurons) :
        # Initialize weights and biases
        self.weights = 0.01 * np.random.randn(n_inputs, n_neurons) 
        self.biases = np.zeros((1, n_neurons))
        # Forward pass
    def forward(self, inputs) :
        # Remember input values
        self.inputs = inputs
        # Calculate output values from inputs, weights and biases 
        self.output = np.dot(inputs, self.weights) + self.biases
    # Backward pass
    def backward(self, dvalues):
        # Gradients on parameters
        self.dweights = np.dot(self.inputs.T, dvalues) 
        self.dbiases = np.sum(dvalues, axis= 0, keepdims=True) # Gradient on values
        self.dinputs = np.dot(dvalues, self.weights.T)
        
    # ReLU activation
class Activation_ReLU:
    # Forward pass
    def forward(self, inputs) :
        # Remember input values
        self.inputs = inputs
        # Calculate output values from inputs 
        self.output = np.maximum(0, inputs)
        # Backward pass
    def backward(self, dvalues):
        # Since we need to modify original variable, # let's make a copy of values first 
        self.dinputs = dvalues.copy()
        # Zero gradient where input values were negative 
        self.dinputs[self.inputs <= 0] = 0
        
# Softmax activation
class Activation_Softmax:
    # Forward pass
    def forward(self, inputs) :
        # Remember input values 
        self.inputs = inputs
        # Get unnormalized probabilities
        exp_values = np.exp(inputs - np.max(inputs, axis=1,keepdims=True))
        probs=exp_values/np.sum(exp_values,axis=1,keepdims=True)
        self.output=probs
        
    # Backward pass
    def backward(self, dvalues):
        # Create uninitialized array 
        self.dinputs = np.empty_like(dvalues)
        # Enumerate outputs and gradients
        for index, (single_output, single_dvalues) in enumerate(zip(self.output, dvalues)):
            # Flatten output array
            single_output = single_output.reshape(-1, 1)
            # Calculate Jacobian matrix of the output and matrix of 1st order partial derivatives
            jacobian_matrix = np.diagflat(single_output) - \
                                          np.dot(single_output, single_output.T)
            # Calculate sample-wise gradient
            # and add it to the array of sample gradients 
            self.dinputs[index] = np.dot(jacobian_matrix,single_dvalues)

                                                    

# Softmax classifier - combined Softmax activation
# and cross-entropy loss for faster backward step
class Activation_Softmax_Loss_CategoricalCrossentropy():
    # Creates activation and loss function objects 
    def __init__(self):
        self.activation = Activation_Softmax()
        self.loss = Loss_CategoricalCrossentropy()
    # Forward pass
    def forward(self, inputs, y_true):
        # Output layer's activation function 
        self.activation.forward(inputs)
        # Set the output
        self.output = self.activation.output
        # Calculate and return loss value
        return self.loss.calculate(self.output, y_true)
    # Backward pass
    def backward(self, dvalues, y_true):
        # Number of samples 
        samples = len(dvalues)
        # If labels are one-hot encoded, # turn them into discrete values 
        if len(y_true.shape) == 2:
            y_true = np.argmax(y_true, axis= 1)
        # Copy so we can safely modify 
        self.dinputs = dvalues.copy()
        # Calculate gradient 
        self.dinputs[range(samples), y_true] -= 1 # Normalize gradient
        self.dinputs = self.dinputs / samples


import numpy as np

class Loss:
    # Calculates the data and regularization losses # given model output and ground truth values 
    def calculate(self, output, y):
        # Calculate sample losses 
        sample_losses = self.forward(output, y)
        # Calculate mean loss
        data_loss = np.mean(sample_losses)
        # Return loss 
        return data_loss  

class Loss_BinaryCrossentropy(Loss):
    def forward(self, y_pred, y_true):
        # Clip data to prevent division by 0
        epsilon = 1e-12
        y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
        # Calculate sample-wise loss
        sample_losses = -(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
        # Calculate mean loss
        sample_losses = np.mean(sample_losses, axis=-1)
        # Return loss
        return sample_losses
    
    def backward(self, dvalues, y_true):
        # Clip data to prevent division by 0
        epsilon = 1e-12
        clipped_dvalues = np.clip(dvalues, epsilon, 1 - epsilon)
        # Gradient on dinputs
        self.dinputs = -(y_true / clipped_dvalues - (1 - y_true) / (1 - clipped_dvalues)) / y_true.shape[0]
        
class Activation_Sigmoid_Loss_BinaryCrossentropy:
    
    def forward(self, inputs, y_true):
        self.inputs = inputs
        self.output = self.sigmoid(inputs)
        self.y_true = y_true.reshape(-1, 1)
        n_samples = len(self.output)

        # Calculate and return the binary cross-entropy loss
        self.loss = Loss_BinaryCrossentropy()
        return self.loss.calculate(self.output, self.y_true)
    
    def backward(self, dvalues, y_true):
        self.loss.backward(dvalues, self.y_true)
        self.dinputs = self.loss.dinputs * self.sigmoid_derivative(self.inputs)
        return self.dinputs
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def sigmoid_derivative(self, x):
        return self.sigmoid(x) * (1 - self.sigmoid(x))

class Optimizer_Adam:
    def __init__(self, learning_rate=0.001, decay=0., epsilon=1e-7, beta_1=0.9, beta_2=0.999):
        self.learning_rate = learning_rate
        self.current_learning_rate = learning_rate
        self.decay = decay
        self.iterations = 0
        self.epsilon = epsilon
        self.beta_1 = beta_1
        self.beta_2 = beta_2

    def pre_update_params(self):
        if self.decay:
            self.current_learning_rate = self.learning_rate * (1. / (1. + self.decay * self.iterations))

    def update_params(self, layer):
        if not hasattr(layer, 'weight_cache'):
            layer.weight_momentums = np.zeros_like(layer.weights)
            layer.weight_cache = np.zeros_like(layer.weights)
            layer.bias_momentums = np.zeros_like(layer.biases)
            layer.bias_cache = np.zeros_like(layer.biases)

        layer.weight_momentums = self.beta_1 * layer.weight_momentums + (1 - self.beta_1) * layer.dweights
        layer.bias_momentums = self.beta_1 * layer.bias_momentums + (1 - self.beta_1) * layer.dbiases

        weight_momentums_corrected = layer.weight_momentums / (1 - self.beta_1 ** (self.iterations + 1))
        bias_momentums_corrected = layer.bias_momentums / (1 - self.beta_1 ** (self.iterations + 1))

        layer.weight_cache = self.beta_2 * layer.weight_cache + (1 - self.beta_2) * layer.dweights ** 2
        layer.bias_cache = self.beta_2 * layer.bias_cache + (1 - self.beta_2) * layer.dbiases ** 2

        weight_cache_corrected = layer.weight_cache / (1 - self.beta_2 ** (self.iterations + 1))
        bias_cache_corrected = layer.bias_cache / (1 - self.beta_2 ** (self.iterations + 1))

        layer.weights += -self.current_learning_rate * weight_momentums_corrected / (np.sqrt(weight_cache_corrected) + self.epsilon)
        layer.biases += -self.current_learning_rate * bias_momentums_corrected / (np.sqrt(bias_cache_corrected) + self.epsilon)

    def post_update_params(self):
        self.iterations += 1



