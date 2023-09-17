from __future__ import annotations
from ..events import Event
from ..utils import MinHeap
from ..entity import SimulationEntity
from enum import Enum
import threading
import numpy as np
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..datacenters import Datacenter
    from ..listeners import EventListener, CircularClockListener


class Simulator(SimulationEntity):
    class State(Enum):
        """The simulation is initailized but not running yet"""
        INITIALIZED = 0
        """The simulation is running"""
        RUNNING = 1
        """The simulation is paused"""
        PAUSED = 1
        """The simulation end normaly or the terminate time arrives"""

    def event_comparator(event_a: Event, event_b: Event) -> bool:
        # The event with small start delay goes first
        if event_a.get_start_time() < event_b.get_start_time():
            return True
        elif event_a.get_start_time() > event_b.get_start_time():
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

    def __init__(self) -> None:
        """
        A simulator is the core of cloud simulation, 
        which maintains an event priority queue and
        a global clock to perform event-driven simulation.
        The events in event queue are ordered by start time.
        Event with smallest start time comes to the top of heap.
        A simulator is also an event dispatcher, 
        which accepts scheduled event from simulation entities 
        and act properly when event occurs
        """
        self.event_queue = MinHeap(Simulator.event_comparator)
        self.global_clock_prev = 0.0
        self.global_clock = 0.0
        self.event_listener_list = []
        self.circular_clock_listener_list = []
        self.state = Simulator.State.INITIALIZED
        self.datacenter = None
        self.is_terminate_time_set = False
        self.event_queue.push(Event(source=None, target=self, event_type=Event.TYPE.SIMULATION_TERMINATE, extra_data={"simulator": self}, start_time=np.finfo(np.float64).max))

    def get_global_clock(self) -> float:
        return self.global_clock

    def set_termination_time(self, terimination_time: float):
        self.is_terminate_time_set = True
        self.event_queue.push(Event(source=None, target=self, event_type=Event.TYPE.SIMULATION_TERMINATE, extra_data={"simulator": self}, start_time=terimination_time))

    def submit(self, event: Event) -> None:
        self.event_queue.push(event)

    def process(self, event: Event):
        for event_listener in self.event_listener_list:
            event_listener.update(event, self)
        if event.get_event_type() == Event.TYPE.SIMULATION_TERMINATE:
            self.process_simulation_terminate(event)
        elif event.get_event_type() == Event.TYPE.SIMULATION_PAUSE:
            self.process_simulation_pause(event)
        elif event.get_event_type() == Event.TYPE.CIRCULAR_CLOCK_EVENT:
            for circular_clock_listener in self.circular_clock_listener_list:
                circular_clock_listener.update(self)
        else:
            self.send(event)
        self.global_clock_prev = self.global_clock

    def process_simulation_terminate(self, event: Event):
        if not self.is_terminate_time_set:
            self.global_clock = self.global_clock_prev
        self.datacenter.process_simulation_terminate(event)

    def process_simulation_pause(self, event: Event):
        self.state = Simulator.State.PAUSED

    def send(self, event: Event) -> None:
        event.get_target().process(event)

    def run_util_pause_or_terminate(self) -> None:
        self.state = Simulator.State.RUNNING
        while self.state == Simulator.State.RUNNING and not self.event_queue.is_empty():
            event = self.event_queue.pop()
            self.global_clock = event.get_start_time()
            self.process(event)

    def add_event_listener(self, listener: EventListener):
        self.event_listener_list.append(listener)

    def add_circular_clock_listener(self, listener: CircularClockListener):
        self.circular_clock_listener_list.append(listener)
        self.event_queue.push(Event(
            source=None, target=self, event_type=Event.TYPE.CIRCULAR_CLOCK_EVENT, extra_data=None, start_time=0.0))

    def get_state(self) -> State:
        return self.state

    def set_state(self, state: State):
        self.state = state

    def set_datacenter(self, datacenter: Datacenter):
        self.datacenter = datacenter
        
    def get_datacenter(self)->Datacenter:
        return self.datacenter
