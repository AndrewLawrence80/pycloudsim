from pycloudsim.datacenters import Datacenter
from pycloudsim.brokers import Broker
from pycloudsim.hosts import Host
from pycloudsim.vms import Vm
from pycloudsim.cloudlets import Cloudlet
from pycloudsim.resources import Pe, RAM, Storage, Bandwidth
from pycloudsim.simulation import Simulator
from typing import List
import numpy as np

config = {
    "datacenter": {
        "scheduling_interval": 1  # Indicates how often the datacenter handles incoming events
    },
    "host": {
        "num": 2,  # Number of physical machines in the datacenter
        "pes": 64,  # Number of CPU cores per host
        "mips": int(1e3),  # CPU rate in MIPS, 1 GHz
        "ram": np.iinfo(np.int32).max,  # Infinite RAM (MB)
        "bandwidth": np.iinfo(np.int32).max,  # Infinite bandwidth (Mbps)
        "storage": np.iinfo(np.int32).max  # Infinite storage (MB)
    },
    "vm": {
        "num": 2,  # Create 1 Vm initially
        "pes": 1,  # 1 CPU core per Vm
        "mips": int(1e3),  # Same as host, assuming no performance loss
        "ram": 1024,  # 1 GB
        "bandwidth": 100,  # 100 Mbps
        "storage": int(10*1e3),  # 10 GB
        "startup_delay": 30,  # Take 30s to start up
        "shutdown_delay": 10  # Take 10s to shutdown
    },
    "cloudlet": {
        "num": 1,  # Create 2 Cloudlets initially
        # ========= Important =========
        # Since the number of requested CPU cores per Cloudlet is 2,
        # while there is only 1 Pe available on the vm,
        # to run a cloudlet taking 1s per CPU (in maximum utilization model) will
        # result in 2s execution time.
        # ========= Important =========
        "pes": 2,  # Required CPU cores
        "length": int(1*1e3),  # 1s for 1 CPU core to run
        "utilization_pe": 1,  # 0 < x <= 1, here each cloudlet will use up 100% of CPU core of Vm
        "utilization_ram": 1e-3,  # 0 <= x <= 1, here each cloudlet will use 1 MB RAM of Vm
        # 0 <= x <= 1, here each cloudlet will use 1 Mbps bandwidth of Vm
        "utilization_bandwidth": 1e-2,
        "size_storage": 1e-3  # 1 KB storage
    }
}


def create_host_list(num_hosts: int, mips: int, num_pes: int, ram: int, storage: int, bandwidth: int) -> List[Host]:
    host_list = []
    for i in range(num_hosts):
        pe_list = []
        for j in range(num_pes):
            pe_list.append(Pe(mips))
        host_list.append(Host(pe_list, i, ram, storage, bandwidth))
    return host_list


def create_vm_list(num_vms: int, mips: int, num_pes: int, ram: int, storage: int, bandwidth: int) -> List[Vm]:
    vm_list = []
    for i in range(num_vms):
        vm_list.append(Vm(i, mips, num_pes, ram, storage, bandwidth))
    return vm_list


def create_cloudlet_list(num_cloudlets: int, num_pes: int, length: int, utilization_pe: float, utilization_ram: float, utilization_bandwidth: float, size_storage: float):
    cloudlet_list = []
    for i in range(num_cloudlets):
        cloudlet = Cloudlet(i, length, num_pes)
        cloudlet.set_utilization_pe(utilization_pe)
        cloudlet.set_utilization_ram(utilization_ram)
        cloudlet.set_utilization_bandwidth(utilization_bandwidth)
        cloudlet.set_utilization_storage(size_storage)
        cloudlet_list.append(cloudlet)
    return cloudlet_list


if __name__ == "__main__":
    simulator = Simulator()
    host_list = create_host_list(config["host"]["num"], config["host"]["mips"], config["host"]["pes"],
                                 config["host"]["ram"], config["host"]["storage"], config["host"]["bandwidth"])
    datacenter = Datacenter(simulator, host_list, scheduling_interval=1)
    broker = Broker(simulator, datacenter)
    vm_list = create_vm_list(config["vm"]["num"], config["vm"]["mips"], config["vm"]["pes"],
                             config["vm"]["ram"], config["vm"]["storage"], config["vm"]["bandwidth"])
    broker.submit_vm_list(vm_list)
    cloudlet_list = create_cloudlet_list(config["cloudlet"]["num"], config["cloudlet"]["pes"],
                                         config["cloudlet"]["length"], config["cloudlet"]["utilization_pe"],
                                         config["cloudlet"]["utilization_ram"], config["cloudlet"]["utilization_bandwidth"],
                                         config["cloudlet"]["size_storage"])

    simulator.run()
    pass
