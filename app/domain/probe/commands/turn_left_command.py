from app.domain.probe.commands.command import Command
from app.domain.probe.entities.direction import Direction
from app.domain.probe.entities.grid import Grid
from app.domain.probe.entities.probe import Probe


class TurnLeft(Command):
    def execute(self, probe: Probe, grid: Grid):
        directions = {
            Direction.NORTH: Direction.WEST,
            Direction.SOUTH: Direction.EAST,
            Direction.EAST: Direction.NORTH,
            Direction.WEST: Direction.SOUTH,
        }

        new_direction = directions[probe.direction]
        probe.direction = new_direction
