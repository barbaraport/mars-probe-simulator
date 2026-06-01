import pytest
from app.domain.probe.commands.move_command import Move
from app.domain.probe.entities.grid import Grid
from app.domain.probe.entities.probe import Probe
from app.domain.probe.exceptions import InvalidMovementError
from app.schemas.direction import Direction


def test_when_creating_valid_move_command_then_should_move_correctly():
    probe = Probe(x=3, y=3, direction=Direction.WEST)
    grid = Grid(x_size=6, y_size=6)

    new_probe = Move().execute(probe, grid)

    assert new_probe.x == 2
    assert new_probe.y == 3
    assert new_probe.direction == Direction.WEST


@pytest.mark.parametrize(
    ("probe_new_x", "probe_new_y", "probe_new_direction"),
    [
        (0, 3, Direction.NORTH),  # top-left corner, up (north)
        (1, 3, Direction.NORTH),  # top corner, up (north)
        (2, 3, Direction.NORTH),  # top corner, up (north)
        (3, 3, Direction.NORTH),  # top-right corner, up (north)
        (3, 3, Direction.EAST),  # top-right corner, right (east)
        (3, 2, Direction.EAST),  # right corner, right (east)
        (3, 1, Direction.EAST),  # right corner, right (east)
        (3, 0, Direction.EAST),  # bottom-right corner, right (east)
        (3, 0, Direction.SOUTH),  # bottom-right corner, down (south)
        (2, 0, Direction.SOUTH),  # bottom corner, down (south)
        (1, 0, Direction.SOUTH),  # bottom corner, down (south)
        (0, 0, Direction.SOUTH),  # bottom-left corner, down (south)
        (0, 0, Direction.WEST),  # bottom-left corner, left (west)
        (0, 1, Direction.WEST),  # left corner, left (west)
        (0, 2, Direction.WEST),  # left corner, left (west)
        (0, 3, Direction.WEST),  # top-left corner, left (west)
    ],
)
def test_when_moving_outside_limits_then_should_raise_invalid_movement_error(
    probe_new_x: int, probe_new_y: int, probe_new_direction: Direction
):
    probe = Probe(x=probe_new_x, y=probe_new_y, direction=probe_new_direction)
    grid = Grid(x_size=3, y_size=3)

    with pytest.raises(InvalidMovementError) as exc_info:
        Move().execute(probe, grid)

    assert (
        str(exc_info.value)
        == f"Movement outside grid limits. The probe must not exceed the grid size of ({grid.x_size}, {grid.y_size})."
    )
