from dependency_injector.wiring import Provide

from Logging.eventlogger import EventLogger
from Models.env import Env
from containers import Container


class DroneController:

    def __init__(self, task_manager, drones_ref,  logger: EventLogger = Provide[Container.event_logger], config=Provide[Container.config], env: Env = Provide[Container.env]):

        self.config = config
        self.logger = logger
        self.env_ref = env
        self.task_manager = task_manager
        self.all_drones = drones_ref
        self.ready_list = []


