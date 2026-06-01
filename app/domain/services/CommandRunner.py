from app.domain.probe.commands.factory import CommandFactory
from app.domain.probe.entities.grid import Grid
from app.domain.probe.entities.probe import Probe


class CommandRunner:
    def __init__(self, grid: Grid):
        self.grid = grid

    def run(self, probe: Probe, commands: str) -> Probe:
        new_probe = Probe(x=probe.x, y=probe.y, direction=probe.direction)

        for command_str in commands:
            command = CommandFactory.create(command_str)
            new_probe = command.execute(new_probe, self.grid)

        return new_probe
