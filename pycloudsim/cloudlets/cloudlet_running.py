from __future__ import annotations
from uuid import UUID
from .clouldlet import Cloudlet
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from ..vms import VmRunning


class CloudletRunning(Cloudlet):
    def __init__(self, cloudlet: Cloudlet) -> None:
        self.cloudlet = cloudlet
        self.vm_running = None
        
    def get_cloudlet(self)->Cloudlet:
        return self.cloudlet

    def get_uuid(self) -> UUID:
        return self.cloudlet.get_uuid()

    def get_id(self) -> int:
        return self.cloudlet.get_id()

    def get_length(self) -> float:
        return self.cloudlet.get_length()

    def get_num_pes(self) -> int:
        return self.cloudlet.get_num_pes()

    def get_utilization_pe(self) -> float:
        return self.cloudlet.get_utilization_pe()

    def get_required_ram(self) -> float:
        return self.cloudlet.get_required_ram()

    def get_required_storage(self) -> float:
        return self.cloudlet.get_required_storage()

    def get_required_bandwidth(self) -> float:
        return self.cloudlet.get_required_bandwidth()

    def get_state(self) -> Cloudlet.State:
        return self.cloudlet.get_state()

    def set_state(self, state: Cloudlet.State):
        self.cloudlet.set_state(state)

    def get_start_time(self) -> float:
        return self.cloudlet.get_start_time()

    def set_start_time(self, start_time: float) -> None:
        self.cloudlet.set_start_time(start_time)

    def get_end_time(self) -> float:
        return self.cloudlet.get_end_time()

    def set_end_time(self, end_time: float) -> None:
        self.cloudlet.set_end_time(end_time)

    def get_vm_uuid(self) -> UUID:
        return self.cloudlet.get_vm_uuid()

    def set_vm_running(self, vm_running: VmRunning) -> None:
        self.vm_running = vm_running
        if vm_running is not None:
            self.cloudlet.set_vm_uuid(vm_running.get_uuid())

    def get_vm_running(self) -> Optional[VmRunning]:
        return self.vm_running
