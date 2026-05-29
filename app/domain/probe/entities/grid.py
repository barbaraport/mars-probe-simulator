class Grid:
    def __init__(self, x_size: int, y_size: int):
        self.x_size = x_size
        self.y_size = y_size

    def is_movement_inside_grid_limits(self, x: int, y: int) -> bool:
        return 0 <= x <= self.x_size and 0 <= y <= self.y_size
