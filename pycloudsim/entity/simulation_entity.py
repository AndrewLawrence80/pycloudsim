from ..events import Event


class SimulationEntity:
    """
    A abstract class (interface) which can process simulation events
    """
    def process(self, event: Event):
        pass
