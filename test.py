import random
from main import cost, create_init_genomes
"""
genomes = create_init_genomes()
genomes_with_cost = []

for genome in genomes:
    genomes_with_cost.append([cost(genome[0], genome[1], genome[2]), genome])

print(genomes_with_cost)
"""
genomes_with_cost = [[94922142, [60, 83, -90]], [94922142, [60, 83, -90]],
                     [94922142, [60, 83, -90]], [94922142, [60, 83, -90]],
                     [94922142, [60, 83, -90]], [94922142, [60, 83, -90]],
                     [94922142, [60, 83, -90]], [94922142, [60, 83, -90]],
                     [94922142, [60, 83, -90]], [94922142, [60, 83, -90]]]
print("BEFORE")
print(genomes_with_cost)


def mutations(generation):
    for genome in generation:
        random_int = random.randint(1, 15)
        if random_int < 2:
            print("MUTATION OCCURED")
            genome[1][random.randint(0, 2)] = random.randint(-100, 100)
            genome[0] = cost(genome[1][0], genome[1][1], genome[1][2])
    return generation


print("AFTER")
print(mutations(genomes_with_cost))