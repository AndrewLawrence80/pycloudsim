from __future__ import annotations
from .vm_placement import VmPlacement
from ..utils import MinHeap
from .host_suitability import HostSuitability
from typing import List, TYPE_CHECKING,Tuple
if TYPE_CHECKING:
    from ..hosts import Host
    from ..vms import VmRunning


class VmPlacementMaxFit(VmPlacement):
    def __init__(self) -> None:
        super().__init__()
    def try_to_place(self, host_list: List[Host], vm_to_run_list: List[VmRunning]) -> Tuple[bool,List[VmRunning]]:
        def host_suitability_comparator(suitability_a: HostSuitability, suitability_b: HostSuitability) -> bool:
            # if host a is suitable for vm while b is not
            if suitability_a.get_suitability() and not suitability_b.get_suitability():
                return True
            # if host a is not suitable for vm while b is
            elif not suitability_a.get_suitability() and suitability_b.get_suitability():
                return False
            # if both of host a and host b are not suitable for vm, their order doesn't matter
            elif not suitability_a.get_suitability() and not suitability_b.get_suitability():
                return False
            # if both of host a and host b are suitable for vm, the one with more available CPU cores goes first
            else:
                if suitability_a.get_host().get_num_pes_available() > suitability_b.get_host().get_num_pes_available():
                    return True
                elif suitability_a.get_host().get_num_pes_available() < suitability_b.get_host().get_num_pes_available():
                    return False
                # if both of host a and host b are suitable for vm with the same num of CPU cores, the one
                # with smaller host id goes first
                else:
                    return suitability_a.get_host().get_id() < suitability_b.get_host().get_id()

        vm_running_placed_list=[]
        is_place_successful = True
        host_suitability_heap = MinHeap(host_suitability_comparator)
        for host in host_list:
            host_suitability_heap.push(HostSuitability(host))
        for vm_to_run in vm_to_run_list:
            for host_suitability in host_suitability_heap:
                host_suitability.update_suitability(vm_to_run)
            host_suitability_heap.reheapify()
            suitability_head = host_suitability_heap.pop()
            if suitability_head.get_suitability() == False:
                is_place_successful = False
                break
            else:
                suitability_head.get_host().bind_vm(vm_to_run)
                vm_running_placed_list.append(vm_to_run)
                host_suitability_heap.push(suitability_head)

        if not is_place_successful:
            for vm_running in vm_running_placed_list:
                host=vm_running.get_host()
                host.release_vm_running(vm_running)
        
        return is_place_successful,vm_running_placed_list
