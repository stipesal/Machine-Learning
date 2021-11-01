"""
FYS-STK4155 @UiO, PROJECT II.
Feedforward neural network.
"""
import numpy as np

from sklearn.metrics import mean_squared_error as mse

from activations import identity, sigmoid, relu, leaky_relu
from weight_inits import xavier, kaiming


class Layer:
    def __init__(self, n_input, n_output, activation, weight_init):
        self.shape = (n_input, n_output)
        self.weight_init = weight_init
        self.activation = activation
        self.set_weights_and_biases()
        self.set_activation()

    def set_activation(self):
        try:
            self.act, self.d_act = globals()[self.activation]()
        except:
            raise ValueError(f"Activation {self.activation} not supported.")

    def set_weights_and_biases(self):
        try:
            self.weights, self.bias = globals()[self.weight_init](*self.shape)
        except:
            raise ValueError(f"Weight initialization {self.weight_init} not supported.")

    def forward(self, input):
        self.input = input
        self.z = self.input @ self.weights + self.bias
        return self.act(self.z)

    def update(self, reg_param, learning_rate):
        # Regularization term gradient.
        self.dW += 2 * reg_param * self.weights
        self.weights -= learning_rate * self.dW
        self.bias -= learning_rate * self.db


class Hidden(Layer):
    def __init__(self, n_input, n_output, activation, weight_init):
        super().__init__(n_input, n_output, activation, weight_init)

    def backward(self, upstream_delta):
        self.delta = upstream_delta * self.d_act(self.z)
        downstream_delta = self.delta @ self.weights.T
        self.dW = np.einsum('ij,ik->jki', self.input, self.delta).mean(axis=-1)
        self.db = self.delta.mean(axis=0)
        return downstream_delta


class Output(Layer):
    def __init__(self, n_input, n_output, activation, weight_init):
        super().__init__(n_input, n_output, activation, weight_init)
        self.weights = self.weights.squeeze()

    def backward(self, y_pred, y_true):
        error = 2 * (y_pred - y_true)
        self.delta = np.outer(error, self.weights)
        self.dW = (error * self.input.T).mean(axis=-1)
        self.db = error.mean(axis=-1)
        return self.delta


class FFNN:
    def __init__(self, p, reg_param, learning_rate):
        self.reg_param = reg_param
        self.learning_rate = learning_rate
        self.p = p
        self.set_layers()

    def set_layers(self):
        self.layers = []
        for i in range(len(self.p) - 2):
            self.layers.append(Hidden(self.p[i], self.p[i + 1], "relu", "xavier"))
        self.layers.append(Output(self.p[-2], self.p[-1], "identity", "xavier"))

    def predict(self, input):
        for layer in self.layers:
            input = layer.forward(input)
        return input

    def backprop(self, X, y):
        y_pred = self.predict(X)

        grad = self.layers[-1].backward(y_pred, y)
        for layer in reversed(self.layers[:-1]):
            grad = layer.backward(grad)
            layer.update(self.reg_param, self.learning_rate)

    def train(self, data, n_epochs, batch_size):
        X_train, _, y_train, _ = data

        n_batches = X_train.shape[0] // batch_size
        idx = np.arange(X_train.shape[0])

        self.hist = {"Train MSE": [], "Test MSE": []}
        for _ in range(n_epochs):
            np.random.shuffle(idx)
            for b in range(n_batches):
                batch = idx[b * batch_size: (b + 1) * batch_size]
                self.backprop(X_train[batch], y_train[batch])

            self.eval(data)

    def score(self, X, y):
        return mse(self.predict(X), y)

    def eval(self, data):
        X_train, X_test, y_train, y_test = data
        self.hist["Train MSE"].append(self.score(X_train, y_train))
        self.hist["Test MSE"].append(self.score(X_test, y_test))