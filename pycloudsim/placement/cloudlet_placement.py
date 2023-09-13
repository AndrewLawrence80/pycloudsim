from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Dict
if TYPE_CHECKING:
    from typing import List, Dict
    from ..vms import VmRunning
    from ..cloudlets import CloudletRunning


class CloudletPlacement:
    def git_fit_map(self, source: List[VmRunning], target: List[CloudletRunning]) -> Optional[Dict]:
        pass
