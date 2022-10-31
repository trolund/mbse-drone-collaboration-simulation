import datetime
import logging

class EventLogger:

    def __init__(self) -> None:
        self.log_in_memory = []
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}", )
        date_time_str = datetime.datetime.strftime("%Y_%m_%d-%H_%M")
        self.date = date_time_str
        file_name = ("Logging\Files\logfile_"+date_time_str+".log")
        file = LogFile(file_name)
        file.write(f"{date_time_str} New simulation started \n" )
        self.file = file

    def log(self, msg, show_in_ui: bool = True):
        if show_in_ui:
            self.log_in_memory.insert(0, msg)
        self.logger.debug(msg)
        self.logOA(msg)

    def logOA(self,msg):
        file = self.file
        file.write(msg)

    def get_log(self):
        return self.log_in_memory


class LogFile(object):
    def __init__(self,file_name) -> None:
        self.file_name = file_name

    def write(self, msg):
        with open(self.file_name, "a") as file:
            now = datetime.datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M")
            line = f"{date_time_str};{msg}\n"
            file.write(line)
            file.close()