from app.domain.probe.commands.command import Command
from app.domain.probe.entities.grid import Grid
from app.domain.probe.entities.probe import Probe
from app.domain.probe.exceptions import InvalidMovementError
from app.schemas.direction import Direction


class Move(Command):
    def execute(self, probe: Probe, grid: Grid) -> Probe:
        movements = {
            Direction.NORTH: (0, 1),  # NORTH -> y -> +1
            Direction.SOUTH: (0, -1),  # SOUTH -> y -> -1
            Direction.EAST: (1, 0),  # EAST -> x -> +1
            Direction.WEST: (-1, 0),  # WEST -> x -> -1
        }

        x_move, y_move = movements[probe.direction]

        new_x_position = probe.x + x_move
        new_y_position = probe.y + y_move

        if not grid.is_movement_inside_grid_limits(new_x_position, new_y_position):
            raise InvalidMovementError(
                f"Movement outside grid limits. The probe must not exceed the grid size of ({grid.x_size}, {grid.y_size})."
            )

        new_probe = Probe(x=new_x_position, y=new_y_position, direction=probe.direction)

        return new_probe
