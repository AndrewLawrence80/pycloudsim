"""
A Pe (Processing Element) represents a CPU core of a physical machine,
defined in terms of Millions Instructions Per Second (MIPS) rating.
"""


class Pe:
    def __init__(self, mips_capacity: int) -> None:
        """
        Parameters
        ----------
        mips_capacity : int
            Pe rate in MIPS
        """
        if mips_capacity <= 0:
            raise ValueError("MIPS capacity of Pe must greater than 0")
        self.mips_capacity = 1.0*mips_capacity
        self.utilization_rate = 0.0

    def __str__(self) -> str:
        return "Pe %s, mips capacity %d" % (id(self), self.mips_capacity)

    def allocate(self, utilization_rate: float):
        """
        Parameters
        ----------
        utilization_rate: float
            Amount of CPU core will be used for a certain Cloudlet
            when the Cloudlet is scheduled to be executed on the Pe
        """
        if self.utilization_rate <= 0:
            raise ValueError(
                "Cloudlet Pe utilization rate must greater than 0")
        self.utilization_rate += utilization_rate

    def deallocate(self, utilization_rate: float):
        """
        Parameters
        ----------
        utilization_rate: float
            Amount of CPU core will be released for a certain Cloudlet
            when the Cloudlet uses up the assigned time slice or finishes
        """
        if self.utilization_rate-utilization_rate < 0:
            raise ValueError(
                "Pe utilization will below 0 after Cloudlet releases")
        self.utilization_rate -= utilization_rate

    def get_mips_capacity(self) -> float:
        return self.mips_capacity

    def get_utilization_rate_allocated(self) -> float:
        return self.utilization_rate

    def get_utilization_rate_available(self) -> float:
        return 1-self.utilization_rate
