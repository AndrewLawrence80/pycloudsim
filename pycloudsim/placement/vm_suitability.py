from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..vms import VmRunning
    from ..cloudlets import CloudletRunning


class VmSuitability:
    def __init__(self, vm_running: VmRunning) -> None:
        self.vm_running = vm_running
        self.suitability = False

    def update_suitability(self, target: CloudletRunning) -> None:
        self.suitability = False
        if (
            target.get_num_pes() <= self.vm_running.get_num_pes_available() and
            target.get_required_ram() <= self.vm_running.get_ram().get_size_available() and
            target.get_required_storage() <= self.vm_running.get_storage().get_size_available() and
            target.get_required_bandwidth() <= self.vm_running.get_bandwidth().get_size_available()
        ):
            self.suitability = True

    def get_suitability(self) -> bool:
        return self.suitability

    def get_vm_running(self) -> VmRunning:
        return self.vm_running
