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
        Host Event
        ----------
        """
        """
        Host Creation
        """
        HOST_CREATION = 100

        """
        Vm Event
        --------
        """
        """
        Destory a Vm after runtime error, early stop, fault injection, etc.
        """
        VM_FAIL = 200

        """
        Destory a Vm after removing the Vm from Host normally
        """
        VM_DESTORY = 201

        """
        Select a Host to bind a created Vm
        """
        VM_BIND = 202

        """
        Poweroff a Vm and move it to disk
        """
        VM_POWEROFF = 203

        """
        Poweron a Vm after creation or reloading from the disk
        """
        VM_POWERON = 204

        """
        Cloudlet Event
        --------------
        """
        """
        Terminate a Cloudlet after runtime error, early stop, fault injection, etc.
        """
        CLOUDLET_FAIL = 300

        """
        Finish a Cloudlet after successful execution
        """
        CLOUDLET_FINISH = 301

        """
        Select a Vm to bind a created Cloudlet
        """
        CLOUDLET_BIND = 302

        """
        Detach a Cloudlet to hang
        """
        CLOUDLET_DETACH = 303

        """
        Attach a Cloudlet to run on a Vm
        """
        CLOUDLET_ATTACH = 304

    """
    Event defines the general ``communication'' behaviors between datacenter entities,
    helps the simulation in a loose coupling form
    """

    def __init__(self, source: object = None, target: object = None, event_type: TYPE = None, extra_data: Dict = None, start_delay: float = 0.0) -> None:
        if event_type is None:
            raise ValueError("Event type can not be None")
        self.start_delay = 1.0*start_delay
        self.source = source
        self.target = target
        self.event_type = event_type
        self.extra_data = extra_data

    def get_start_delay(self):
        return self.start_delay

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
