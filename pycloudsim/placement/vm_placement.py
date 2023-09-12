from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Dict
if TYPE_CHECKING:
    from typing import List
    from ..hosts import Host
    from ..vms import Vm


class VmPlacement:
    def get_fit_map(self, source: List[Host], target: List[Vm]) -> Optional[Dict]:
        pass
