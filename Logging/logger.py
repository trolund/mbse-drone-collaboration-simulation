from datetime import datetime

from Logging.log_type import LogType


class Logger:
    curr_log = []

    def log(self, msg, type=LogType.NORMAL):
        dt = datetime.now()
        ts = datetime.timestamp(dt)
        self.curr_log.append((msg, type, ts))


