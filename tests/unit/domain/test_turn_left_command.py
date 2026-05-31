import pytest

from app.domain.probe.commands.turn_left_command import TurnLeft
from app.domain.probe.entities.grid import Grid
from app.domain.probe.entities.probe import Probe
from app.schemas.direction import Direction


@pytest.mark.parametrize(
    ("old_direction", "new_direction"),
    [
        (Direction.NORTH, Direction.WEST),
        (Direction.WEST, Direction.SOUTH),
        (Direction.SOUTH, Direction.EAST),
        (Direction.EAST, Direction.NORTH),
    ],
)
def test_when_turning_probe_to_the_left_then_should_turn_successfully_and_keep_coordinates(
    old_direction: Direction, new_direction: Direction
):
    probe = Probe(x=3, y=3, direction=old_direction)
    grid = Grid(x_size=5, y_size=5)

    TurnLeft().execute(probe, grid)

    assert probe.direction == new_direction
    assert probe.x == 3
    assert probe.y == 3
