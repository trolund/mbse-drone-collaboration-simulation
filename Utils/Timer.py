from dependency_injector.wiring import Provide

from Logging.eventlogger import EventLogger
from containers import Container


class Timer:
    time: float

    def __init__(self, logger: EventLogger = Provide[Container.event_logger]):
        self.time = 0

    def reset(self):
        self.time = 0

    def add_delta_time(self, delta):
        self.time += delta

    def get_time(self):
        return self.time

    def get_time_string(self):
        return f"{'{0:.2f}'.format(self.time)}s"
    
    def get_time_log(self):
        return f"{'{0:.5f}'.format(self.time)}"
