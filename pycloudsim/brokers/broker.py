from ..datacenters import Datacenter
from ..simulation import Simulator
from ..simulation import SimulationEntity
from ..vms import Vm
from ..events import Event
from typing import List


class Broker(SimulationEntity):
    """
    A Broker represents a intermediate proxy communicating customers and a datacener.
    It hides management details such as Vm and Cloudlet behavior
    such as creation, allocation, schedule, etc.
    """

    def __init__(self, simulator: Simulator, datacenter: Datacenter) -> None:
        if datacenter is None:
            raise ValueError("Datacenter can not be None")
        self.datacenter = datacenter
        self.simulator = simulator

    def submit_vm_list(self, vm_list: List[Vm]):
        for vm in vm_list:
            vm.set_state(Vm.State.SUBMITTED)
        self.simulator.submit(Event(source=None, target=self.datacenter,
                              event_type=Event.TYPE.VM_BIND, extra_data={"vm_list": vm_list}, start_delay=0))

    def submit_cloudlet_list(self, cloudlet_list: List[Vm]):
        pass
