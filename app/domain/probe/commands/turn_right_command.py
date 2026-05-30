from app.domain.probe.commands.command import Command
from app.domain.probe.entities.grid import Grid
from app.domain.probe.entities.probe import Probe
from app.schemas.direction import Direction


class TurnRight(Command):
    def execute(self, probe: Probe, grid: Grid):
        directions = {
            Direction.NORTH: Direction.EAST,
            Direction.SOUTH: Direction.WEST,
            Direction.EAST: Direction.SOUTH,
            Direction.WEST: Direction.NORTH,
        }

        new_direction = directions[probe.direction]
        probe.direction = new_direction
