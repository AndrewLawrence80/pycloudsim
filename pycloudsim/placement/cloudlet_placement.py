from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import List, Tuple
    from ..vms import VmRunning
    from ..cloudlets import CloudletRunning


class CloudletPlacement:
    def try_to_place(self, source: List[VmRunning], target: List[CloudletRunning]) -> Tuple[bool, List[CloudletRunning]]:
        pass