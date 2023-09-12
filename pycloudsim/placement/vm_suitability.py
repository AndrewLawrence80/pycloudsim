from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..vms import Vm
    from ..cloudlets import Cloudlet


class VmSuitability:
    def __init__(self, vm: Vm) -> None:
        self.vm = vm
        self.suitability = False

    def update_suitability(self, target: Cloudlet) -> None:
        self.suitability = False
        if (
            target.get_num_pes() <= self.vm.get_num_pes_available() and
            target.get_required_ram() <= self.vm.get_ram().get_size_available() and
            target.get_required_storage() <= self.vm.get_storage().get_size_available() and
            target.get_required_bandwidth() <= self.vm.get_bandwidth().get_size_available()
        ):
            self.suitability = True

    def get_suitability(self) -> bool:
        return self.suitability

    def get_vm(self) -> Vm:
        return self.vm
