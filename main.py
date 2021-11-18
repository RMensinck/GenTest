import random

GENERATION_SIZE = 10
NUMBER_OF_GENERATIONS = 5

random.seed(1)


class Genome:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.cost = self.cost_function()

    def mutations(self):
        if random.randint(1, 100) < 5:
            random_int = random.randint(1, 3)
            if random_int == 1: self.x = random.randint(-100, 100)
            if random_int == 2: self.y = random.randint(-100, 100)
            if random_int == 3: self.z = random.randint(-100, 100)
            self.cost = self.cost_function()
            print("mutation occured---------------")

    def cost_function(self):
        return abs(0 - problem(self.x, self.y, self.z))


def problem(x, y, z):
    return (500 * x) + (2 * y**4) - (3 * z**2) - 200


def create_init_genomes():
    genomes = []
    for _ in range(GENERATION_SIZE):
        genomes.append(
            Genome(random.randint(-100, 100), random.randint(-100, 100),
                   random.randint(-100, 100)))
    return genomes


def tournament_selection(input_generation):
    next_gen = []
    for _ in range(GENERATION_SIZE):
        participants = [
            input_generation[random.randint(0, GENERATION_SIZE - 1)],
            input_generation[random.randint(0, GENERATION_SIZE - 1)]
        ]
        if participants[0].cost < participants[1].cost:
            winner = participants[0]
        else:
            winner = participants[1]
        next_gen.append(winner)
    return next_gen


def generation_avarage_cost(generation):
    sum = 0
    for genome in generation:
        sum += genome.cost
    return sum / len(generation)


def main():

    genomes = create_init_genomes()

    for _ in range(NUMBER_OF_GENERATIONS):
        print("\n")
        for genome in genomes:
            print(f"pre-mutatie: {genome.x} {genome.y} {genome.z}")
            genome.mutations()
            print(f"post-mutatie: {genome.x} {genome.y} {genome.z}")
        genomes = tournament_selection(genomes)

        print(generation_avarage_cost(genomes))


if __name__ == "__main__":
    main()
