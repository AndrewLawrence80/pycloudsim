from __future__ import annotations
from .vm_suitability import VmSuitability
from .cloudlet_placement import CloudletPlacement
from ..utils import MinHeap
from typing import TYPE_CHECKING, List, Tuple
if TYPE_CHECKING:
    from ..vms import VmRunning
    from ..cloudlets import CloudletRunning


class CloudletPlacementMaxFit(CloudletPlacement):
    def __init__(self) -> None:
        super().__init__()

    def try_to_place(self, vm_running_list: List[VmRunning], cloudlet_to_run_list: List[CloudletRunning]) -> Tuple[bool, List[CloudletRunning]]:
        def vm_suitability_comparator(suitability_a: VmSuitability, suitability_b: VmSuitability):
            if suitability_a.get_suitability() and not suitability_b.get_suitability():
                return True
            elif not suitability_a.get_suitability() and suitability_b.get_suitability():
                return False
            elif not suitability_a.get_suitability() and not suitability_b.get_suitability():
                return False
            else:
                if suitability_a.get_vm_running().get_num_pes_available() > suitability_b.get_vm_running().get_num_pes_available():
                    return True
                elif suitability_a.get_vm_running().get_num_pes_available() < suitability_b.get_vm_running().get_num_pes_available():
                    return False
                else:
                    return suitability_a.get_vm_running().get_id() < suitability_b.get_vm_running().get_id()
        if len(vm_running_list) == 0:
            return False, []

        cloudlet_running_placed_list = []
        is_place_successful = True
        vm_suitability_heap = MinHeap(vm_suitability_comparator)
        for vm_running in vm_running_list:
            vm_suitability_heap.push(VmSuitability(vm_running))
        for cloudlet_to_run in cloudlet_to_run_list:
            for vm_suitability in vm_suitability_heap:
                vm_suitability.update_suitability(cloudlet_to_run)
            vm_suitability_heap.reheapify()
            suitability_head = vm_suitability_heap.pop()
            if suitability_head.get_suitability() == False:
                is_place_successful = False
                break
            else:
                suitability_head.get_vm_running().bind_cloudlet(cloudlet_to_run)
                cloudlet_running_placed_list.append(cloudlet_to_run)
                vm_suitability_heap.push(suitability_head)
        if not is_place_successful:
            for cloudlet_running in cloudlet_running_placed_list:
                vm_running = cloudlet_running.get_vm_running()
                vm_running.release_cloudlet(cloudlet_running)

        return is_place_successful, cloudlet_running_placed_list
