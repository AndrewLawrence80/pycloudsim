from enum import Enum
from typing import Dict


class Event:
    class TYPE(Enum):
        """
        This class defines various types of possible events 
        in a cloudsim scenario. The value of Enum defines the
        priority of each event, the smaller the value is, the higher
        the priority is. These will help when handling events occur
        in the same time in when simulator runs.
        All the event value is dedicatedly designed, 
        think carefully if you want to make changes
        """

        """
        Terminate the global simulation
        """
        SIMULATION_TERMINATE = 0

        """
        Pause the global simulation
        """
        SIMULATION_PAUSE = 1

        """
        Listener Event
        -----------------------------
        
        """
        """
        Circular Clock
        When the global clock reach the circular clock trigger condiction
        (global_clock % circular_interval == 0),
        the listener event must be handle first
        """
        CIRCULAR_CLOCK_EVENT = 100

        """
        Event Listener
        When specified event occurs during simulation, the event listener
        is triggered, the listener must be handle after a circular clock event
        if both of them occur at the same time.
        It is not necessary to define a dedicated event type of event listener
        since the simulator will broadcast event to every event listener when
        a event occurs
        """

        """
        Host Event
        ----------
        Since the hosts in the datacenter are initialized
        at the begining of datacenter creation,
        the host events are not implemented yet.
        """
        """
        Add host(s) when simulation is running
        """
        HOST_ADD = 200

        """
        Remove host(s) when simulation is running
        """
        HOST_REMOVE = 201

        """
        Poweron host(s) when simulation is running
        """
        HOST_POWERON = 202

        """
        Poweroff host(s) when simulation is running
        """
        HOST_POWEROFF = 203

        """
        Vm Event
        --------
        """
        """
        Destory a Vm after runtime error, early stop, fault injection, etc.
        """
        VM_FAIL = 300

        """
        Destory a Vm after removing the Vm from Host normally
        """
        VM_DESTORY = 301

        """
        Select a Host to bind a created Vm
        """
        VM_BIND = 302

        """
        Poweroff a Vm and move it to disk
        """
        VM_SHUTDOWN = 303

        """
        Poweron a Vm after creation or reloading from the disk
        """
        VM_BOOTUP = 304

        """
        Cloudlet Event
        --------------
        """
        """
        Terminate a Cloudlet after runtime error, early stop, fault injection, etc.
        """
        CLOUDLET_FAIL = 400

        """
        Finish a Cloudlet after successful execution
        """
        CLOUDLET_FINISH = 401

        """
        Select a Vm to bind a Cloudlet in the datacenter waiting queue
        """
        CLOUDLET_BIND = 402

        """
        Submit a Cloudlet or a Cloudlet list to the datacenter waiting queue
        """
        CLOUDLET_SUBMIT = 403

    """
    Event defines the general ``communication'' behaviors between datacenter entities,
    helps the simulation in a loose coupling form
    """

    def __init__(self, source: object = None, target: object = None, event_type: TYPE = None, extra_data: Dict = None, start_time: float = 0.0) -> None:
        if event_type is None:
            raise ValueError("Event type can not be None")
        self.source = source
        self.target = target
        self.event_type = event_type
        self.extra_data = extra_data
        self.start_time = start_time

    def get_start_time(self):
        return self.start_time

    def get_source(self):
        return self.source

    def get_target(self):
        return self.target

    def get_event_type(self):
        return self.event_type

    def get_event_priority(self):
        return self.event_type.value

    def get_extra_data(self):
        return self.extra_data
