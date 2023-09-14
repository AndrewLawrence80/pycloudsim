from pycloudsim.hosts import Host
from pycloudsim.vms import Vm
from pycloudsim.cloudlets import Cloudlet
from pycloudsim.resources import Pe
from pycloudsim.simulation import Simulator
from pycloudsim.datacenters import Datacenter
from pycloudsim.brokers import Broker
from pycloudsim.listeners import CircularClockListener
from pycloudsim.events import Event
import numpy as np

config = {
    "host": {
        "num": 2,  # Number of physical machines in the datacenter
        "pes": 4,  # Number of CPU cores per host
        "mips": int(1e3),  # CPU rate in MIPS, 1 GHz
        "ram": np.iinfo(np.int32).max,  # Infinite RAM (MB)
        "bandwidth": np.iinfo(np.int32).max,  # Infinite bandwidth (Mbps)
        "storage": np.iinfo(np.int32).max  # Infinite storage (MB)
    },
    "vm": {
        "num": 4,  # Vm number
        "pes": 2,  # CPU core(s) per Vm
        "host_mips_factor": 1,  # Same as host, assuming no performance loss
        "ram": 1024,  # 1 GB
        "bandwidth": 100,  # 100 Mbps
        "storage": int(10*1e3),  # 10 GB
        "startup_delay": 30,  # Take 30s to start up
        "shutdown_delay": 10  # Take 10s to shutdown
    },
    "cloudlet": {
        "num": 5,  # Create 2 Cloudlets initially
        "pes": 1,  # Required 1 CPU core(s)
        "length": int(1*1e3),  # 1s for 1 CPU core to run
        "utilization_pe": 1,  # 0 < x <= 1, here each cloudlet will use up 100% of CPU core of Vm
        "required_ram": 1,  # Required RAM size in MB
        "required_bandwidth": 1,  # Required bandwdith in Mbps
        "required_storage": 1  # Required storage in MB
    }
}

if __name__ == "__main__":
    simulator = Simulator()

    host_list = []
    for id in range(config["host"]["num"]):
        pe_list = []
        for _ in range(config["host"]["pes"]):
            pe_list.append(Pe(config["host"]["mips"]))
        host_list.append(Host(pe_list, id, config["host"]["ram"], config["host"]["storage"], config["host"]["bandwidth"]))
    datacenter = Datacenter(host_list)
    simulator.set_datacenter(datacenter)
    broker = Broker(simulator, datacenter)

    vm_list = []
    for id in range(config["vm"]["num"]):
        vm = Vm(id, config["vm"]["host_mips_factor"], config["vm"]["pes"], config["vm"]["ram"], config["vm"]["storage"], config["vm"]["bandwidth"])
        vm.set_startup_delay(config["vm"]["startup_delay"])
        vm.set_shutdown_delay(config["vm"]["shutdown_delay"])
        vm_list.append(vm)
    broker.submit_vm_list(vm_list)

    class DynamicIncomingCloudletListenter(CircularClockListener):
        def __init__(self, cicular_interval: float) -> None:
            super().__init__(cicular_interval)
            self.num_incoming_cloudlet_list = [8, 4, 16, 32, 1]
            self.broker = None
            self.num_cloudlet_created = 0

        def update(self, simulator: Simulator) -> None:
            global_clock = simulator.get_global_clock()
            idx = 0 if int(global_clock) == 0 else int(global_clock)//int(self.circular_interval)
            if idx < len(self.num_incoming_cloudlet_list):
                num_incoming_cloudlets = self.num_incoming_cloudlet_list[idx]
                cloudlet_list = []
                for _ in range(num_incoming_cloudlets):
                    cloudlet_list.append(Cloudlet(self.num_cloudlet_created, config["cloudlet"]["length"], config["cloudlet"]["pes"], config["cloudlet"]["utilization_pe"],
                                                  config["cloudlet"]["required_ram"], config["cloudlet"]["required_storage"], config["cloudlet"]["required_bandwidth"]))
                    self.num_cloudlet_created += 1
                self.broker.submit_cloudlet_list(cloudlet_list)
                simulator.submit(Event(source=None, target=simulator, event_type=Event.TYPE.CIRCULAR_CLOCK_EVENT, extra_data=None, start_time=global_clock+self.circular_interval))

        def set_broker(self, broker: Broker) -> None:
            self.broker = broker

    circular_listener_dynamic_incoming_cloudlet = DynamicIncomingCloudletListenter(60)
    circular_listener_dynamic_incoming_cloudlet.set_broker(broker)

    simulator.add_circular_clock_listener(circular_listener_dynamic_incoming_cloudlet)
    # cloudlet_list = []
    # for id in range(config["cloudlet"]["num"]):
    #     cloudlet_list.append(Cloudlet(id, config["cloudlet"]["length"], config["cloudlet"]["pes"], config["cloudlet"]["utilization_pe"],
    #                                   config["cloudlet"]["required_ram"], config["cloudlet"]["required_storage"], config["cloudlet"]["required_bandwidth"]))
    # broker.submit_cloudlet_list(cloudlet_list)
    
    simulator.run_util_pause_or_terminate()
