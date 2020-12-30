import numpy as np
import matplotlib.pyplot as plt

from utils import sigmoid, relu, tanh, mse


class NeuralNetwork:
    def __init__(self, layers, eta, output_shape=(1, 1)):
        self.output_layer = np.zeros(output_shape)
        self.layers = []
        self.eta = eta

        for layer, next_layer in zip(layers[0:-1], layers[1:]):
            self.layers.append(Layer(layer['fn'], (next_layer['size'], layer['size'])))

        self.layers.append(
            Layer(layers[-1]['fn'], (output_shape[0], layers[-1]['size']))
        )

    def feed_forward(self, x):
        self.layers[0].values = x

        for layer, next_layer in zip(self.layers[0:-1], self.layers[1:]):
            next_layer.values = layer.fn(np.dot(layer.values, layer.weights.T))

        self.output_layer = self.layers[-1].fn(
            np.dot(self.layers[-1].values, self.layers[-1].weights.T)
        )

    def back_propagation(self, y):
        delta_list = []

        delta = (y - self.output_layer) * self.layers[-1].fn_prim(self.output_layer)
        delta_list.append(self.eta * np.dot(delta.T, self.layers[-1].values))

        for layer, previous_layer in zip(reversed(self.layers[0:-1]), reversed(self.layers[1:])):
            delta = layer.fn_prim(previous_layer.values) * np.dot(delta, previous_layer.weights)
            delta_list.append(self.eta * np.dot(delta.T, layer.values))

        for layer, weight in zip(self.layers, reversed(delta_list)):
            layer.weights += weight

    def train(self, X, expected_output, i):
        for _ in range(i):
            self.feed_forward(X)
            self.back_propagation(expected_output)


class Layer:
    def __init__(self, activate_function, shape):
        self.fn, self.fn_prim = activate_function
        self.weights = np.random.standard_normal(shape)
        self.values = np.zeros((shape[1]))


def run_tests(test):
    network = NeuralNetwork(test['layers'], test['eta'])
    d = test['x']/max(test['x'])
    i = test['fn'](d)

    X = np.reshape(d, (len(d), 1))
    y = np.reshape(i, (len(i), 1))

    b = test['b']/max(test['b'])
    b_i = test['fn'](b)
    _X = np.reshape(b, (len(b), 1))

    fig = plt.figure()
    axs = fig.add_subplot(2, 1, 1)
    axs.set_title(test['name'])
    axs.scatter(d, y, color='black')

    axs2 = fig.add_subplot(2, 1, 2)
    axs2.set_title('Approx')

    for i in range(51):
        network.train(X, y, 100)
        network.feed_forward(_X)
        axs2.clear()
        axs2.set_xlabel(
            f"{i*100} iteracji\nMSE: {mse(b_i, network.output_layer.flatten())}")
        axs2.scatter(b, network.output_layer.flatten(), color='orange')
        plt.pause(0.02)
    plt.show()


tests = [
    {
        'name': 'Parabola, 2 layery',
        'layers': [
            {'fn': sigmoid, 'size': 1},
            {'fn': tanh, 'size': 10},
        ],
        'x': np.linspace(-50, 50, 26),
        'b': np.linspace(-50, 50, 101),
        'fn': lambda x: x**2,
        'eta': 0.2
    },
    {
        'name': 'Sinus, 2 layery',
        'layers': [
            {'fn': tanh, 'size': 1},
            {'fn': tanh, 'size': 10}
        ],
        'x': np.linspace(0, 2, 21),
        'b': np.linspace(0, 2, 161),
        'fn': lambda x: np.sin((3*np.pi/2) * x),
        'eta': 0.01
    },
    {
        'name': 'Parabola, 3 layery',
        'layers': [
            {'fn': sigmoid, 'size': 1},
            {'fn': sigmoid, 'size': 10},
            {'fn': sigmoid, 'size': 10},
        ],
        'x': np.linspace(-50, 50, 26),
        'b': np.linspace(-50, 50, 101),
        'fn': lambda x: x**2,
        'eta': 0.1
    },
    {
        'name': 'Sinus, 3 layery',
        'layers': [
            {'fn': tanh, 'size': 1},
            {'fn': tanh, 'size': 10},
            {'fn': tanh, 'size': 10}
        ],
        'x': np.linspace(0, 2, 21),
        'b': np.linspace(0, 2, 161),
        'fn': lambda x: np.sin((3*np.pi/2) * x),
        'eta': 0.01
    }
]

for test in tests:
    run_tests(test)
