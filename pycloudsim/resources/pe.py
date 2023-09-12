"""
A Pe (Processing Element) represents a CPU core of a physical machine,
defined in terms of Millions Instructions Per Second (MIPS) rating.
"""
from uuid import uuid1, UUID
from enum import Enum


class Pe:
    class State(Enum):
        FREE = 0
        BUSY = 1

    def __init__(self, mips_capacity: int) -> None:
        """
        Parameters
        ----------
        mips_capacity : int
            Pe rate in MIPS
        """
        if mips_capacity <= 0:
            raise ValueError("MIPS capacity of Pe must greater than 0")
        self.uuid = uuid1()
        self.mips_capacity = 1.0*mips_capacity
        self.utilization_rate = 0.0
        self.state = Pe.State.FREE

    def get_uuid(self) -> UUID:
        return self.uuid

    def allocate(self, utilization_rate: float) -> None:
        if utilization_rate <= 0 or utilization_rate > 1:
            raise ValueError(
                "Cloudlet Pe utilization rate must beween 0 and 1")
        self.utilization_rate += utilization_rate

    def deallocate(self, utilization_rate: float) -> None:
        if utilization_rate <= 0 or utilization_rate > 1:
            raise ValueError(
                "Cloudlet Pe utilization rate must beween 0 and 1")
        self.utilization_rate -= utilization_rate

    def get_mips_capacity(self) -> float:
        return self.mips_capacity

    def get_utilization_rate_allocated(self) -> float:
        return self.utilization_rate

    def get_utilization_rate_available(self) -> float:
        return 1-self.utilization_rate

    def get_state(self) -> State:
        return self.state

    def set_state(self, state: State) -> None:
        self.state = state
