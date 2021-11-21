import cv2 as cv
import numpy as np
import random
from load_constants import CONSTANTS
from SimTerrain import Wall, Pos, TileGrid
from bacteria import Bacteria, BacteriaGenome

TILE_SIZE = CONSTANTS["PARAMETERS"]["TILE_SIZE"]
FIELD_WIDTH = CONSTANTS["PARAMETERS"]["FIELD_WIDTH"]
FIELD_HEIGHT = CONSTANTS["PARAMETERS"]["FIELD_HEIGHT"]
NUMBER_OF_DAYS = CONSTANTS["PARAMETERS"]["NUMBER_OF_DAYS"]
BACKGROUND_COLOR = CONSTANTS["PARAMETERS"]["BACKGROUND_COLOR"]["R"], CONSTANTS[
    "PARAMETERS"]["BACKGROUND_COLOR"]["G"], CONSTANTS["PARAMETERS"][
        "BACKGROUND_COLOR"]["B"]


def draw_field(field_height, field_width, background_color):
    simmap = np.zeros((field_height, field_width, 3), dtype="uint8")
    simmap[:] = background_color
    return simmap


def draw_walls():
    for wall in walls:
        cv.rectangle(simmap,
                     (wall.start_x * TILE_SIZE, wall.start_y * TILE_SIZE),
                     (wall.end_x * TILE_SIZE, wall.end_y * TILE_SIZE),
                     wall.color, cv.FILLED)


def draw_bacteria():
    for bac in bacteria:
        if bacteria == None:
            pass
        cv.rectangle(simmap, (bac.pos.x * TILE_SIZE, bac.pos.y * TILE_SIZE),
                     (bac.pos.x * TILE_SIZE + TILE_SIZE - 1,
                      bac.pos.y * TILE_SIZE + TILE_SIZE - 1), bac.color,
                     cv.FILLED)


def create_new_bacteria(genome_id, bacteria_id):

    genome = BacteriaGenome(genome_id)

    def find_x():
        return random.randint(0, FIELD_WIDTH - 1)

    def find_y():
        return random.randint(0, FIELD_HEIGHT - 1)

    x = find_x()
    y = find_y()
    target_tile = tilemap.get_tile(x, y)

    attempts = 0
    while target_tile.bacteria == True:
        x = find_x()
        y = find_y()
        target_tile = tilemap.get_tile(x, y)
        attempts += 1
        if attempts > 100: return None

    target_tile.bacteria = True

    print(f"new bacteria at {x},{y}")
    return Bacteria(bacteria_id, genome, x, y)


def create_new_wall(id, x, y):
    print("create_new_wall called get_tile")
    target_tile = tilemap.get_tile(x, y)
    target_tile.wall = True
    return Wall(id, x, y)


#Setup walls and bacteria lists
tilemap = TileGrid(FIELD_WIDTH, FIELD_HEIGHT, TILE_SIZE)
walls = []
bacteria = []

simmap = draw_field(FIELD_HEIGHT * TILE_SIZE, FIELD_WIDTH * TILE_SIZE,
                    BACKGROUND_COLOR)

draw_walls()

#Frame loop
for day in range(NUMBER_OF_DAYS):

    print(f"day: {day}")
    if day % 5 == 0:
        new_bac = create_new_bacteria(day, day)
        if new_bac != None:
            print("new bacteria created succesfully")
            bacteria.append(new_bac)

    if day % 10 == 0:
        new_bacteria = []
        for bac in bacteria:
            new_bac = bac.devide(tilemap, FIELD_WIDTH, FIELD_HEIGHT)
            if new_bac != None:
                print(
                    f"bacteria {bac.pos.x},{bac.pos.y} devided succesfully into {new_bac.pos.x},{new_bac.pos.y}"
                )
                new_bacteria.append(new_bac)
            else:
                print(
                    f"bacteria at {bac.pos.x},{bac.pos.y} failed to reproduce")

        for bac in new_bacteria:
            bacteria.append(bac)

    for bac in bacteria:
        bac.move(tilemap, FIELD_WIDTH, FIELD_HEIGHT)

    for i, x in enumerate(tilemap.map):
        for j, y in enumerate(x):
            print(
                f"tile {tilemap.map[i][j].pos.x},{tilemap.map[i][j].pos.y} bac status is: {tilemap.map[i][j].bacteria}"
            )

    #draw background
    simmap = draw_field(FIELD_HEIGHT * TILE_SIZE, FIELD_WIDTH * TILE_SIZE,
                        BACKGROUND_COLOR)

    draw_bacteria()
    print(f"number of bacteria: {len(bacteria)}")
    cv.imshow("blank", simmap)

    cv.waitKey(0)
