from ..hosts import Host
from ..simulation import Simulator, SimulationEntity
from ..events import Event
from ..logger import Logger
from ..placement import VmPlacementMaxFit
from enum import Enum
from typing import List
import copy


class Datacenter(SimulationEntity):
    def __init__(self, simulator: Simulator, host_list: List[Host], scheduling_interval: float = 1) -> None:
        self.host_dict = {}
        self.vm_dict = {}
        self.scheduling_interval = 1.0*scheduling_interval
        self.simulator = simulator
        self.simulator.submit(Event(
            source=None, target=self, event_type=Event.TYPE.HOST_CREATION, extra_data={"host_list": host_list}, start_delay=0))
        self.vm_placement_policy = VmPlacementMaxFit()
        self.cloudlet_placement_policy = None

    def process(self, event: Event):
        if event.get_event_type() == Event.TYPE.HOST_CREATION:
            self.process_host_creation(event)
        elif event.get_event_type() == Event.TYPE.VM_BIND:
            self.process_vm_bind(event)

    def process_host_creation(self, event: Event):
        logger = Logger()
        logger.info("%6.2f\tDatacenter\tTrying to create hosts in datacenter" %
                    self.simulator.get_global_clock())
        extra_data = event.get_extra_data()
        host_list = extra_data["host_list"]
        for host in host_list:
            self.host_dict[host.get_uuid()] = host
        logger.info("%6.2f\tDatacenter\tSucceed to create hosts in datacenter" %
                    self.simulator.get_global_clock())

    def process_vm_bind(self, event: Event):
        logger = Logger()
        logger.info("%6.2f\tDatacenter\tTrying to bind vm to host" %
                    self.simulator.get_global_clock())
        extra_data = event.get_extra_data()
        vm_list = extra_data["vm_list"]
        vm_dict = {}
        for vm in vm_list:
            vm_dict[vm.get_uuid()] = vm

        is_bind_successful = False
        host_list_copy = [copy.deepcopy(host)
                          for host in self.host_dict.values()]
        vm_list_copy = [copy.deepcopy(vm) for vm in vm_list]
        fit_map = self.vm_placement_policy.get_fit_map(
            host_list_copy, vm_list_copy)
        if fit_map is None:
            is_bind_successful = False
            logger.warning(
                "%6.2f\tDatacenter\tFailed to bind vms to host since there is no suitable host to accommodate all the vms")
        else:
            is_bind_successful = True
            for vm_uuid, host_uuid in fit_map.items():
                self.host_dict[host_uuid].bind_vm(vm_dict[vm_uuid])
                self.vm_dict[vm_uuid] = vm_dict[vm_uuid]
                self.vm_dict[vm_uuid].bind_host(self.host_dict[host_uuid])

        if is_bind_successful:
            logger.info("%6.2f\tDatacenter\tSucceed to bind vm to host" %
                        self.simulator.get_global_clock())
            
        else:
            logger.info("%6.2f\tDatacenter\tCancel vm binding due to lack of resources" % (
                self.simulator.get_global_clock()))

    def get_host_list(self):
        return self.host_list
