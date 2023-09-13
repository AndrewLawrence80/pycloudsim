from __future__ import annotations
from enum import Enum
from uuid import uuid1
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..vms import Vm
    from uuid import UUID


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
        The Cloudlet successfully finished running on an assigned Vm
        """
        SUCCEEDED = 4

        """
        The Cloudlet failed due to run time error such as Vm crash or fault injection
        """
        FAILED = 5

        """
        The Cloudlet canceled after being submitted to the datacenter broker due to early stop of Vm or simulation
        """
        CANCELED = 6

    def __init__(self, id: int = -1, length: int = 1, num_pes: int = 1, utilization_pe: float = 1.0, required_ram: float = 0.0, required_storage: float = 0.0, required_bandwidth=0.0) -> None:
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
            if the number of the required CPU cannot be satisfied,
            the Cloudlet will be canceled
        """
        self.uuid = uuid1()
        self.id = id
        if length <= 0:
            raise ValueError("Cloudlet must greater than 0")
        self.length = 1.0*length
        if num_pes <= 0:
            raise ValueError("Cloudlet Pes must greater than 0")
        self.num_pes = num_pes
        if utilization_pe <= 0:
            raise ValueError("Cloudlet utilization of Pe must greater than 0")
        self.utilization_pe = 1.0*utilization_pe
        if required_ram < 0:
            raise ValueError("Cloudlet requested ram must no less than 0")
        self.required_ram = required_ram
        if required_storage < 0:
            raise ValueError("Cloudlet required storage must no less than 0")
        self.required_storage = required_storage
        if required_bandwidth < 0:
            raise ValueError("Cloudlet required bandwidth must no less than 0")
        self.required_bandwidth = required_bandwidth
        # By default the state is initailized as ```CREATED```
        self.state = Cloudlet.State.CREATED

        self.start_time = 0.0
        self.end_time = 0.0

        self.vm_uuid = None

    def get_uuid(self) -> UUID:
        return self.uuid

    def get_id(self) -> int:
        return self.id

    def get_length(self) -> float:
        return self.length

    def get_num_pes(self) -> int:
        return self.num_pes

    def get_utilization_pe(self) -> float:
        return self.utilization_pe

    def get_required_ram(self) -> float:
        return self.required_ram

    def get_required_storage(self) -> float:
        return self.required_storage

    def get_required_bandwidth(self) -> float:
        return self.required_bandwidth

    def get_state(self) -> State:
        return self.state

    def set_state(self, state: State):
        self.state = state

    def get_start_time(self) -> float:
        return self.start_time

    def set_start_time(self, start_time: float) -> None:
        self.start_time = start_time

    def get_end_time(self) -> float:
        return self.end_time

    def set_end_time(self, end_time: float) -> None:
        self.end_time = end_time

    def get_vm_uuid(self) -> UUID:
        return self.vm_uuid

    def set_vm_uuid(self, uuid: UUID):
        self.vm_uuid = uuid
