from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Dict
if TYPE_CHECKING:
    from typing import Dict,List,Tuple
    from ..hosts import Host
    from ..vms import VmRunning


class VmPlacement:
    def try_to_place(self, source: List[Host], target: List[VmRunning]) -> Tuple[bool,List[VmRunning]]:
        pass
