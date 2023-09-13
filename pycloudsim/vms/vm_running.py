from __future__ import annotations
from uuid import UUID
from .vm import Vm
from ..cloudlets import CloudletRunning
from ..resources import Pe
from collections import defaultdict
from typing import Dict, List, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from resources import RAM, Bandwidth, Storage
    from ..hosts import Host
    from ..cloudlets import Cloudlet
    from uuid import UUID


class VmRunning(Vm):
    def __init__(self, vm: Vm):
        self.vm = vm
        self.mips = 0.0
        self.num_pes_available = vm.get_num_pes()
        self.vm_pe_dict = {}
        self.ram = None
        self.storage = None
        self.bandwidth = None
        self.is_scheduled_to_shutdown = False
        self.cloudlet_running_pe_dict = defaultdict(list)
        self.cloudlet_running_dict = {}
        self.host = None

    def get_vm(self) -> Vm:
        return self.vm

    def get_uuid(self) -> UUID:
        return self.vm.get_uuid()

    def get_id(self) -> int:
        return self.vm.get_id()

    def get_host_mips_factor(self) -> float:
        return self.vm.get_host_mips_factor()

    def get_num_pes(self) -> int:
        return self.vm.get_num_pes()

    def get_size_ram(self) -> float:
        return self.vm.get_size_ram()

    def get_size_storage(self) -> float:
        return self.vm.get_size_storage()

    def get_size_bandwidth(self) -> float:
        return self.vm.get_size_bandwidth()

    def get_startup_delay(self) -> float:
        return self.vm.get_startup_delay()

    def get_shutdown_delay(self) -> float:
        return self.vm.get_shutdown_delay()

    def get_state(self) -> Vm.State:
        return self.state

    def set_state(self, state: Vm.State):
        self.vm.set_state(state)

    def get_host_uuid(self) -> UUID:
        return self.vm.get_host_uuid()

    def get_mips(self) -> float:
        return self.mips

    def set_mips(self, mips: float) -> None:
        self.mips = mips

    def get_num_pes_available(self) -> int:
        return self.num_pes_available

    def get_vm_pe_dict(self) -> Dict[UUID, Pe]:
        return self.vm_pe_dict

    def add_vm_pe(self, pe: Pe) -> None:
        self.vm_pe_dict[pe.get_uuid()] = pe

    def get_ram(self) -> RAM:
        return self.ram

    def set_ram(self, ram: RAM) -> None:
        self.ram = ram

    def get_storage(self) -> Storage:
        return self.storage

    def set_storage(self, storage: Storage) -> None:
        self.storage = storage

    def get_bandwidth(self) -> Bandwidth:
        return self.bandwidth

    def set_bandwidth(self, bandwidth: Bandwidth) -> None:
        self.bandwidth = bandwidth

    def set_is_scheduled_to_shutdown(self, is_scheduled_to_shutdown: bool) -> None:
        self.is_scheduled_to_shutdown = is_scheduled_to_shutdown

    def get_is_scheduled_to_shutdown(self) -> bool:
        return self.is_scheduled_to_shutdown

    def bind_cloudlet(self, cloudlet_running: CloudletRunning) -> None:
        for _ in range(cloudlet_running.get_num_pes()):
            for vm_pe in self.vm_pe_dict.values():
                if vm_pe.get_state() == Pe.State.FREE:
                    vm_pe.set_state(Pe.State.BUSY)
                    vm_pe.allocate(cloudlet_running.get_utilization_pe())
                    self.cloudlet_running_pe_dict[cloudlet_running.get_uuid()].append(vm_pe.get_uuid())
                    host_pe = self.host.get_host_pe_dict()[self.host.get_vm_pe_mapping()[vm_pe.get_uuid()]]
                    host_pe.allocate(cloudlet_running.get_utilization_pe())
                    break
        self.num_pes_available -= cloudlet_running.get_num_pes()

        self.ram.allocate(cloudlet_running.get_required_ram())

        self.storage.allocate(cloudlet_running.get_required_storage())

        self.bandwidth.allocate(cloudlet_running.get_required_bandwidth())

        self.cloudlet_running_dict[cloudlet_running.get_uuid()] = cloudlet_running

        cloudlet_running.set_vm_running(self)

    def release_cloudlet(self, cloudlet_running: CloudletRunning) -> None:
        cloudlet_running.set_vm_running(None)

        self.cloudlet_running_dict.pop(cloudlet_running.get_uuid())

        self.bandwidth.dealloate(cloudlet_running.get_required_bandwidth())

        self.storage.dealloate(cloudlet_running.get_required_storage())

        self.ram.dealloate(cloudlet_running.get_required_ram())
        
        self.num_pes_available += cloudlet_running.get_num_pes()

        pe_uuid_list = self.cloudlet_running_pe_dict.pop(cloudlet_running.get_uuid())
        for pe_uuid in pe_uuid_list:
            self.vm_pe_dict[pe_uuid].set_state(Pe.State.FREE)
            self.vm_pe_dict[pe_uuid].deallocate(cloudlet_running.get_utilization_pe())
            host_pe = self.host.get_host_pe_dict()[self.host.get_vm_pe_mapping()[pe_uuid]]
            host_pe.deallocate(cloudlet_running.get_utilization_pe())
        

    def get_cloudlet_running_pe_dict(self) -> Dict[UUID, List[Pe]]:
        return self.cloudlet_running_pe_dict

    def get_cloudlet_running_dict(self) -> Dict[UUID, CloudletRunning]:
        return self.cloudlet_running_dict

    def get_host(self) -> Optional[Host]:
        return self.host

    def set_host(self, host: Host):
        self.host = host
        self.vm.set_host_uuid(host.get_uuid())
