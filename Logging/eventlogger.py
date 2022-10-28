import datetime
import logging

from tomlkit import date


class EventLogger:

    def __init__(self) -> None:
        self.log_in_memory = []
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}", )
        f = open("Logging\Files\logfile.log", "a")
        time = datetime.datetime.now()
        f.write(f"{time} New simulation started \n" )

    def log(self, msg, show_in_ui: bool = True):
        if show_in_ui:
            self.log_in_memory.insert(0, msg)
        self.logger.debug(msg)
        self.logOA(msg)

    def logOA(self,msg):
        time = datetime.datetime.now()
        line = f"{time} {msg} \n"
        f = open("Logging\Files\logfile.log", "a")
        f.write(line)
        f.close()

    def get_log(self):
        return self.log_in_memory


