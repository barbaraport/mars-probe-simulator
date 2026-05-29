from app.domain.probe.commands.factory import CommandFactory
from app.domain.probe.entities.grid import Grid
from app.domain.probe.entities.probe import Probe


class CommandRunner:
    def __init__(self, grid: Grid):
        self.grid = grid

    def run(self, probe: Probe, commands: str):
        for command_str in commands:
            command = CommandFactory.create(command_str)
            command.execute(probe, self.grid)

        return probe
