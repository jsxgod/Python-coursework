import numpy as np

from utils import sigmoid, relu

# GLOBAL VALUES
ETA = 0.01
ITERATIONS = 5000
NEURONS = 4

X = np.array(
    [[0, 0, 1],
     [0, 1, 1],
     [1, 0, 1],
     [1, 1, 1]
     ])

operators = [
    ('XOR', np.array([[0.], [1.], [1.], [0.]])),
    ('AND', np.array([[0.], [0.], [0.], [1.]])),
    ('OR', np.array([[1.], [1.], [1.], [1.]]))
]

functions = [sigmoid, relu]


class NeuralNetwork:
    def __init__(self, X, expected, func1, func2, eta):
        self.eta = eta
        self.X = X
        self.expected_output = expected
        self.output = np.zeros(expected.shape)

        self.weights1 = np.random.rand(NEURONS, X.shape[1])
        self.weights2 = np.random.rand(1, NEURONS)

        self.f1, self.f1_d = func1
        self.f2, self.f2_d = func2

    def feed_forward(self):
        self.layer1 = self.f1(np.dot(self.X, self.weights1.T))
        self.output = self.f2(np.dot(self.layer1, self.weights2.T))

    def back_propagation(self):
        delta2 = (self.expected_output - self.output) * self.f2_d(self.output)
        d_weights2 = self.eta * np.dot(delta2.T, self.layer1)

        delta1 = self.f1_d(self.layer1) * np.dot(delta2, self.weights2)
        d_weights1 = self.eta * np.dot(delta1.T, self.X)

        self.weights1 += d_weights1
        self.weights2 += d_weights2

    def train(self, i):
        for _ in range(i):
            self.feed_forward()
            self.back_propagation()


def run_tests(f1, f2):
    for op_name, op_result in operators:
        network = NeuralNetwork(X=X, expected=op_result, func1=f1, func2=f2, eta=ETA)
        network.train(ITERATIONS)
        print(op_name, " :" + "\t\t ", network.output.flatten())
        print("expected :\t ", op_result.flatten(), '\n')

    print('##########################################################################')


np.set_printoptions(precision=3, floatmode='fixed')

print('SIGMOID | SIGMOID')
run_tests(sigmoid, sigmoid)
print('SIGMOID | RELU')
run_tests(sigmoid, relu)
print('RELU | SIGMOID')
run_tests(relu, sigmoid)
print('RELU | RELU')
run_tests(relu, relu)
