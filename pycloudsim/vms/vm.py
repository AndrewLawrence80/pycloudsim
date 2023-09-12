from __future__ import annotations
from enum import Enum
from uuid import UUID, uuid1
from collections import defaultdict
from typing import Dict, List, TYPE_CHECKING
from ..cloudlets import Cloudlet
from ..resources import Pe
if TYPE_CHECKING:
    from ..hosts import Host
    from ..resources import RAM, Storage, Bandwidth


class Vm:
    """
    A virtual machine (Vm) is a composed of virtual computing resources
    such as Pe, RAM, bandwidth, storage, etc. provided by Host.
    In cloud computing scenarios, Vms run on a Host assigned by the datacenter Broker
    and execute Cloudlets
    """
    class State(Enum):
        """
        A Vm instance has been created but not submitted to the datacenter Broker yet
        """
        CREATED = 0

        """
        A Vm instance has been created and submitted to the datacenter Broker but has not been bound to any Host yet
        """
        SUBMITTED = 1

        """
        A Vm instance has been bound to a Host but has not booted up yet
        """
        BOUNDED = 2

        """
        A Vm instance has successfully booted up on an assigned Host,
        and has allocated time slice to run
        """
        RUNNING = 3

        """
        A Vm should shutdown first when datacenter scales down vm capacity
        """
        SHUTTINGDOWN = 4

        """
        A Vm destroyed successfully by the datacenter
        """
        DESTROYED = 5

        """
        A Vm exited abnormally by simulation early stopping, crash or fault injection
        """
        FAILED = 6

        """
        A Vm instance will be canceled if there is no suitable Host to bind
        """
        CANCELED = 7

    def __init__(self, id: int = -1, host_mips_factor: float = 1.0, num_pes: int = 1, size_ram: int = 1024, size_storage: int = 10*1024, size_bandwidth: int = 100) -> None:
        """
        Parameters
        ----------
        id: int
            It is recommended to assign an id to the Vm for better summary
        host_mips_factor: float
            The "performance" of vm pe compared with host pe,
            if there is no performance loss, host_mips_factor
            should be set to 1.0
        num_pes: int
            The required number of Pes to run on the Vm
        size_ram: int
            RAM size of Vm in MB, default 1 GB
        size_storage: int
            Storage size of Vm in MB, default 10 GB
        size_bandwidth: int
            Bandwidth of Vm in Mbps, default 100 Mbps
        """

        self.uuid = uuid1()
        self.id = id
        self.host_mips_factor = 1.0*host_mips_factor
        self.num_pes = num_pes
        self.num_pes_available = self.num_pes
        self.vm_pe_dict = {}
        self.cloudlet_pe_dict = defaultdict(list)
        self.size_ram = 1.0*size_ram
        self.size_storage = 1.0*size_storage
        self.size_bandwidth = 1.0*size_bandwidth
        self.ram = None
        self.storage = None
        self.bandwidth = None
        self.startup_delay = 0.0
        self.shudown_delay = 0.0
        self.is_scheduled_to_shutdown=False
        self.state = Vm.State.CREATED

        self.host = None
        self.cloudlet_dict = {}

    def get_uuid(self) -> UUID:
        return self.uuid

    def get_id(self) -> int:
        return self.id

    def get_host_mips_factor(self) -> float:
        return self.host_mips_factor

    def get_num_pes(self) -> int:
        return self.num_pes

    def get_num_pes_available(self) -> int:
        return self.num_pes_available

    def get_vm_pe_dict(self) -> Dict[UUID, Pe]:
        return self.vm_pe_dict

    def add_vm_pe(self, pe: Pe) -> None:
        self.vm_pe_dict[pe.get_uuid()] = pe

    def get_cloudlet_pe_dict(self) -> Dict[UUID, List[Pe]]:
        return self.cloudlet_pe_dict

    def get_size_ram(self) -> float:
        return self.size_ram

    def get_size_storage(self) -> float:
        return self.size_storage

    def get_size_bandwidth(self) -> float:
        return self.size_bandwidth

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

    def get_startup_delay(self) -> float:
        return self.startup_delay

    def set_startup_delay(self, delay: float) -> None:
        self.startup_delay = delay

    def get_shutdown_delay(self) -> float:
        return self.shudown_delay

    def set_shutdown_delay(self, delay: float) -> None:
        self.shudown_delay = delay
        
    def set_is_scheduled_to_shutdown(self,is_scheduled_to_shutdown:bool)->None:
        self.is_scheduled_to_shutdown=is_scheduled_to_shutdown
        
    def get_is_scheduled_to_shutdown(self)->bool:
        return self.is_scheduled_to_shutdown

    def get_state(self) -> State:
        return self.state

    def set_state(self, state: State):
        self.state = state

    def set_host(self, host: Host) -> None:
        self.host = host

    def get_host(self):
        return self.host

    def bind_cloudlet(self, cloudlet: Cloudlet) -> None:
        for _ in range(cloudlet.get_num_pes()):
            for vm_pe in self.vm_pe_dict.values():
                if vm_pe.get_state() == Pe.State.FREE:
                    vm_pe.set_state(Pe.State.BUSY)
                    vm_pe.allocate(cloudlet.get_utilization_pe())
                    self.cloudlet_pe_dict[cloudlet.get_uuid()].append(
                        vm_pe.get_uuid())
                    self.host.get_host_pe_dict()[self.host.get_vm_pe_mapping()[vm_pe.get_uuid()]].allocate(cloudlet.get_utilization_pe())
                    break
        self.num_pes_available-=cloudlet.get_num_pes()
        self.ram.allocate(cloudlet.get_required_ram())
        self.storage.allocate(cloudlet.get_required_storage())
        self.bandwidth.allocate(cloudlet.get_required_bandwidth())
        self.cloudlet_dict[cloudlet.get_uuid()]=cloudlet
        cloudlet.set_vm(self)

    def release_cloudlet(self, cloudlet: Cloudlet) -> None:
        self.bandwidth.dealloate(cloudlet.get_required_bandwidth())
        self.storage.dealloate(cloudlet.get_required_storage())
        self.ram.dealloate(cloudlet.get_required_ram())
        cloudlet_pe_uuid_list=self.cloudlet_pe_dict.pop(cloudlet.get_uuid())
        for cloudlet_pe_uuid in cloudlet_pe_uuid_list:
            self.vm_pe_dict[cloudlet_pe_uuid].set_state(Pe.State.FREE)
            self.vm_pe_dict[cloudlet_pe_uuid].deallocate(cloudlet.get_utilization_pe())
            self.host.get_host_pe_dict()[self.host.get_vm_pe_mapping()[cloudlet_pe_uuid]].deallocate(cloudlet.get_utilization_pe())
        self.num_pes_available+=cloudlet.get_num_pes()
        self.cloudlet_dict.pop(cloudlet.get_uuid())
        cloudlet.set_state(cloudlet.State.SUCCEEDED)

    def get_cloudlet_dict(self) -> Dict:
        return self.cloudlet_dict
