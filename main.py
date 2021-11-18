import random

GENERATION_SIZE = 10
NUMBER_OF_GENERATIONS = 20


def problem(x, y, z):
    return (500 * x) + (2 * y**4) - (3 * z**2) - 200


def cost(x, y, z):
    return abs(0 - problem(x, y, z))


def create_init_genomes():
    genomes = []
    for _ in range(GENERATION_SIZE):
        genomes.append([
            random.randint(-100, 100),
            random.randint(-100, 100),
            random.randint(-100, 100)
        ])
    return genomes


def tournament_selection(input_generation):
    next_gen = []
    for _ in range(GENERATION_SIZE):
        participants = [
            input_generation[random.randint(0, GENERATION_SIZE - 1)],
            input_generation[random.randint(0, GENERATION_SIZE - 1)]
        ]
        participants.sort()
        winner = participants[0]
        next_gen.append(winner)
    return next_gen


def generation_avarage_cost(generation):
    sum = 0
    for genome in generation:
        sum += genome[0]
    return sum / len(generation)


def mutations(generation):
    for genome in generation:
        random_int = random.randint(1, 15)
        if random_int < 2:
            print("MUTATION")
            genome[1][random.randint(0, 2)] = random.randint(-100, 100)
            genome[0] = cost(genome[1][0], genome[1][1], genome[1][2])
    return generation


def main():

    genomes = create_init_genomes()
    genome_with_cost = []

    for genome in genomes:
        genome_with_cost.append(
            [cost(genome[0], genome[1], genome[2]), genome])

    for _ in range(NUMBER_OF_GENERATIONS):
        print("\n")
        print("START")
        print(genome_with_cost)
        genome_with_cost = mutations(genome_with_cost)
        print("AFTER MUTATION")
        print(genome_with_cost)
        genome_with_cost = tournament_selection(genome_with_cost)

        print(generation_avarage_cost(genome_with_cost))


if __name__ == "__main__":
    main()
