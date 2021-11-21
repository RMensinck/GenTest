from typing import List


class TileGrid:
    def __init__(self, width, height, grid_size):
        self.grid_size = grid_size
        self.width = width
        self.height = height
        self.map: List[List[Tile]] = [None] * width
        for x in range(0, self.width):
            self.map[x] = [None] * height
            for y in range(0, self.height):
                self.map[x][y] = Tile(x, y)

    def __str__(self):
        return f"The Grid"

    def get_tile(self, x, y):
        return self.map[x][y]


class Pos:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"Position x:{self.x} y:{self.y}"


class Tile:
    def __init__(self, x, y) -> None:
        self.pos = Pos(x, y)
        self.bacteria = False
        self.wall = False

    def __str__(self) -> str:
        return f"Tile of position {self.pos.x},{self.pos.y}"

    def is_wall(self):
        return self.wall

    def is_bacteria(self):
        return self.bacteria

    def is_open(self):
        return self.bacteria == False and self.wall == False


class Wall:
    def __init__(self, id, x, y) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.color = 0, 0, 0

    def __str__(self) -> str:
        return f"Wall id: {self.id}"


class Border:
    def __init__(self, color, field_width, field_hight):
        self.color = color
        self.width = 1
        self.start_x = 0
        self.start_y = 0
        self.final_x = field_width
        self.final_y = field_hight

    def __str__(self) -> str:
        return f"object to draw borders"
