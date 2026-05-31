import pytest

from app.domain.probe.commands.turn_right_command import TurnRight
from app.domain.probe.entities.grid import Grid
from app.domain.probe.entities.probe import Probe
from app.schemas.direction import Direction


@pytest.mark.parametrize(
    ("old_direction", "new_direction"),
    [
        (Direction.NORTH, Direction.EAST),
        (Direction.EAST, Direction.SOUTH),
        (Direction.SOUTH, Direction.WEST),
        (Direction.WEST, Direction.NORTH),
    ],
)
def test_when_turning_probe_to_the_right_then_should_turn_successfully_and_keep_coordinates(
    old_direction: Direction, new_direction: Direction
):
    probe = Probe(x=5, y=5, direction=old_direction)
    grid = Grid(x_size=5, y_size=5)

    TurnRight().execute(probe, grid)

    assert probe.direction == new_direction
    assert probe.x == 5
    assert probe.y == 5
