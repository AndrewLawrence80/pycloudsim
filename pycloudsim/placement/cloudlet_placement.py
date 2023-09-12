from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Dict
if TYPE_CHECKING:
    from typing import List, Dict
    from ..vms import Vm
    from ..cloudlets import Cloudlet
    from uuid import UUID


class CloudletPlacement:
    def git_fit_map(self, source: List[Vm], target: List[Cloudlet]) -> Optional[Dict]:
        pass
