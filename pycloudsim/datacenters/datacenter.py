from __future__ import annotations
from ..entity import SimulationEntity
from ..events import Event
from ..logger import Logger
from ..placement import VmPlacementMaxFit
from ..placement import CloudletPlacementMaxFit
from ..vms import Vm
from ..cloudlets import Cloudlet
from collections import deque
from uuid import uuid1, UUID
from typing import List, TYPE_CHECKING, Dict
import copy
if TYPE_CHECKING:
    from ..hosts import Host


class Datacenter(SimulationEntity):
    def __init__(self, host_list: List[Host]) -> None:
        self.uuid = uuid1()
        self.host_dict = self._build_host_dict(host_list)
        self.vm_placement_policy = VmPlacementMaxFit()
        self.vm_booting_dict = {}
        self.vm_running_dict = {}
        self.vm_end_of_life_dict = {}
        self.cloudlet_placement_policy = CloudletPlacementMaxFit()
        self.cloudlet_waiting_deque = deque([])
        self.cloudlet_running_dict = {}
        self.cloudlet_end_of_life_dict = {}

    def _build_host_dict(self, host_list: List[Host]) -> Dict[UUID, Host]:
        host_dict = {}
        for host in host_list:
            host.set_datacenter(self)
            host_dict[host.get_uuid()] = host
        return host_dict

    def process(self, event: Event):
        if event.get_event_type() == Event.TYPE.SIMULATION_TERMINATE:
            self.process_simulation_terminate(event)
        elif event.get_event_type() == Event.TYPE.HOST_ADD:
            pass
        elif event.get_event_type() == Event.TYPE.HOST_REMOVE:
            pass
        elif event.get_event_type() == Event.TYPE.HOST_POWERON:
            pass
        elif event.get_event_type() == Event.TYPE.HOST_POWEROFF:
            pass
        elif event.get_event_type() == Event.TYPE.VM_FAIL:
            pass
        elif event.get_event_type() == Event.TYPE.VM_DESTORY:
            self.process_vm_destroy(event)
        elif event.get_event_type() == Event.TYPE.VM_BIND:
            self.process_vm_bind(event)
        elif event.get_event_type() == Event.TYPE.VM_SHUTDOWN:
            self.process_vm_shutdown(event)
        elif event.get_event_type() == Event.TYPE.VM_BOOTUP:
            self.process_vm_bootup(event)
        elif event.get_event_type() == Event.TYPE.CLOUDLET_FAIL:
            pass
        elif event.get_event_type() == Event.TYPE.CLOUDLET_FINISH:
            self.process_cloudlet_finish(event)
        elif event.get_event_type() == Event.TYPE.CLOUDLET_BIND:
            self.processs_cloudlet_bind(event)
        elif event.get_event_type() == Event.TYPE.CLOUDLET_SUBMIT:
            self.process_cloudlet_submit(event)

    def process_vm_bind(self, event: Event):
        extra_data = event.get_extra_data()
        simulator = extra_data["simulator"]
        vm_list = extra_data["vm_list"]
        logger = Logger()
        logger.info("%6.2f\tDatacenter\tTrying to bind vm to host" %
                    simulator.get_global_clock())
        vm_dict = {}
        for vm in vm_list:
            vm_dict[vm.get_uuid()] = vm

        host_list_copy = [copy.deepcopy(host)
                          for host in self.host_dict.values()]
        vm_list_copy = [copy.deepcopy(vm) for vm in vm_list]
        fit_map = self.vm_placement_policy.get_fit_map(
            host_list_copy, vm_list_copy)
        if fit_map is None:
            logger.warning(
                "%6.2f\tDatacenter\tFailed to bind vms to host since there is no suitable host to accommodate all the vms")
        else:
            for vm_uuid, host_uuid in fit_map.items():
                vm = vm_dict[vm_uuid]
                host = self.host_dict[host_uuid]
                host.bind_vm(vm)
                self.vm_booting_dict[vm_uuid] = vm
                simulator.submit(Event(source=None, target=self, event_type=Event.TYPE.VM_BOOTUP, extra_data={
                                 "vm": vm, "simulator": simulator}, start_time=simulator.get_global_clock()+vm.get_startup_delay()))
                vm.set_state(Vm.State.BOUNDED)
                logger.info("%6.2f\tDatacenter\tBind Vm %d to Host %d" % (
                    simulator.get_global_clock(), vm.get_id(), host.get_id()))
            logger.info("%6.2f\tDatacenter\tSucceed to bind vm to host" %
                        simulator.get_global_clock())

    def process_vm_bootup(self, event: Event) -> None:
        extra_data = event.get_extra_data()
        vm = extra_data["vm"]
        simulator = extra_data["simulator"]
        vm.set_state(Vm.State.RUNNING)
        self.vm_booting_dict.pop(vm.get_uuid())
        self.vm_running_dict[vm.get_uuid()] = vm
        logger = Logger()
        logger.info("%6.2f\tDatacenter\tVm %d booted up" %
                    (simulator.get_global_clock(), vm.get_id()))
        simulator.submit(Event(source=None, target=self, event_type=Event.TYPE.CLOUDLET_BIND, extra_data={
                         "simulator": simulator}, start_time=simulator.get_global_clock()))

    def process_cloudlet_submit(self, event: Event) -> None:
        extra_data = event.get_extra_data()
        cloudlet_list = extra_data["cloudlet_list"]
        simulator = extra_data["simulator"]
        logger = Logger()
        for cloudlet in cloudlet_list:
            self.cloudlet_waiting_deque.append(cloudlet)
            logger.info("%6.2f\tDatacenter\tCloudlet %d submitted" %
                        (simulator.get_global_clock(), cloudlet.get_id()))
        simulator.submit(Event(source=None, target=self, event_type=Event.TYPE.CLOUDLET_BIND, extra_data={
                         "simulator": simulator}, start_time=simulator.get_global_clock()))

    def processs_cloudlet_bind(self, event: Event) -> None:
        extra_data = event.get_extra_data()
        simulator = extra_data["simulator"]
        logger = Logger()
        while not len(self.cloudlet_waiting_deque) == 0:
            cloudlet = self.cloudlet_waiting_deque.popleft()
            running_vm_list_copy = []
            for vm in self.vm_running_dict.values():
                if vm.get_state() == Vm.State.RUNNING and not vm.get_is_scheduled_to_shutdown():
                    running_vm_list_copy.append(copy.deepcopy(vm))
            cloudlet_list_copy = [copy.deepcopy(cloudlet)]
            fit_map = self.cloudlet_placement_policy.git_fit_map(
                running_vm_list_copy, cloudlet_list_copy)
            if fit_map is None:
                self.cloudlet_waiting_deque.appendleft(cloudlet)
                break
            else:
                running_vm_uuid = list(fit_map.values())[0]
                running_vm = self.vm_running_dict[running_vm_uuid]
                running_vm.bind_cloudlet(cloudlet)
                logger.info("%6.2f\tDatacenter\tBind Cloudlet %d to Vm %d" % (
                    simulator.get_global_clock(), cloudlet.get_id(), running_vm.get_id()))
                cloudlet.set_state(Cloudlet.State.RUNNING)
                self.cloudlet_running_dict[cloudlet.get_uuid()] = cloudlet
                cloudlet_pe_uuid = running_vm.get_cloudlet_pe_dict()[
                    cloudlet.get_uuid()][0]
                mips = running_vm.get_vm_pe_dict()[cloudlet_pe_uuid].get_mips_capacity(
                )*running_vm.get_host_mips_factor()
                exec_time = round(cloudlet.get_length()/mips, 2)
                simulator.submit(Event(source=None, target=self, event_type=Event.TYPE.CLOUDLET_FINISH, extra_data={
                                 "cloudlet": cloudlet, "simulator": simulator}, start_time=simulator.get_global_clock()+exec_time))

    def process_cloudlet_finish(self, event: Event) -> None:
        extra_data = event.get_extra_data()
        cloudlet = extra_data["cloudlet"]
        simulator = extra_data["simulator"]
        self.cloudlet_running_dict.pop(cloudlet.get_uuid())
        vm = self.vm_running_dict[cloudlet.get_vm().get_uuid()]
        vm.release_cloudlet(cloudlet)
        cloudlet.set_state(Cloudlet.State.SUCCEEDED)
        self.cloudlet_end_of_life_dict[cloudlet.get_uuid()] = cloudlet
        logger = Logger()
        logger.info("%6.2f\tDatacenter\tCloudlet %d exection done at Vm %d" % (
            simulator.get_global_clock(), cloudlet.get_id(), vm.get_id()))
        simulator.submit(Event(source=None, target=self, event_type=Event.TYPE.CLOUDLET_BIND, extra_data={
                         "simulator": simulator}, start_time=simulator.get_global_clock()))
        if cloudlet.get_vm().get_is_scheduled_to_shutdown() and len(vm.get_cloudlet_dict()) == 0:
            simulator.submit(Event(source=None, target=self, event_type=Event.TYPE.VM_SHUTDOWN, extra_data={
                             "vm": vm, "simulator": simulator}, start_time=simulator.get_global_clock()))

    def process_vm_shutdown(self, event: Event) -> None:
        extra_data = event.get_extra_data()
        vm = extra_data["vm"]
        simulator = extra_data["simulator"]
        logger = Logger()
        logger.info("%6.2f\tDatacenter\tVm %d begins shutting down" %
                    (simulator.get_global_clock(), vm.get_id()))
        vm.set_state(Vm.State.SHUTTINGDOWN)
        cloudlet_dict = vm.get_cloudlet_dict()
        for cloudlet in cloudlet_dict.values():
            vm.release_cloudlet(cloudlet)
            cloudlet.set_state(Cloudlet.State.FAILED)
            self.cloudlet_running_dict.pop(cloudlet.get_uuid())
            self.cloudlet_end_of_life_dict[cloudlet.get_uuid()] = cloudlet
        simulator.submit(Event(source=None, target=self, event_type=Event.TYPE.VM_DESTORY, extra_data={
                         "vm": vm, "simulator": simulator}, start_time=simulator.get_global_clock()+vm.get_shutdown_delay()))

    def process_simulation_terminate(self, event: Event) -> None:
        extra_data = event.get_extra_data()
        simulator = extra_data["simulator"]
        for vm in self.vm_running_dict.values():
            simulator.submit(Event(source=None, target=self, event_type=Event.TYPE.VM_SHUTDOWN, extra_data={
                             "vm": vm, "simulator": simulator}, start_time=simulator.get_global_clock()))
        for cloudlet in self.cloudlet_waiting_deque:
            cloudlet.set_state(Cloudlet.State.CANCELED)
            self.cloudlet_end_of_life_dict[cloudlet.get_uuid()] = cloudlet

    def process_vm_destroy(self, event: Event) -> None:
        extra_data = event.get_extra_data()
        vm = extra_data["vm"]
        simulator = extra_data["simulator"]
        vm.set_state(Vm.State.DESTROYED)
        self.vm_running_dict.pop(vm.get_uuid())
        self.vm_end_of_life_dict[vm.get_uuid()] = vm
        logger = Logger()
        logger.info("%6.2f\tDatacenter\tVm %d destroyed" %
                    (simulator.get_global_clock(), vm.get_id()))
