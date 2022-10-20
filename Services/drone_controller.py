from random import randrange
from typing import List

from dependency_injector.wiring import Provide

from Cominication_hub.ConcreteMediator import ConcreteMediator
from Logging.eventlogger import EventLogger
from Models.env import Env
from Services.task_manager import TaskManager
from containers import Container


class DroneController(ConcreteMediator):

    task_manager: TaskManager

    # contain the plan the drones will execute
    plan = {}

    def __init__(self, task_manager, drones_ref,
                 logger: EventLogger = Provide[Container.event_logger],
                 config = Provide[Container.config],
                 env: Env = Provide[Container.env]):

        super().__init__(drones_ref)
        self.config = config
        self.logger = logger
        self.env_ref = env
        self.task_manager = task_manager
        self.all_drones = drones_ref
        self.ready_list = []

    def init_plan(self):
        for d in self.all_drones:
            self.plan[d.id] = []

    def start_Delivery(self):

        while not self.task_manager.is_done():
            curr_drone = self.ready_list.pop()

            print(curr_drone)






