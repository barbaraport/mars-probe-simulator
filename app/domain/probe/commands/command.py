from abc import ABC, abstractmethod

from app.domain.probe.entities.probe import Probe
from app.domain.probe.entities.grid import Grid


class Command(ABC):
    @abstractmethod
    def execute(self, probe: Probe, grid: Grid):
        pass
