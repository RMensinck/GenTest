import cv2 as cv
import numpy as np
import time
import random
from SimTerrain import Wall, Border, Pos, Grid
from bacteria import Bacteria, BacteriaGenome

GRID_SIZE = 5
FIELD_WIDTH = 200
FIELD_HEIGHT = 100
BACKGROUND_COLOR = 222, 222, 222


def draw_field(field_height, field_width, background_color):
    simmap = np.zeros((field_height, field_width, 3), dtype="uint8")
    simmap[:] = background_color
    return simmap


def draw_borders():
    cv.rectangle(simmap, (border.start_x, border.start_y),
                 (border.final_x, border.final_y), border.color, border.width)


def draw_walls():
    for wall in walls:
        cv.rectangle(simmap,
                     (wall.start_x * GRID_SIZE, wall.start_y * GRID_SIZE),
                     (wall.end_x * GRID_SIZE, wall.end_y * GRID_SIZE),
                     wall.color, cv.FILLED)


def draw_bacteria():
    for bac in bacteria:
        cv.rectangle(simmap, (bac.pos.x * GRID_SIZE, bac.pos.y * GRID_SIZE),
                     (bac.pos.x * GRID_SIZE + 5, bac.pos.y * GRID_SIZE + 5),
                     bac.color, cv.FILLED)


def create_new_bacteria(genome_id, bacteria_id, x, y):
    genome = BacteriaGenome(genome_id)
    return Bacteria(bacteria_id, genome, x, y)


#Setup walls and bacteria lists
grid = Grid(FIELD_WIDTH, FIELD_HEIGHT, GRID_SIZE)
walls = []
bacteria = []

simmap = draw_field(FIELD_HEIGHT * GRID_SIZE, FIELD_WIDTH * GRID_SIZE,
                    BACKGROUND_COLOR)

#draw_borders()
draw_walls()

#Frame loop
for frame in range(100):

    print(f"frame: {frame}")

    bacteria.append(
        create_new_bacteria(frame, frame, random.randint(0, 150),
                            random.randint(0, 50)))

    simmap = draw_field(FIELD_HEIGHT * GRID_SIZE, FIELD_WIDTH * GRID_SIZE,
                        BACKGROUND_COLOR)
    draw_bacteria()
    time.sleep(1)

    cv.imshow("blank", simmap)

    cv.waitKey(10)