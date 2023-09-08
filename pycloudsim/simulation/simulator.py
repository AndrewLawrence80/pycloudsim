from ..events import Event
from ..utils import MinHeap
from .simulation_entity import SimulationEntity
import numpy as np


class Simulator(SimulationEntity):
    """
    A simulator is the core of cloud simulation, 
    which maintains an event priority queue and
    a global clock to perform event-driven simulation.
    A simulator is also an event dispatcher, 
    which accepts scheduled event from simulation entities 
    and act properly when event occurs
    """
    def event_comparator(event_a: Event, event_b: Event) -> bool:
        # The event with small start delay goes first
        if event_a.get_start_delay() < event_b.get_start_delay():
            return True
        elif event_a.get_start_delay() > event_b.get_start_delay():
            return False
        else:
            # If 2 or more events occur at the same time,
            # event with higher priority (smaller priority value, see details in Event class)
            # go first
            if event_a.get_event_priority() < event_b.get_event_priority():
                return True
            elif event_a.get_event_priority() > event_b.get_event_priority():
                return False
            else:
                # If 2 events with the same priority occur at the same time,
                # their order doesn't matter
                return False

    def __init__(self, time_terminate: float = None) -> None:
        self.event_queue = MinHeap(Simulator.event_comparator)
        self.global_clock = 0.0
        # set termination event
        if time_terminate is not None:
            if time_terminate <= 0:
                raise ValueError(
                    "Simulation terminate time must greater than 0")
        else:
            self.event_queue.push(Event(source=None, target=None, event_type=Event.TYPE.SIMULATION_TERMINATE,
                                  extra_data=None, start_delay=np.finfo(np.float64).max))

    def get_global_clock(self) -> float:
        return self.global_clock

    def submit(self, event: Event) -> None:
        self.event_queue.push(event)

    def send(self, event: Event) -> None:
        event.get_target().process(event)

    def run(self) -> None:
        while not self.event_queue.is_empty():
            event = self.event_queue.pop()
            self.global_clock += event.get_start_delay()
            self.process(event)

    def process(self, event: Event):
        if event.get_event_type() == Event.TYPE.SIMULATION_TERMINATE:
            self.process_simulation_terminate(event)
        elif event.get_event_type() == Event.TYPE.HOST_CREATION:
            self.send(event)
        elif event.get_event_type() == Event.TYPE.VM_FAIL:
            pass
        elif event.get_event_type() == Event.TYPE.VM_DESTORY:
            pass
        elif event.get_event_type() == Event.TYPE.VM_BIND:
            self.send(event)
        elif event.get_event_type() == Event.TYPE.VM_POWEROFF:
            pass
        elif event.get_event_type() == Event.TYPE.VM_POWERON:
            pass
        elif event.get_event_type() == Event.TYPE.CLOUDLET_FAIL:
            pass
        elif event.get_event_type() == Event.TYPE.CLOUDLET_FINISH:
            pass
        elif event.get_event_type() == Event.TYPE.CLOUDLET_BIND:
            pass
        elif event.get_event_type() == Event.TYPE.CLOUDLET_DETACH:
            pass
        elif event.get_event_type() == Event.TYPE.CLOUDLET_ATTACH:
            pass
        else:
            raise ValueError("Event type is not defined")

    def process_simulation_terminate(self, event: Event):
        pass
