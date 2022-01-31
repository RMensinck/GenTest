from copy import copy, error
from typing import DefaultDict
import cv2 as cv
import numpy as np
import random
from load_constants import CONSTANTS
from sim_terrain import Tile, Wall, Position, TileGrid
from bacteria import Bacteria, Genome
from food import Food
from statistics import median
import matplotlib.pyplot as plt

TILE_SIZE = CONSTANTS["PARAMETERS"]["TILE_SIZE"]
FIELD_WIDTH = CONSTANTS["PARAMETERS"]["FIELD_WIDTH"]
FIELD_HEIGHT = CONSTANTS["PARAMETERS"]["FIELD_HEIGHT"]
NUMBER_OF_DAYS = CONSTANTS["PARAMETERS"]["NUMBER_OF_DAYS"]
BACKGROUND_COLOR = CONSTANTS["PARAMETERS"]["BACKGROUND_COLOR"]["R"], CONSTANTS[
    "PARAMETERS"]["BACKGROUND_COLOR"]["G"], CONSTANTS["PARAMETERS"][
        "BACKGROUND_COLOR"]["B"]
HEADLESS = CONSTANTS["PARAMETERS"]["HEADLESS"]
MUTATION_ODDS = CONSTANTS["PARAMETERS"]["MUTATION_ODDS"]

MAX_AGE = 50
FOOD_FOR_REPRODUCTION = 4
GENERATION_SIZE = 300


def draw_field(field_height, field_width, background_color) -> np.array:
    simulation_map = np.zeros((field_height, field_width, 3), dtype="uint8")
    simulation_map[:] = background_color
    return simulation_map


def draw_food() -> None:
    for food in foods:
        cv.rectangle(simulation_map,
                     (food.pos.x * TILE_SIZE, food.pos.y * TILE_SIZE),
                     (food.pos.x * TILE_SIZE + TILE_SIZE - 1,
                      food.pos.y * TILE_SIZE + TILE_SIZE - 1), food.color,
                     cv.FILLED)


def draw_bacteria() -> None:
    for bac in bacteria:
        if bac == None:
            pass
        cv.rectangle(simulation_map,
                     (bac.pos.x * TILE_SIZE, bac.pos.y * TILE_SIZE),
                     (bac.pos.x * TILE_SIZE + TILE_SIZE - 1,
                      bac.pos.y * TILE_SIZE + TILE_SIZE - 1), bac.color,
                     cv.FILLED)


def find_random_pos() -> Position:
    target_pos = Position(random.randint(0, FIELD_WIDTH - 1),
                          random.randint(0, FIELD_HEIGHT - 1))
    return target_pos


def find_open_random_pos(max_attempts) -> Tile:
    target_tile = tilemap.get_tile_by_pos(find_random_pos())
    attempts = 0
    while target_tile.is_open() == False:
        target_tile = tilemap.get_tile_by_pos(find_random_pos())
        attempts += 1
        if attempts > max_attempts: return None
    return target_tile


def create_new_bacteria(number_to_spawn) -> None:
    output_bacteria = []
    for _ in range(number_to_spawn):
        target_tile = find_open_random_pos(100)
        if target_tile != None:
            new_bac = Bacteria(
                random.randint(0, 1000000), target_tile.pos, 0, MAX_AGE,
                FOOD_FOR_REPRODUCTION, get_random_color(),
                Genome(np.random.randn(16, 10), np.random.randn(10, 10),
                       np.random.randn(10, 6), np.random.randn(1, 10),
                       np.random.randn(1, 10), np.random.randn(1, 6)))
            target_tile.bacteria = new_bac
            output_bacteria.append(new_bac)
    return output_bacteria


def create_food(number_of_foods) -> None:
    for _ in range(number_of_foods):
        target_tile = find_open_random_pos(100)
        if target_tile != None:
            new_food = Food(target_tile.pos)
            target_tile.food = new_food
            foods.append(new_food)


def get_random_color() -> tuple:
    return random.randint(0, 255), random.randint(0,
                                                  255), random.randint(0, 255)


def tournament_selection(input_generation) -> tuple:
    participants = random.sample(input_generation, 4)

    if participants[0].score > participants[1].score:
        winner1 = participants[0]
    else:
        winner1 = participants[1]

    if participants[2].score > participants[3].score:
        winner2 = participants[2]
    else:
        winner2 = participants[3]

    return winner1, winner2


