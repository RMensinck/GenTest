from sim_terrain import Pos


class Food:
    def __init__(self, pos) -> None:
        self.stock = 10
        self.color = 20, 30, 180
        self.pos = pos

    def __str__(self) -> str:
        return f"food class"

    def check_stock_left(self) -> bool:
        if self.stock > 0:
            return True
        else:
            return False
