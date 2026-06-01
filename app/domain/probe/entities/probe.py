from app.domain.probe.exceptions import InvalidCoordinateError
from app.schemas.direction import Direction


class Probe:
    def __init__(self, x: int, y: int, direction: Direction):
        if x < 0:
            raise InvalidCoordinateError(f"{x} (X value) is not a positive integer")

        if y < 0:
            raise InvalidCoordinateError(f"{y} (Y value) is not a positive integer")

        self.x = x
        self.y = y
        self.direction = direction
