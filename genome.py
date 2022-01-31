import random
import numpy as np


class Genome:
    def __init__(self, l1, l2, l3, b1, b2, b3) -> None:

        self.weights_l1 = l1
        self.weights_l2 = l2
        self.weights_l3 = l3
        self.bias1 = b1
        self.bias2 = b2
        self.bias3 = b3

    def mutate(self):
        mutation_target = random.choice(["weights", "biases", "Nothing"])
        if mutation_target == "weights":
            weights_to_mutate = random.randint(1, 3)
            if weights_to_mutate == 1:
                target_weights = self.weights_l1
            if weights_to_mutate == 2:
                target_weights = self.weights_l2
            if weights_to_mutate == 3:
                target_weights = self.weights_l3
            target_weights[random.randint(
                0, target_weights.shape[0] - 1)][random.randint(
                    0, target_weights.shape[1] - 1)] = np.random.randn(1)[0]

        if mutation_target == "biases":
            bias_to_mutate = random.randint(1, 3)
            if bias_to_mutate == 1:
                target_bias = self.bias1
            if bias_to_mutate == 2:
                target_bias = self.bias2
            if bias_to_mutate == 3:
                target_bias = self.bias3
            target_bias[0][random.randint(0, target_bias.shape[1] -
                                          1)] = np.random.randn(1)[0]

    def __str__(self) -> str:
        return f"BacteriaGenome id: {self.id}"
