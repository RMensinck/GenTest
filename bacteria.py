import random
from matplotlib.pyplot import colorbar
from sim_terrain import Position, Tile
from genome import Genome


class Bacteria:
    def __init__(self, id, pos, genome) -> None:
        self.id = id
        self.genome = genome
        self.pos = pos
        self.age = 0
        self.food_eaten = 0
        self.max_age = self.genome.max_age
        self.food_for_reproduction = self.genome.food_for_reproduction
        self.color = self.genome.color
        self.can_kill = self.genome.can_kill

    def __str__(self) -> str:
        return f"Bacteria id: {self.id}"

    def get_enviroment_dict(self, tilemap, FIELD_WIDTH, FIELD_HEIGHT):
        enviroment = {}
        if self.pos.y > 0:
            uptile = tilemap.get_tile(self.pos.x, self.pos.y - 1)
            if uptile.is_open():
                enviroment["up_tile_empty"] = 1
                enviroment["up_tile_food"] = 0
                enviroment["up_tile_bac"] = 0
            elif uptile.food != None:
                enviroment["up_tile_empty"] = 0
                enviroment["up_tile_food"] = 1
                enviroment["up_tile_bac"] = 0
            elif uptile.bacteria != None:
                enviroment["up_tile_empty"] = 0
                enviroment["up_tile_food"] = 0
                enviroment["up_tile_bac"] = 1
        else:
            enviroment["up_tile_empty"] = 0
            enviroment["up_tile_food"] = 0
            enviroment["up_tile_bac"] = 0

        if self.pos.y < FIELD_HEIGHT - 1:
            downtile = tilemap.get_tile(self.pos.x, self.pos.y + 1)
            if downtile.is_open():
                enviroment["down_tile_empty"] = 1
                enviroment["down_tile_food"] = 0
                enviroment["down_tile_bac"] = 0
            elif downtile.food != None:
                enviroment["down_tile_empty"] = 0
                enviroment["down_tile_food"] = 1
                enviroment["down_tile_bac"] = 0
            elif downtile.bacteria != None:
                enviroment["down_tile_empty"] = 0
                enviroment["down_tile_food"] = 0
                enviroment["down_tile_bac"] = 1
        else:
            enviroment["down_tile_empty"] = 0
            enviroment["down_tile_food"] = 0
            enviroment["down_tile_bac"] = 0

        if self.pos.x > 0:
            lefttile = tilemap.get_tile(self.pos.x - 1, self.pos.y)
            if lefttile.is_open():
                enviroment["left_tile_empty"] = 1
                enviroment["left_tile_food"] = 0
                enviroment["left_tile_bac"] = 0
            elif lefttile.food != None:
                enviroment["left_tile_empty"] = 0
                enviroment["left_tile_food"] = 1
                enviroment["left_tile_bac"] = 0
            elif lefttile.bacteria != None:
                enviroment["left_tile_empty"] = 0
                enviroment["left_tile_food"] = 0
                enviroment["left_tile_bac"] = 1
        else:
            enviroment["left_tile_empty"] = 0
            enviroment["left_tile_food"] = 0
            enviroment["left_tile_bac"] = 0

        if self.pos.x < FIELD_WIDTH - 1:
            righttile = tilemap.get_tile(self.pos.x + 1, self.pos.y)
            if righttile.is_open():
                enviroment["right_tile_empty"] = 1
                enviroment["right_tile_food"] = 0
                enviroment["right_tile_bac"] = 0
            elif righttile.food != None:
                enviroment["right_tile_empty"] = 0
                enviroment["right_tile_food"] = 1
                enviroment["right_tile_bac"] = 0
            elif righttile.bacteria != None:
                enviroment["right_tile_empty"] = 0
                enviroment["right_tile_food"] = 0
                enviroment["right_tile_bac"] = 1
        else:
            enviroment["right_tile_empty"] = 0
            enviroment["right_tile_food"] = 0
            enviroment["right_tile_bac"] = 0

        return enviroment

    def update_self(self) -> None:
        self.max_age = self.genome.max_age
        self.food_for_reproduction = self.genome.food_for_reproduction
        self.color = self.genome.color
        self.can_kill = self.genome.can_kill

    def move(self, tilemap, FIELD_WIDTH, FIELD_HEIGHT) -> None:
        target_tile = self.get_random_open_adjecent_tile(
            tilemap, FIELD_WIDTH, FIELD_HEIGHT)
        if target_tile == None: return None
        old_tile = tilemap.get_tile_by_pos(self.pos)
        old_tile.bacteria = None
        self.pos = Position(target_tile.pos.x, target_tile.pos.y)
        new_tile = tilemap.get_tile_by_pos(self.pos)
        new_tile.bacteria = self

    def devide(self, tilemap, FIELD_WIDTH, FIELD_HEIGHT):

        target_tile = self.get_random_open_adjecent_tile(
            tilemap, FIELD_WIDTH, FIELD_HEIGHT)
        if target_tile == None: return None
        new_bac = Bacteria(
            self.id, target_tile.pos,
            Genome(self.color, self.max_age, self.food_for_reproduction,
                   self.can_kill))

        target_tile.bacteria = new_bac

        return new_bac

    """
    need to register food and bacteria to the tile so we dont need to loop all the food and bacteria
    """

    def kill_adjecent_bacteria(self, bacteria, tilemap):

        for bac in bacteria:
            if self.pos.is_adjacent_to(bac.pos) == True:
                self.food_eaten += 1
                bacteria_tile = tilemap.get_tile_by_pos(bac.pos)
                bacteria.remove(bac)
                bacteria_tile.bacteria = None

    def eat(self, foods) -> None:

        for food in foods:
            if self.pos.is_adjacent_to(food.pos) == True:
                self.food_eaten += 1
                food.stock -= 1

    def get_adjecent_bacteria(self, tilemap, FIELD_WIDTH,
                              FIELD_HEIGHT) -> list[Tile]:
        possible_directions = self.get_possible_directions(
            FIELD_WIDTH, FIELD_HEIGHT)
        adjecent_bacteria = []
        for direction in possible_directions:
            if direction == "up":
                target_tile = tilemap.get_tile(self.pos.x, self.pos.y - 1)
            if direction == "down":
                target_tile = tilemap.get_tile(self.pos.x, self.pos.y + 1)
            if direction == "left":
                target_tile = tilemap.get_tile(self.pos.x - 1, self.pos.y)
            if direction == "right":
                target_tile = tilemap.get_tile(self.pos.x + 1, self.pos.y)
            if target_tile.is_bacteria():
                adjecent_bacteria.append(target_tile)

        return adjecent_bacteria

    def get_random_direction(self, FIELD_WIDTH, FIELD_HEIGHT) -> str:

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
                                      FIELD_HEIGHT) -> Tile:
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

    def get_possible_directions(self, FIELD_WIDTH, FIELD_HEIGHT) -> list:

        if self.pos.x > 0 and self.pos.x < FIELD_WIDTH - 1 and self.pos.y > 0 and self.pos.y < FIELD_HEIGHT - 1:
            possible_directions = ["up", "down", "left", "right"]

        #checks if input location is in a corner
        elif self.pos.x <= 0 and self.pos.y <= 0:
            possible_directions = ["down", "right"]
        elif self.pos.x <= 0 and self.pos.y >= FIELD_HEIGHT - 1:
            possible_directions = ["up", "right"]
        elif self.pos.x >= FIELD_WIDTH - 1 and self.pos.y <= 0:
            possible_directions = ["down", "left"]
        elif self.pos.x >= FIELD_WIDTH - 1 and self.pos.y >= FIELD_HEIGHT - 1:
            possible_directions = ["up", "left"]

        #if input location is on a edge
        elif self.pos.x <= 0:
            possible_directions = ["up", "down", "right"]
        elif self.pos.x >= FIELD_WIDTH - 1:
            possible_directions = ["up", "down", "left"]
        elif self.pos.y <= 0:
            possible_directions = ["down", "left", "right"]
        elif self.pos.y >= FIELD_HEIGHT - 1:
            possible_directions = ["up", "left", "right"]

        return possible_directions

    def check_survival(self) -> bool:
        if self.max_age < self.age:
            return False
        else:
            return True

    def update_age(self) -> None:
        self.age += 1
