import pytest

from app.domain.probe.entities.grid import Grid
from app.domain.probe.entities.probe import Probe
from app.domain.probe.exceptions import InvalidCommandError, InvalidMovementError
from app.domain.services.CommandRunner import CommandRunner
from app.schemas.direction import Direction


def test_when_giving_valid_command_then_should_execute_commands_correctly():
    grid = Grid(x_size=5, y_size=5)
    probe = Probe(x=0, y=0, direction=Direction.NORTH)

    command_runner = CommandRunner(grid)
    new_probe = command_runner.run(probe, "MRM")

    assert new_probe.x == 1
    assert new_probe.y == 1
    assert new_probe.direction == Direction.EAST


def test_when_giving_invalid_command_in_the_middle_should_raise_exception():
    grid = Grid(x_size=5, y_size=5)
    probe = Probe(x=0, y=0, direction=Direction.NORTH)

    with pytest.raises(InvalidCommandError) as exc_info:
        command_runner = CommandRunner(grid)
        command_runner.run(probe, "MMYM")

    assert (
        str(exc_info.value)
        == "The command 'Y' does not exist. The existent commands are: M, L, R."
    )


def test_when_giving_outside_bounds_commands_should_raise_exception():
    grid = Grid(x_size=5, y_size=5)
    probe = Probe(x=0, y=0, direction=Direction.NORTH)

    with pytest.raises(InvalidMovementError) as exc_info:
        command_runner = CommandRunner(grid)
        command_runner.run(probe, "MMMMMM")  # 6 times -> outside boundary

    assert (
        str(exc_info.value)
        == "Movement outside grid limits. The probe must not exceed the grid size of (5, 5)."
    )
