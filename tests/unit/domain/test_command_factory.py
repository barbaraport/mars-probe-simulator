import pytest

from app.domain.probe.commands.command import Command
from app.domain.probe.commands.factory import CommandFactory
from app.domain.probe.commands.move_command import Move
from app.domain.probe.commands.turn_left_command import TurnLeft
from app.domain.probe.commands.turn_right_command import TurnRight
from app.domain.probe.exceptions import InvalidCommandError


@pytest.mark.parametrize("command", ["M", "m"])
def test_when_sending_valid_m_command_then_command_should_be_created_successfully(
    command: str,
):
    command_class = CommandFactory.create(command)
    assert isinstance(command_class, Command)
    assert isinstance(command_class, Move)


@pytest.mark.parametrize("command", ["L", "l"])
def test_when_sending_valid_l_command_then_command_should_be_created_successfully(
    command: str,
):
    command_class = CommandFactory.create(command)
    assert isinstance(command_class, Command)
    assert isinstance(command_class, TurnLeft)


@pytest.mark.parametrize("command", ["R", "r"])
def test_when_sending_valid_r_command_then_command_should_be_created_successfully(
    command: str,
):
    command_class = CommandFactory.create(command)
    assert isinstance(command_class, Command)
    assert isinstance(command_class, TurnRight)


@pytest.mark.parametrize("command", ["X", "0", "+"])
def test_when_sending_invalid_command_then_should_raise_error(command: str):
    with pytest.raises(InvalidCommandError) as exc_info:
        CommandFactory.create(command)

    assert (
        str(exc_info.value)
        == f"The command '{command}' does not exist. The existent commands are: M, L, R."
    )
