from typing import DefaultDict
import cv2 as cv
import numpy as np
import random
from load_constants import CONSTANTS
from sim_terrain import Tile, Wall, Position, TileGrid
from bacteria import Bacteria, Genome
from food import Food
import matplotlib.pyplot as plt

TILE_SIZE = CONSTANTS["PARAMETERS"]["TILE_SIZE"]
FIELD_WIDTH = CONSTANTS["PARAMETERS"]["FIELD_WIDTH"]
FIELD_HEIGHT = CONSTANTS["PARAMETERS"]["FIELD_HEIGHT"]
NUMBER_OF_DAYS = CONSTANTS["PARAMETERS"]["NUMBER_OF_DAYS"]
BACKGROUND_COLOR = CONSTANTS["PARAMETERS"]["BACKGROUND_COLOR"]["R"], CONSTANTS[
    "PARAMETERS"]["BACKGROUND_COLOR"]["G"], CONSTANTS["PARAMETERS"][
        "BACKGROUND_COLOR"]["B"]
HEADLESS = CONSTANTS["PARAMETERS"]["HEADLESS"]

START_COLOR = (150, 70, 70)
START_CAN_KILL = False
START_MAX_AGE = 30
START_FOOD_FOR_REPRODUCTION = 3


def draw_field(field_height, field_width, background_color):
    simulation_map = np.zeros((field_height, field_width, 3), dtype="uint8")
    simulation_map[:] = background_color
    return simulation_map


def draw_walls():
    for wall in walls:
        cv.rectangle(simulation_map,
                     (wall.start_x * TILE_SIZE, wall.start_y * TILE_SIZE),
                     (wall.end_x * TILE_SIZE, wall.end_y * TILE_SIZE),
                     wall.color, cv.FILLED)


def draw_food():
    for food in foods:
        cv.rectangle(simulation_map,
                     (food.pos.x * TILE_SIZE, food.pos.y * TILE_SIZE),
                     (food.pos.x * TILE_SIZE + TILE_SIZE - 1,
                      food.pos.y * TILE_SIZE + TILE_SIZE - 1), food.color,
                     cv.FILLED)


def draw_bacteria():
    for bac in bacteria:
        if bacteria == None:
            pass
        cv.rectangle(simulation_map,
                     (bac.pos.x * TILE_SIZE, bac.pos.y * TILE_SIZE),
                     (bac.pos.x * TILE_SIZE + TILE_SIZE - 1,
                      bac.pos.y * TILE_SIZE + TILE_SIZE - 1), bac.color,
                     cv.FILLED)


def find_random_pos():
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


def create_new_bacteria(bacteria_id, number_to_spawn) -> None:
    for _ in range(number_to_spawn):
        target_tile = find_open_random_pos(100)
        if target_tile != None:
            target_tile.bacteria = True
            bacteria.append(
                Bacteria(
                    bacteria_id, target_tile.pos,
                    Genome(START_COLOR, START_MAX_AGE,
                           START_FOOD_FOR_REPRODUCTION, START_CAN_KILL)))


def create_new_wall(id, x, y):
    """
    update before using
    """
    target_tile = tilemap.get_tile(x, y)
    target_tile.wall = True
    return Wall(id, x, y)


def create_food(number_of_foods) -> None:
    for _ in range(number_of_foods):
        target_tile = find_open_random_pos(100)
        if target_tile != None:
            target_tile.food = True
            foods.append(Food(target_tile.pos))


#Setup walls and bacteria lists
tilemap = TileGrid(FIELD_WIDTH, FIELD_HEIGHT, TILE_SIZE)
walls = []
bacteria = []
foods = []

simulation_map = draw_field(FIELD_HEIGHT * TILE_SIZE, FIELD_WIDTH * TILE_SIZE,
                            BACKGROUND_COLOR)

#Frame loop
for day in range(NUMBER_OF_DAYS + 10000):

    if day % 100 == 0:
        print(f"day: {day}")

    #spawn food
    if day % 10 == 0:
        create_food(5)
    if day == 0:
        create_food(100)

    #add new bacteria
    if day < 1:
        create_new_bacteria(1, 3)

    #move all bacteria arround randomly
    for bac in bacteria:
        bac.move(tilemap, FIELD_WIDTH, FIELD_HEIGHT)

    #update age of all bacteria and let them eat
    new_bacteria = []
    for bac in bacteria:
        bac.update_age()
        bac.eat(foods)
        if bac.check_survival() == False:
            bac_tile = tilemap.get_tile_by_pos(bac.pos)
            bac_tile.bacteria = False
            bacteria.remove(bac)
            continue
        if bac.food_eaten >= 3:
            new_bac = bac.devide(tilemap, FIELD_WIDTH, FIELD_HEIGHT)
            bac.food_eaten = 0
            if new_bac != None:
                new_bacteria.append(new_bac)

        if bac.can_kill:
            bac.kill_adjecent_bacteria(bacteria, tilemap)
        if bac.genome.mutate() == True:
            bac.update_self()
    for bac in new_bacteria:
        bacteria.append(bac)

    #check food stock left
    for food in foods:
        if food.check_stock_left() == False:
            food_tile = tilemap.get_tile_by_pos(food.pos)
            food_tile.food = False
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

    if HEADLESS == False:
        draw_bacteria()
        draw_food()
        print(f"number of bacteria: {len(bacteria)}")
        cv.imshow("blank", simulation_map)
        cv.waitKey(0)
    if day % 5 == 0:
        #plt.scatter(day, len(bacteria), color="black")
        for key in spicies_tracker_dict:
            plt.scatter(
                day,
                spicies_tracker_dict[key],
                color=(key[2] / 255, key[1] / 255, key[0] /
                       255))  #flipped because colors in open cv are BGR

plt.show()
