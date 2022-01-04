import random
import numpy as np


class Genome:
    def __init__(self, color, max_age, food_for_reproduction, l1, l2,
                 l3) -> None:
        self.color = color
        self.max_age = max_age
        self.food_for_reproduction = food_for_reproduction
        self.weights_l1 = l1
        self.weights_l2 = l2
        self.weights_l3 = l3

    def __str__(self) -> str:
        return f"BacteriaGenome id: {self.id}"
