from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..events import Event
    from ..simulation import Simulator
class EventListener:
    def __init__(self,event_type:Event.TYPE) -> None:
        self.event_type=event_type
    
    def update(event:Event,simulator:Simulator)->None:
        pass
