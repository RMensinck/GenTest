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
        if random.randint(1, 10000) == 1:
            self.color = random.randint(30, 255), random.randint(
                30, 255), random.randint(30, 120)
            gene_to_mutate = random.choice(
                ["max_age", "food_for_reproduction", "can_kill"])

            if gene_to_mutate == "max_age":
                self.max_age = random.randint(10, 100)

            if gene_to_mutate == "food_for_reproduction":
                self.food_for_reproduction = random.randint(3, 10)

            if gene_to_mutate == "can_kill":
                if self.can_kill == False: new_can_kill = True
                if self.can_kill == True: new_can_kill = False
                self.can_kill = new_can_kill

            return True
        else:
            return False
