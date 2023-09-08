from enum import Enum
from ..vms import Vm
from uuid import UUID,uuid1

class Cloudlet:
    """
    A Cloudlet is the basic unit of an application/job/task to be executed by a Vm
    """

    class State(Enum):
        """
        The Cloudlet is created but has not been submitted to the datacenter broker
        """
        CREATED = 0

        """
        The Cloudlet is submitted to the datacenter broker but has not been assigned to any Vm yet
        """
        SUBMITTED = 1

        """
        The Cloudlet is assigned to a Vm but has not been scheduled to run yet
        """
        WAITING = 2

        """
        The Cloudlet is running on a Vm
        """
        RUNNING = 3

        """
        The Cloudlet has run out of previous assigned Pe time slice, but not finished yet.
        Vm scheduler will hang up the Cloudlet util the next time when it is eligible to run again
        """
        HANGING = 4

        """
        The Cloudlet successfully finished running on an assigned Vm
        """
        SUCCEEDED = 5

        """
        The Cloudlet failed due to run time error such as Vm crash or fault injection
        """
        FAILED = 6

        """
        The Cloudlet canceled after being submitted to the datacenter broker due to early stop of Vm or simulation
        """
        CANCELED = 7

    def __init__(self, id: int = -1, length: int = 1, num_pes: int = 1) -> None:
        """
        Parameters
        ----------
        id: int
            If id is ignored, a suitable Vm will still be assigned to execute the Cloudlet after submission, 
            but it is suggested to provide a unique Cloudlet id for better execution summary,
            unless you want Vm to execute instructions like ```NOP```
        length: int
            The length of the Cloudlet, measured in million instructions (MI)
        num_pes: int
            The number of the required of CPU cores of the Cloudlet,
            which is arbitrary defined by the user.
            Actual number of allocated CPU cores will be decided by the assigned Vm, 
            for example, if a Cloudlet of length 1000 MI, requiring 2 Pes is assigned
            to a Vm with 1 Pe with 1000 MIPS, the total execution time of the Cloudlet
            is 1000 (MI) x 2 (Pes) / (1000 (MIPS) x 1 (Pe)) = 2s
        """
        self.uuid=uuid1()
        self.id = id
        if length <= 0:
            raise ValueError("Cloudlet must greater than 0")
        self.length = 1.0*length
        if num_pes <= 0:
            raise ValueError("Cloudlet Pes must greater than 0")
        self.num_pes = num_pes
        # By default use 100% of CPU core
        self.utilization_pe = 1.0
        # By default use 0 KB RAM
        self.utilization_ram = 0.0
        # By default use 0 Mbps bandwidth
        self.utilization_bandwidth = 0.0
        # By default use 0 MB file as IO
        self.utilization_storage = 0.0
        # By default the state is initailized as ```CREATED```
        self.state = Cloudlet.State.CREATED

        self.start_time = 0.0
        self.executed_time = 0.0
        self.end_time = 0.0

        self.executed_length = 0.0
        self.remaining_length = self.length

        self.vm = None

    def set_utilization_pe(self, utilization_rate: float):
        if not (utilization_rate > 0 and utilization_rate <= 1):
            raise ValueError(
                "Utilization rate of Pe must greater than 0 and no more than 1")
        self.utilization_pe = 1.0*utilization_rate

    def set_utilization_ram(self, utilization_rate: float):
        if not (utilization_rate >= 0 and utilization_rate <= 1):
            raise ValueError(
                "Utilization of RAM must no less than 0 and no more than 1")
        self.utilization_ram = 1.0*utilization_rate

    def set_utilization_bandwidth(self, utilization_rate: float):
        if not (utilization_rate >= 0 and utilization_rate <= 1):
            raise ValueError(
                "Utilization of bandwidth must no less than 0 and no more than 1")
        self.utilization_ram = 1.0*utilization_rate

    def set_utilization_storage(self, utilization_size: float):
        """
        Parameters
        ----------
        utilization_size: float
            The storage size will be used by the Cloudlet in MB
        """
        if not(utilization_size >= 0):
            raise ValueError("Utilization of storage must no less than 0")
        self.utilization_storage = 1.0*utilization_size

    def bind_to_vm(self, vm: Vm):
        self.vm = vm

    def set_state(self, state: State):
        self.state = state

    def get_uuid(self)->UUID:
        return self.uuid