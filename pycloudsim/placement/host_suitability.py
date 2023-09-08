from ..hosts import Host
from ..vms import Vm
from .suitability import Suitability


class HostSuitability(Suitability):
    def __init__(self, host: Host) -> None:
        self.host = host
        self.is_suitable = False

    def is_suitable_for(self, target: Vm) -> bool:
        self.is_suitable = False
        if (
            target.get_num_pes() <= self.host.get_num_pes() and
            target.get_size_ram() <= self.host.get_ram().get_size_available() and
            target.get_size_storage() <= self.host.get_storage().get_size_available() and
            target.get_size_bandwidth() <= self.host.get_bandwidth().get_size_available()
        ):
            self.is_suitable = True

    def get_is_suitable(self) -> bool:
        return self.is_suitable

    def get_host(self) -> Host:
        return self.host
