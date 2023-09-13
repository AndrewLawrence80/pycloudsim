"""
Storage for Host (physical machine) or Vm
"""
from uuid import uuid1, UUID


class Storage:

    def __init__(self, size_capacity: int) -> None:
        """
        Parameters
        ----------
        size_capacity: int
            Storage capacity in MB
        """
        if size_capacity <= 0:
            raise ValueError("Capacity of storage must greater than 0 MB")
        self.uuid = uuid1()
        self.size_capacity = 1.0*size_capacity
        self.size_available = self.size_capacity

    def get_uuid(self) -> UUID:
        return self.uuid

    def allocate(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("Storage to allocate must no less than 0 MB")
        elif self.size_available < amount:
            raise RuntimeError("Allocate amount exceeds available storage size")
        self.size_available -= amount

    def dealloate(self, amount: float) -> None:
        if (amount < 0):
            raise ValueError("Storage to deallocate must no less than 0 MB")
        self.size_available += amount

    def get_size_capacity(self) -> float:
        return self.size_capacity

    def get_size_available(self) -> float:
        return self.size_available

    def get_utilization_rate(self) -> float:
        return (self.size_capacity-self.size_available)/self.size_capacity
