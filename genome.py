class Genome:
    def __init__(self) -> None:
        self.id = id
        self.color = 150, 70, 70
        self.max_age = 100
        self.food_for_reproduction = 5
        self.vision = False

    def __str__(self) -> str:
        return f"BacteriaGenome id: {self.id}"