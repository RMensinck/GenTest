from copy import Error, copy
import random
import time
import matplotlib.pyplot as plt

GENERATION_SIZE = 30  #must be even number
NUMBER_OF_GENERATIONS = 5


class Genome:
    def __init__(self, identifier):
        self.id = identifier
        self.times_mutated = 0
        self.x = random.randint(-100, 100)
        self.y = random.randint(-100, 100)
        self.z = random.randint(-100, 100)
        self.cost = self.cost_function()

    def mutate(self):
        if random.randint(1, 100) < 2:
            random_int = random.randint(1, 3)
            if random_int == 1: self.x = random.randint(-100, 100)
            if random_int == 2: self.y = random.randint(-100, 100)
            if random_int == 3: self.z = random.randint(-100, 100)
            self.cost = self.cost_function()
            return True
        return False

    def cost_function(self):
        return abs(0 - problem(self.x, self.y, self.z))

    def __str__(self):
        return f"{self.id}.{self.times_mutated}: ({self.x}, {self.y}, {self.z}) costs {self.cost}"


def check_validity_constants():
    if GENERATION_SIZE % 2 != 0 or GENERATION_SIZE < 0:
        print("Generation size must be a even, positive int")
        return False


def problem(x, y, z):
    return (500 * x) + (2 * y**4) - (3 * z**2) - 200


def create_init_genomes():
    return [Genome(id) for id in range(GENERATION_SIZE)]


def tournament_selection(input_generation):
    participant1 = input_generation[random.randint(0, GENERATION_SIZE - 1)]
    participant2 = input_generation[random.randint(0, GENERATION_SIZE - 1)]
    participant3 = input_generation[random.randint(0, GENERATION_SIZE - 1)]
    participant4 = input_generation[random.randint(0, GENERATION_SIZE - 1)]

    if participant1.cost < participant2.cost:
        winner1 = participant1
    else:
        winner1 = participant2

    if participant3.cost < participant4.cost:
        winner2 = participant3
    else:
        winner2 = participant4

    return winner1, winner2


def generation_avarage_cost(generation):
    sum = 0
    for genome in generation:
        sum += genome.cost
    return sum / len(generation)


def crossover(genome1, genome2):

    if random.randint(1, 100) <= 20:
        if random.choice([True, False]):
            x1 = genome1.x
            x2 = genome2.x
            genome1.x = x2
            genome2.x = x1
        if random.choice([True, False]):
            y1 = genome1.y
            y2 = genome2.y
            genome1.y = y2
            genome2.y = y1
        if random.choice([True, False]):
            z1 = genome1.z
            z2 = genome2.z
            genome1.z = z2
            genome2.z = z1


def main():

    if check_validity_constants() == False: raise Error

    genomes = create_init_genomes()

    for generation in range(NUMBER_OF_GENERATIONS):
        for genome in genomes:
            genome.mutate()

        next_gen = []
        for _ in range(GENERATION_SIZE // 2):
            winners = tournament_selection(genomes)
            crossover(winners[0], winners[1])
            next_gen.append(copy(winners[0]))
            next_gen.append(copy(winners[1]))
        genomes = next_gen

        costs = []
        pos = []
        genomes.sort(key=lambda x: x.cost)
        for i, genome in enumerate(genomes):
            costs.append(genome.cost)
            pos.append(i)

            plt.ylim(0, 500000)
            plt.scatter(pos, costs, color="black")
            plt.pause(0.001)

        print(
            f"Generation {generation} done, average cost: {generation_avarage_cost(genomes)}"
        )
    plt.show()


if __name__ == "__main__":
    main()
