from enum import Enum
from ..resources import Pe
from ..resources import RAM
from ..resources import Storage
from ..resources import Bandwidth
from uuid import UUID, uuid1


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
        A Vm uses up the allocated time slice and is hanging by Vm Scheduler on the Host
        """
        HANGING = 4

        """
        A Vm is ``poweroff'' on an assigned Host so that no Cloudlets will be bound to the Vm
        """
        POWEROFF = 5

        """
        A Vm destroyed successfully by the datacenter Broker
        """
        DESTROYED = 6

        """
        A Vm exited abnormally by simulation early stopping, crash or fault injection
        """
        FAILED = 7

        """
        A Vm instance will be canceled if there is no suitable Host to bind
        """
        CANCELED = 8

    def __init__(self, id: int = -1, mips: int = int(1e3), num_pes: int = 1, size_ram: int = 1024, size_storage: int = 10*1024, size_bandwidth: int = 100) -> None:
        """
        Parameters
        ----------
        id: int
            It is recommended to assign an id to the Vm for better summary
        mips: int
            Vm Pe rate in MIPS, it is recommend to be no greater than Host MIPS
            or the created Vm will be canceled by datacenter Broker
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
        self.mips = 1.0*mips
        self.num_pes = num_pes
        self.size_ram = 1.0*size_ram
        self.size_storage = 1.0*size_storage
        self.size_bandwidth = 1.0*size_bandwidth
        self.ram = None
        self.storage = None
        self.bandwidth = None
        self.state = Vm.State.CREATED
        self.startup_delay = 0.0
        self.shudown_delay = 0.0

        self.cloudlet_dict = None
        self.host = None

    def get_uuid(self) -> UUID:
        return self.uuid

    def get_id(self) -> int:
        return id

    def get_num_pes(self) -> int:
        return self.num_pes

    def get_size_ram(self) -> float:
        return self.size_ram

    def get_size_storage(self) -> float:
        return self.size_storage

    def get_size_bandwidth(self) -> float:
        return self.size_bandwidth

    def get_start_up_delay(self) -> float:
        return self.startup_delay

    def get_shutdown_delay(self) -> float:
        return self.shudown_delay

    def bind_host(self, host) -> None:
        self.host = host
        self.state = Vm.State.BOUNDED

    def cancel(self) -> None:
        self.state = Vm.State.CANCELED

    def set_state(self, state: State):
        self.state = state
