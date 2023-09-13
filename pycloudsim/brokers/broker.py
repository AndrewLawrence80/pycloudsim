from __future__ import annotations
from ..datacenters import Datacenter
from ..simulation import Simulator
from ..vms import Vm
from ..cloudlets import Cloudlet
from ..events import Event
from typing import List, TYPE_CHECKING


class Broker:
    def __init__(self, simulator: Simulator, datacenter: Datacenter) -> None:
        """
        A Broker represents a intermediate proxy communicating customers and a datacener.
        It hides management details such as Vm and Cloudlet behavior
        such as creation, allocation, schedule, etc.
        """
        if datacenter is None:
            raise ValueError("Datacenter can not be None")
        self.datacenter = datacenter
        self.simulator = simulator

    def submit_vm_list(self, vm_list: List[Vm]):
        """
        After submission, datacenter will try to bind all submitted Vms to suitable Hosts
        using max-fit strategy. There are 2 possible bind result: all bind or none bind
        """
        for vm in vm_list:
            vm.set_state(Vm.State.SUBMITTED)
        self.simulator.submit(Event(source=None, target=self.datacenter, event_type=Event.TYPE.VM_BIND, extra_data={"vm_list": vm_list, "simulator": self.simulator}, start_time=self.simulator.get_global_clock()))

    def submit_cloudlet_list(self, cloudlet_list: List[Cloudlet]):
        """
        After submission, datacenter will put all the submitted Cloudlets into a waiting queue,
        all the cloudlets will be served in FIFO way
        """
        for cloudlet in cloudlet_list:
            cloudlet.set_state(Cloudlet.State.SUBMITTED)
        self.simulator.submit(Event(source=None, target=self.datacenter, event_type=Event.TYPE.CLOUDLET_SUBMIT, extra_data={"cloudlet_list": cloudlet_list, "simulator": self.simulator}, start_time=self.simulator.get_global_clock()))
