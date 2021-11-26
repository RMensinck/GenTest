import random


class Genome:
    def __init__(self, color, max_age, food_for_reproduction,
                 can_kill) -> None:
        self.color = color
        self.max_age = max_age
        self.food_for_reproduction = food_for_reproduction
        self.can_kill = can_kill

    def __str__(self) -> str:
        return f"BacteriaGenome id: {self.id}"

    def mutate(self) -> bool:
        if random.randint(1, 1000) == 1:
            random_color = random.randint(30, 255), random.randint(
                30, 255), random.randint(30, 120)
            gene_to_mutate = random.choice(
                ["max_age", "food_for_reproduction", "can_kill"])
            if gene_to_mutate == "max_age":
                new_max_age = random.randint(10, 100)
                return Genome(random_color, new_max_age,
                              self.food_for_reproduction, self.can_kill)
            if gene_to_mutate == "food_for_reproduction":
                new_food_for_reproduction = random.randint(3, 10)
                return Genome(random_color, self.max_age,
                              new_food_for_reproduction, self.can_kill)
            if gene_to_mutate == "can_kill":
                if self.can_kill == False: new_can_kill = True
                if self.can_kill == True: new_can_kill = False
                return Genome(random_color, self.max_age,
                              self.food_for_reproduction, new_can_kill)

        else:
            return False
