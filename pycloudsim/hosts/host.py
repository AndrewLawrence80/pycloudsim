from ..resources import Pe, RAM, Storage, Bandwidth
from typing import List
from uuid import UUID, uuid1


class Host:
    """
    A Host is a physical machine composed of computing resources
    such as Pe, RAM, bandwidth, storage, etc. 
    In cloud computing scenarios, hosts are grouped together to form datacenters
    and also basic unit to place a virtual machine (Vm)
    """

    def __init__(self, pe_list: List[Pe], id: int = -1, size_ram: int = 32*1024, size_storage: int = 1024*1024, size_bandwidth: int = int(10*103)) -> None:
        """
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
        self.pe_list = pe_list
        self.num_pes = len(self.pe_list)
        self.num_available_pes = self.num_pes
        self.id = id
        self.ram = RAM(size_ram)
        self.storage = Storage(size_storage)
        self.bandwidth = Bandwidth(size_bandwidth)
        self.vm_dict = {}

    def get_uuid(self) -> UUID:
        return self.uuid

    def get_num_pes(self) -> int:
        return self.num_pes

    def get_num_available_pes(self) -> int:
        return self.num_available_pes

    def get_id(self) -> int:
        return self.id

    def get_pe_list(self) -> List[Pe]:
        return self.pe_list

    def get_ram(self) -> RAM:
        return self.ram

    def get_storage(self) -> Storage:
        return self.storage

    def get_bandwidth(self) -> Bandwidth:
        return self.bandwidth

    def bind_vm(self, vm) -> None:
        self.num_available_pes -= vm.get_num_pes()
        self.ram.allocate(vm.get_size_ram())
        self.storage.allocate(vm.get_size_storage())
        self.bandwidth.allocate(vm.get_size_bandwidth())
        self.vm_dict[vm.get_uuid()] = vm
