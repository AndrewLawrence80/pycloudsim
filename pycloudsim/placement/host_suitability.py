from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..hosts import Host
    from ..vms import VmRunning


class HostSuitability:
    def __init__(self, host: Host) -> None:
        self.host = host
        self.suitability = False

    def update_suitability(self, target: VmRunning) -> bool:
        self.suitability = False
        if (
            target.get_num_pes() <= self.host.get_num_pes_available() and
            target.get_size_ram() <= self.host.get_ram().get_size_available() and
            target.get_size_storage() <= self.host.get_storage().get_size_available() and
            target.get_size_bandwidth() <= self.host.get_bandwidth().get_size_available()
        ):
            self.suitability = True

    def get_suitability(self) -> bool:
        return self.suitability

    def get_host(self) -> Host:
        return self.host
