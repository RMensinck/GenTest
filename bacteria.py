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

    def move(self):
        direction = random.choice(["up", "down", "left", "right"])
        if direction == "up":
            self.pos.y -= 1
        if direction == "down":
            self.pos.y += 1
        if direction == "right":
            self.pos.x += 1
        if direction == "left":
            self.pos.x -= 1

    def devide(self):
        return Bacteria(self.id, BacteriaGenome(self.id), self.pos.x + 1,
                        self.pos.y)


class BacteriaGenome:
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return f"BacteriaGenome id: {self.id}"