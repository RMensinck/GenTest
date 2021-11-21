import random
from SimTerrain import Pos


class Bacteria:
    def __init__(self, id, genome, x, y):
        self.id = id
        self.genome = genome
        self.pos = Pos(x, y)
        self.color = 150, 70, 70

    def __str__(self):
        return f"Bacteria id: {self.id}"

    def move(self, tilemap, FIELD_WIDTH, FIELD_HEIGHT):
        target_tile = self.get_random_open_adjecent_tile(
            tilemap, FIELD_WIDTH, FIELD_HEIGHT)
        if target_tile == None: return None
        old_tile = tilemap.get_tile_by_pos(self.pos)
        old_tile.bacteria = False
        self.pos = Pos(target_tile.pos.x, target_tile.pos.y)
        new_tile = tilemap.get_tile_by_pos(self.pos)
        new_tile.bacteria = True

    def devide(self, tilemap, FIELD_WIDTH, FIELD_HEIGHT):

        target_tile = self.get_random_open_adjecent_tile(
            tilemap, FIELD_WIDTH, FIELD_HEIGHT)
        if target_tile == None: return None
        target_tile.bacteria = True

        return Bacteria(self.id, BacteriaGenome(self.id), target_tile.pos.x,
                        target_tile.pos.y)

    def get_random_direction(self, FIELD_WIDTH, FIELD_HEIGHT):

        #input loc is not on the edge of the field
        if self.pos.x > 0 and self.pos.x < FIELD_WIDTH - 1 and self.pos.y > 0 and self.pos.y < FIELD_HEIGHT - 1:
            target_direction = random.choice(["up", "down", "left", "right"])

        #checks if input location is in a corner
        elif self.pos.x <= 0 and self.pos.y <= 0:
            target_direction = random.choice(["down", "right"])
        elif self.pos.x <= 0 and self.pos.y >= FIELD_HEIGHT - 1:
            target_direction = random.choice(["up", "right"])
        elif self.pos.x >= FIELD_WIDTH - 1 and self.pos.y <= 0:
            target_direction = random.choice(["down", "left"])
        elif self.pos.x >= FIELD_WIDTH - 1 and self.pos.y >= FIELD_HEIGHT - 1:
            target_direction = random.choice(["up", "left"])

        #if input location is on a edge
        elif self.pos.x <= 0:
            target_direction = random.choice(["up", "down", "right"])
        elif self.pos.x >= FIELD_WIDTH - 1:
            target_direction = random.choice(["up", "down", "left"])
        elif self.pos.y <= 0:
            target_direction = random.choice(["down", "left", "right"])
        elif self.pos.y >= FIELD_HEIGHT - 1:
            target_direction = random.choice(["up", "left", "right"])

        return target_direction

    def get_random_open_adjecent_tile(self, tilemap, FIELD_WIDTH,
                                      FIELD_HEIGHT):
        direction = self.get_random_direction(FIELD_WIDTH, FIELD_HEIGHT)
        if direction == "up":
            target_tile = tilemap.get_tile(self.pos.x, self.pos.y - 1)
        if direction == "down":
            target_tile = tilemap.get_tile(self.pos.x, self.pos.y + 1)
        if direction == "right":
            target_tile = tilemap.get_tile(self.pos.x + 1, self.pos.y)
        if direction == "left":
            target_tile = tilemap.get_tile(self.pos.x - 1, self.pos.y)

        attempts = 0
        while target_tile.is_open() == False:
            direction = self.get_random_direction(FIELD_WIDTH, FIELD_HEIGHT)
            if direction == "up":
                target_tile = tilemap.get_tile(self.pos.x, self.pos.y - 1)
            if direction == "down":
                target_tile = tilemap.get_tile(self.pos.x, self.pos.y + 1)
            if direction == "right":
                target_tile = tilemap.get_tile(self.pos.x + 1, self.pos.y)
            if direction == "left":
                target_tile = tilemap.get_tile(self.pos.x - 1, self.pos.y)
            attempts += 1
            if attempts >= 10: return None

        return target_tile


class BacteriaGenome:
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return f"BacteriaGenome id: {self.id}"