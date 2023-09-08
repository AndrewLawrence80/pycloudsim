"""
Bandwidth for Host (physical machine) or Vm
"""


class Bandwidth:

    def __init__(self, size_capacity: int) -> None:
        """
        Parameters
        ----------
        size_capacity: int
            Bandwidth in Mbps
        """
        self.size_capacity = 1.0*size_capacity
        self.size_available = self.size_capacity

    def allocate(self, amount: float) -> bool:
        if amount < 0:
            raise ValueError("Bandwidth to allocate must no less than 0 Mbps")
        allocate_succeeded = False
        if self.size_available > amount:
            self.size_available -= amount
            allocate_succeeded = True
        return allocate_succeeded

    def dealloate(self, amount: float) -> None:
        if self.size_available+amount > self.size_capacity:
            raise RuntimeError("Bandwidth exceeds capacity")
        self.size_available += amount

    def get_size_capacity(self) -> float:
        return self.size_capacity

    def get_size_available(self) -> float:
        return self.size_available

    def get_utilization_rate(self) -> float:
        return (self.size_capacity-self.size_available)/self.size_capacity
