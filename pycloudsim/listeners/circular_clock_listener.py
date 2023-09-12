from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..simulation import Simulator


class CircularClockListener:
    def __init__(self, cicular_interval: float) -> None:
        self.circular_interval = cicular_interval

    def update(simulator) -> None:
        pass

    def get_circular_interval(self) -> float:
        return self.circular_interval
