from __future__ import annotations
from enum import Enum
from uuid import uuid1
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from uuid import UUID


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
        self.size_ram = 1.0*size_ram
        self.size_storage = 1.0*size_storage
        self.size_bandwidth = 1.0*size_bandwidth
        self.startup_delay = 0.0
        self.shudown_delay = 0.0
        self.state = Vm.State.CREATED
        self.host_uuid = None

    def get_uuid(self) -> UUID:
        return self.uuid

    def get_id(self) -> int:
        return self.id

    def get_host_mips_factor(self) -> float:
        return self.host_mips_factor

    def get_num_pes(self) -> int:
        return self.num_pes

    def get_size_ram(self) -> float:
        return self.size_ram

    def get_size_storage(self) -> float:
        return self.size_storage

    def get_size_bandwidth(self) -> float:
        return self.size_bandwidth

    def get_startup_delay(self) -> float:
        return self.startup_delay

    def set_startup_delay(self, delay: float) -> None:
        self.startup_delay = delay

    def get_shutdown_delay(self) -> float:
        return self.shudown_delay

    def set_shutdown_delay(self, delay: float) -> None:
        self.shudown_delay = delay

    def get_state(self) -> State:
        return self.state

    def set_state(self, state: State):
        self.state = state

    def get_host_uuid(self) -> UUID:
        return self.host_uuid

    def set_host_uuid(self, uuid: UUID) -> None:
        self.host_uuid = uuid
