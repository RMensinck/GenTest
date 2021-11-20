class Grid:
    def __init__(self, width, height, grid_size):
        self.grid_size = grid_size
        self.width = width
        self.height = height
        self.tiles = []
        for x in range(0, self.width):
            for y in range(0, self.height):
                self.tiles.append(Pos(x, y))

    def __str__(self):
        return f"The Grid"


class Pos:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"Position x:{self.x} y:{self.y}"


class Wall:
    def __init__(self, id, width, height, start_x, start_y) -> None:
        self.id = id
        self.width = width
        self.height = height
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = self.start_x + width
        self.end_y = self.start_y + height
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
