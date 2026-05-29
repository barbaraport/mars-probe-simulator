from app.domain.probe.commands.command import Command
from app.domain.probe.commands.move_command import Move
from app.domain.probe.commands.turn_left_command import TurnLeft
from app.domain.probe.commands.turn_right_command import TurnRight
from app.domain.probe.exceptions import InvalidCommandError


class CommandFactory:
    @staticmethod
    def create(command: str) -> Command:
        commands: dict[str, Command] = {
            "M": Move(),
            "L": TurnLeft(),
            "R": TurnRight(),
        }

        if command not in commands:
            raise InvalidCommandError(
                f"The command '{command}' does not exist. The existent commands are: {', '.join(commands.keys())}"
            )

        return commands[command]
