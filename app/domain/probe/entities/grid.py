from app.domain.probe.exceptions import InvalidSizeError


class Grid:
    def __init__(self, x_size: int, y_size: int):
        if x_size < 0:
            raise InvalidSizeError(f"X ({x_size}) must be a positive integer.")

        if y_size < 0:
            raise InvalidSizeError(f"Y ({y_size}) must be a positive integer.")

        if x_size == 0 and y_size == 0:
            raise InvalidSizeError(
                f"At least one value ({x_size}, {y_size}) must be greater than zero."
            )

        self.x_size = x_size
        self.y_size = y_size

    def is_movement_inside_grid_limits(self, x: int, y: int) -> bool:
        return 0 <= x <= self.x_size and 0 <= y <= self.y_size
