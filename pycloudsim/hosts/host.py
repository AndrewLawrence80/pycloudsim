from __future__ import annotations
from uuid import UUID, uuid1
from collections import defaultdict
from ..resources import Pe, RAM, Storage, Bandwidth
from typing import List, Dict
from typing import TYPE_CHECKING
from ..vms import VmRunning
if TYPE_CHECKING:
    from ..datacenters import Datacenter
    from ..vms import Vm


class Host:
    def __init__(self, pe_list: List[Pe], id: int = -1, size_ram: int = 32*1024, size_storage: int = 1024*1024, size_bandwidth: int = int(10*103)) -> None:
        """
        A Host is a physical machine composed of computing resources
        such as Pe, RAM, bandwidth, storage, etc. 
        In cloud computing scenarios, hosts are grouped together to form datacenters
        and also basic unit to place a virtual machine (Vm)
        
        Parameters
        ----------
        pe_list: List[Pe]
            List of CPU cores, better be homogenous, that is all Pes have same rate in MIPS
        id: int
            It is recommended to assign an id for each host for better summary
        size_ram: int
            RAM size of host in MB, default 32 GB
        size_storage: int
            Storage size of host in MB, default 1 TB
        size_bandwidth: int
            Bandwidth of host in MB, default 10 Gbps
        """
        self.uuid = uuid1()
        self.id = id
        self.num_pes = len(pe_list)
        self.num_pes_available = self.num_pes
        self.host_pe_dict = self._build_pe_dict(pe_list)
        self.vm_pe_mapping = {}
        self.vm_pe_dict = defaultdict(list)
        self.ram = RAM(size_ram)
        self.vm_ram_dict = {}
        self.storage = Storage(size_storage)
        self.vm_storage_dict = {}
        self.bandwidth = Bandwidth(size_bandwidth)
        self.vm_bandwidth_dict = {}
        self.vm_running_dict = {}
        self.datacenter = None

    def _build_pe_dict(self, pe_list: List[Pe]) -> Dict[UUID, Pe]:
        pe_dict = {}
        for pe in pe_list:
            pe_dict[pe.get_uuid()] = pe
        return pe_dict

    def get_uuid(self) -> UUID:
        return self.uuid

    def get_id(self) -> int:
        return self.id

    def get_num_pes(self) -> int:
        return self.num_pes

    def get_num_pes_available(self) -> int:
        return self.num_pes_available

    def get_host_pe_dict(self) -> Dict[UUID, Pe]:
        return self.host_pe_dict

    def get_vm_pe_mapping(self) -> Dict[UUID, UUID]:
        return self.vm_pe_mapping

    def get_vm_pe_dict(self) -> Dict[UUID, List[UUID]]:
        return self.vm_pe_dict

    def get_ram(self) -> RAM:
        return self.ram

    def get_vm_ram_dict(self) -> Dict[UUID, RAM]:
        return self.vm_ram_dict

    def get_storage(self) -> Storage:
        return self.storage

    def get_vm_storage_dict(self) -> Dict[UUID, Storage]:
        return self.vm_storage_dict

    def get_bandwidth(self) -> Bandwidth:
        return self.bandwidth

    def get_vm_bandwidth_dict(self) -> Dict[UUID, Bandwidth]:
        return self.vm_bandwidth_dict

    def get_vm_running_dict(self) -> Dict[UUID, VmRunning]:
        return self.vm_running_dict

    def bind_vm(self, vm_running: VmRunning) -> None:
        for _ in range(vm_running.get_num_pes()):
            for host_pe in self.host_pe_dict.values():
                if host_pe.get_state() == Pe.State.FREE:
                    host_pe.set_state(Pe.State.BUSY)
                    # create virtual pe for vm
                    vm_pe = Pe(vm_running.get_host_mips_factor() * host_pe.get_mips_capacity())
                    # construct vm and host pe mapping
                    self.vm_pe_mapping[vm_pe.get_uuid()] = host_pe.get_uuid()
                    # assign virutal pe to vm
                    self.vm_pe_dict[vm_running.get_uuid()].append(vm_pe.get_uuid())
                    vm_running.add_vm_pe(vm_pe)
                    break
        self.num_pes_available -= vm_running.get_num_pes()
        vm_pe=list(vm_running.get_vm_pe_dict().values())[0]
        vm_running.set_mips(vm_pe.get_mips_capacity())

        vm_ram = RAM(vm_running.get_size_ram())
        self.ram.allocate(vm_ram.get_size_capacity())
        self.vm_ram_dict[vm_ram.get_uuid()] = vm_ram
        vm_running.set_ram(vm_ram)

        vm_storage = Storage(vm_running.get_size_storage())
        self.storage.allocate(vm_storage.get_size_capacity())
        self.vm_storage_dict[vm_storage.get_uuid()] = vm_storage
        vm_running.set_storage(vm_storage)

        vm_bandwidth = Bandwidth(vm_running.get_size_bandwidth())
        self.bandwidth.allocate(vm_bandwidth.get_size_capacity())
        self.vm_bandwidth_dict[vm_bandwidth.get_uuid()] = vm_bandwidth
        vm_running.set_bandwidth(vm_bandwidth)

        self.vm_running_dict[vm_running.get_uuid()] = vm_running
        vm_running.set_host(self)

    def release_vm(self, vm_running: VmRunning) -> None:
        vm_running.set_host(None)
        
        self.vm_running_dict.pop(vm_running.get_uuid())

        self.vm_bandwidth_dict.pop(vm_running.get_bandwidth().get_uuid())
        self.bandwidth.dealloate(vm_running.get_bandwidth().get_size_capacity())
        vm_running.set_bandwidth(None)

        self.vm_storage_dict.pop(vm_running.get_storage().get_uuid())
        self.storage.dealloate(vm_running.get_storage().get_size_capacity())
        vm_running.set_storage(None)

        self.vm_ram_dict.pop(vm_running.get_ram().get_uuid())
        self.ram.dealloate(vm_running.get_ram().get_size_capacity())
        vm_running.set_ram(None)

        vm_running.get_vm_pe_dict().clear()
        self.num_pes_available += vm_running.get_num_pes()
        vm_pe_uuid_list = self.vm_pe_dict.pop(vm_running.get_uuid())
        for vm_pe_uuid in vm_pe_uuid_list:
            self.host_pe_dict[self.vm_pe_mapping[vm_pe_uuid]].set_state(Pe.State.FREE)
            self.vm_pe_mapping.pop(vm_pe_uuid)

    def get_datacenter(self):
        return self.datacenter

    def set_datacenter(self, datacenter: Datacenter):
        self.datacenter = datacenter