def crossover(winner1, winner2) -> None:

    if random.randint(1, 100) <= 10:
        weight_to_mutate = random.choice(["l1", "l2", "l3"])

        if weight_to_mutate == "l1":
            target_weights_1 = winner1.genome.weights_l1
            target_weights_2 = winner2.genome.weights_l1

        if weight_to_mutate == "l2":
            target_weights_1 = winner1.genome.weights_l2
            target_weights_2 = winner2.genome.weights_l2

        if weight_to_mutate == "l3":
            target_weights_1 = winner1.genome.weights_l3
            target_weights_2 = winner2.genome.weights_l3

        weights_1 = copy(target_weights_1)
        weights_2 = copy(target_weights_2)

        if weights_1.shape != weights_2.shape: raise error
        original_shape = weights_1.shape
        weights_length = len(weights_1)

        weights_1 = weights_1.flatten()
        weights_2 = weights_2.flatten()

        crossover_point = random.randint(1, weights_length - 1)

        new_1 = np.concatenate(
            (weights_1[:crossover_point], weights_2[crossover_point:]))
        new_2 = np.concatenate(
            (weights_2[:crossover_point], weights_1[crossover_point:]))

        target_weights_1 = np.reshape(new_1, original_shape)
        target_weights_2 = np.reshape(new_2, original_shape)
        winner1.color = (random.randint(1, 255), random.randint(1, 255),
                         random.randint(1, 255))
        winner2.color = (random.randint(1, 255), random.randint(1, 255),
                         random.randint(1, 255))

    if random.randint(1, 100) <= 30:
        bias_to_mutate = random.choice(["b1", "b2", "b3"])

        if bias_to_mutate == "b1":
            target_bias1 = winner1.genome.bias1
            target_bias2 = winner2.genome.bias1

        if bias_to_mutate == "b2":
            target_bias1 = winner1.genome.bias2
            target_bias2 = winner2.genome.bias2

        if bias_to_mutate == "b3":
            target_bias1 = winner1.genome.bias3
            target_bias2 = winner2.genome.bias3

        bias_1 = copy(target_bias1)
        bias_2 = copy(target_bias2)

        if bias_1.shape != bias_2.shape: raise error
        bias_shape = bias_1.shape

        bias_1 = bias_1.flatten()
        bias_2 = bias_2.flatten()

        bias_length = len(bias_1)

        crossover_point = random.randint(1, bias_length - 1)

        new_1 = np.concatenate(
            (bias_1[:crossover_point], bias_2[crossover_point:]))
        new_2 = np.concatenate(
            (bias_2[:crossover_point], bias_1[crossover_point:]))

        target_bias1 = np.reshape(new_1, bias_shape)
        target_bias2 = np.reshape(new_2, bias_shape)
        winner1.color = (random.randint(1, 255), random.randint(1, 255),
                         random.randint(1, 255))
        winner2.color = (random.randint(1, 255), random.randint(1, 255),
                         random.randint(1, 255))


#Setup bacteria lists
tilemap = TileGrid(FIELD_WIDTH, FIELD_HEIGHT, TILE_SIZE)
bacteria = []
foods = []
simulation_map = draw_field(FIELD_HEIGHT * TILE_SIZE, FIELD_WIDTH * TILE_SIZE,
                            BACKGROUND_COLOR)


