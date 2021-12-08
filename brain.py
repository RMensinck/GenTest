import numpy as np

inputs = np.array([5, 2, 1])
outputs = ["move up", "move down", "move right", "move left", "eat", "devide"]


class Brain:
    def __init__(self, input_list, neurons_per_layer) -> None:
        self.input_list = input_list
        self.n_inputs = len(input_list)
        self.n_neurons = neurons_per_layer
        self.output = None
        self.dense1 = Layer_Dense(self.n_inputs, self.n_neurons)
        self.activation1 = Activation_ReLU()
        self.dense2 = Layer_Dense(self.n_neurons, self.n_neurons)
        self.activation2 = Activation_ReLU()
        self.dense3 = Layer_Dense(self.n_neurons, 4)
        self.activation3 = Activation_Softmax()

    def get_action(self) -> int:
        self.dense1.forward(inputs)
        self.activation1.forward(self.dense1.output)
        self.dense2.forward(self.dense1.output)
        self.activation2.forward(self.dense2.output)
        self.dense3.forward(self.dense2.output)
        self.activation3.forward(self.dense3.output)
        action = self.dense3.output
        return action


class Layer_Dense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.1 * np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))

    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases


class Activation_ReLU:
    def forward(self, inputs):
        self.output = np.maximum(0, inputs)


class Activation_Softmax:
    def forward(self, inputs):
        exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        probabilities = exp_values / np.sum(exp_values, axis=1, keepdims=True)
        self.output = probabilities


def test():
    brain = Brain(inputs, 5)
    print(brain.get_action())


if __name__ == "__main__":
    test()