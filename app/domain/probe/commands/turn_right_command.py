from app.domain.probe.commands.command import Command
from app.domain.probe.entities.grid import Grid
from app.domain.probe.entities.probe import Probe
from app.schemas.direction import Direction


class TurnRight(Command):
    def execute(self, probe: Probe, grid: Grid) -> Probe:
        directions = {
            Direction.NORTH: Direction.EAST,
            Direction.SOUTH: Direction.WEST,
            Direction.EAST: Direction.SOUTH,
            Direction.WEST: Direction.NORTH,
        }

        new_direction = directions[probe.direction]
        new_probe = Probe(x=probe.x, y=probe.y, direction=new_direction)

        return new_probe
