import datetime
import logging

from Logging.summary_stats import make_summary_file

class EventLogger:

    def __init__(self) -> None:
        self.log_in_memory = []
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}", )

        self.logger.setLevel(logging.INFO)
        self.done = False
        now = datetime.datetime.now()
        date_time_str = now.strftime("%Y_%m_%d-%H_%M_%S")
        self.date = date_time_str
        file_name = ("Logging\Files\logfile_"+date_time_str+".log")
        self.file_name = file_name
        file = LogFile(file_name)
        file.write(f"{date_time_str} New simulation started" )
        self.file = file

    def log(self, msg, show_in_ui: bool = True):
        if not self.done:
            if show_in_ui:
                self.log_in_memory.insert(0, msg)
                self.logger.debug(msg)
            self.logOA(msg)
        if "Simulation finished at" in msg:
            self.done = True

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
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            line = f"{date_time_str};{msg}\n"
            file.write(line)
            file.close()
    