def simulate(generation, input_bacteria=None, headless=HEADLESS) -> dict:
    global bacteria
    global tilemap
    global foods
    global simulation_map
    global GENERATION_SIZE

    tilemap = TileGrid(FIELD_WIDTH, FIELD_HEIGHT, TILE_SIZE)
    bacteria = []
    foods = []

    simulation_map = draw_field(FIELD_HEIGHT * TILE_SIZE,
                                FIELD_WIDTH * TILE_SIZE, BACKGROUND_COLOR)
    bacteria = input_bacteria
    spicies_score_dict = {}
    for bac in bacteria:
        spicies_score_dict[bac.color] = {"bacteria": bac, "score": 0}
    #Frame loop
    for day in range(1000):
        #spawn food
        if len(foods) < 2000:
            create_food(300)
        if day == 0:
            create_food(2000)

        if headless == False:
            draw_bacteria()
            draw_food()
            cv.imshow("blank", simulation_map)
            cv.waitKey(0)

        #update age of all bacteria
        new_bacteria = []
        for bac in bacteria:
            bac.update_age()
            if bac.check_survival() == False:
                bac_tile = tilemap.get_tile_by_pos(bac.pos)
                bac_tile.bacteria = None
                bacteria.remove(bac)
                #continue

            action = bac.get_action(tilemap, FIELD_WIDTH, FIELD_HEIGHT)

            if action == "move up":
                bac.move_up(tilemap, FIELD_WIDTH, FIELD_HEIGHT)
            if action == "move down":
                bac.move_down(tilemap, FIELD_WIDTH, FIELD_HEIGHT)
            if action == "move left":
                bac.move_left(tilemap, FIELD_WIDTH, FIELD_HEIGHT)
            if action == "move right":
                bac.move_right(tilemap, FIELD_WIDTH, FIELD_HEIGHT)
            if action == "eat":
                bac.eat(tilemap, FIELD_WIDTH, FIELD_HEIGHT)
            if action == "devide":
                if bac.food_eaten >= 3:
                    new_bac = bac.devide(tilemap, FIELD_WIDTH, FIELD_HEIGHT,
                                         MUTATION_ODDS)
                    if new_bac != None:
                        new_bacteria.append(new_bac)

        for bac in new_bacteria:
            bacteria.append(bac)

        #check food stock left
        for food in foods:
            if food.check_stock_left() == False:
                food_tile = tilemap.get_tile_by_pos(food.pos)
                food_tile.food = None
                foods.remove(food)

        #check if any bacteria left
        if len(bacteria) == 0:
            print(f"bacteria survived for {day} days ")
            break

        #draw background
        simulation_map = draw_field(FIELD_HEIGHT * TILE_SIZE,
                                    FIELD_WIDTH * TILE_SIZE, BACKGROUND_COLOR)

        spicies_tracker_dict = DefaultDict(lambda: 0)
        for bac in bacteria:
            spicies_tracker_dict[bac.color] += 1

        for bac in bacteria:
            spicies_spec_dict = spicies_score_dict[bac.color]
            spicies_spec_dict["score"] += bac.score
        """
        if headless == False:
            if day % 3 == 0:
                #plt.scatter(day, len(bacteria), color="black")
                for key in spicies_tracker_dict:
                    if spicies_tracker_dict[key] > 60:
                        plt.scatter(
                            day,
                            spicies_tracker_dict[key],
                            color=(key[2] / 255, key[1] / 255, key[0] / 255)
                        )  #flipped because colors in open cv are BGR
        """
    return spicies_score_dict


def get_generation_avarage_score(spicies_score_dict):
    total_score = 0
    for spicies in spicies_score_dict:
        total_score += spicies_score_dict[spicies]["score"]

    return total_score / GENERATION_SIZE


def get_generation_median_score(spicies_score_dict):
    scores = []
    for spicies in spicies_score_dict:
        scores.append(spicies_score_dict[spicies]["score"])
    return median(scores)


def simulate_multiple_generations(number_of_generations):
    #create starting bacteria set
    input_generation = create_new_bacteria(GENERATION_SIZE)

    for generation in range(number_of_generations):
        #simulate the generation
        spicies_score_dict = simulate(generation,
                                      input_bacteria=input_generation)

        #print the preformance of the simulated generation
        avarage_score = get_generation_avarage_score(spicies_score_dict)
        median_score = get_generation_median_score(spicies_score_dict)
        print(
            f"generation: {generation}, avarage score: {avarage_score}, median score: {median_score}"
        )

        plt.scatter(generation, avarage_score, color="black")
        plt.scatter(generation, median_score, color="red")

        #create the next generation
        output_generation = []
        for spicies in spicies_score_dict:
            output_generation.append(spicies_score_dict[spicies]["bacteria"])

        #tournament selection and crossover
        output_generation_crossed = []
        for _ in range(GENERATION_SIZE // 2):
            winners = tournament_selection(output_generation)
            crossover(winners[0], winners[1])
            output_generation_crossed.append(copy(winners[0]))
            output_generation_crossed.append(copy(winners[1]))

        input_generation = output_generation_crossed

        #reset all bacteria
        for bac in input_generation:
            bac.age = 0
            bac.pos = bac.get_random_spawn_pos(tilemap, FIELD_WIDTH,
                                               FIELD_HEIGHT)
            bac.color = get_random_color()
            bac.score = 0
            bac.genome = copy(bac.genome)
            bac.update_brain()
            if random.randint(1, 100) < 5:
                bac.genome.mutate()

    plt.show()


def main() -> None:
    simulate_multiple_generations(100)


if __name__ == "__main__":
    main()
