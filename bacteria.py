from sys import _xoptions

from SimTerrain import Pos


class Bacteria:
    def __init__(self, id, genome, x, y):
        self.id = id
        self.genome = genome
        self.pos = Pos(x, y)
        self.color = 150, 70, 70

    def __str__(self):
        return f"Bacteria id: {self.id}"


class BacteriaGenome:
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return f"BacteriaGenome id: {self.id}"