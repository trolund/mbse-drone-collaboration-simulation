import logging


class EventLogger:

    def __init__(self) -> None:
        self.log_in_memory = []
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}", )

    def log(self, msg, show_in_ui: bool = True):
        if show_in_ui:
            self.log_in_memory.insert(0, msg)
        self.logger.debug(msg)

    def get_log(self):
        return self.log_in_memory
