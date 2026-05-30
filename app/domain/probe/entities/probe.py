from app.schemas.direction import Direction


class Probe:
    def __init__(self, x: int, y: int, direction: Direction):
        self.x = x
        self.y = y
        self.direction = direction
