from typing import List
import numpy as np
"""
ToDo:

zorgen dat self.n_inputs dynamisch wordt
"""


class Brain:
    def __init__(self, neurons_per_layer, weights_l1, weights_l2, weights_l3):

        self.n_inputs = 13
        self.n_neurons = neurons_per_layer
        self.actions = [
            "move up", "move down", "move left", "move right", "eat", "devide"
        ]
        self.dense1 = self.Layer_Dense(weights_l1, self.n_neurons)
        self.activation1 = self.Activation_ReLU()
        self.dense2 = self.Layer_Dense(weights_l2, self.n_neurons)
        self.activation2 = self.Activation_ReLU()
        self.dense3 = self.Layer_Dense(weights_l3, len(self.actions))
        self.activation3 = self.Activation_Softmax()

    def get_output(self, enviorment_list):
        input_list = self.make_input_list(enviorment_list)
        self.dense1.forward(input_list)
        self.activation1.forward(self.dense1.output)
        self.dense2.forward(self.dense1.output)
        self.activation2.forward(self.dense2.output)
        self.dense3.forward(self.dense2.output)
        self.activation3.forward(self.dense3.output)
        output = self.activation3.output
        highest_output_location = np.where(output == np.amax(output))
        highest_output_index = highest_output_location[1][0]
        action = self.actions[highest_output_index]
        return action

    def make_input_list(self, enviorment_list):
        input_list = np.array([
            enviorment_list["up_tile_empty"], enviorment_list["up_tile_food"],
            enviorment_list["up_tile_bac"], enviorment_list['down_tile_empty'],
            enviorment_list['down_tile_food'],
            enviorment_list['down_tile_bac'],
            enviorment_list['left_tile_empty'],
            enviorment_list['left_tile_food'],
            enviorment_list['left_tile_bac'],
            enviorment_list['right_tile_empty'],
            enviorment_list['right_tile_food'],
            enviorment_list['right_tile_bac'], enviorment_list['food_eaten']
        ])
        return input_list

    class Layer_Dense:
        def __init__(self, weights, n_neurons):
            self.weights = weights
            self.biases = np.zeros((1, n_neurons))

        def forward(self, inputs):
            self.output = np.dot(inputs, self.weights) + self.biases

    class Activation_ReLU:
        def forward(self, inputs):
            self.output = np.maximum(0, inputs)

    class Activation_Softmax:
        def forward(self, inputs):
            exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
            probabilities = exp_values / np.sum(
                exp_values, axis=1, keepdims=True)
            self.output = probabilities
