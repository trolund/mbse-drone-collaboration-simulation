import threading
from time import sleep

from dependency_injector.wiring import Provide

from Cominication_hub.ConcreteMediator import ConcreteMediator
from Logging.eventlogger import EventLogger
from Models.drone import Drone
from Models.env import Env
from Models.move_type import Move_Type
from Services.task_manager import TaskManager
from Utils.layout_utils import grid_to_pos_tuple
from containers import Container


class DroneController(ConcreteMediator):
    task_manager: TaskManager

    # contain the plan the drones will execute
    plan = {}

    def __init__(self, task_manager, drones_ref, step_size,
                 logger: EventLogger = Provide[Container.event_logger],
                 config=Provide[Container.config],
                 env: Env = Provide[Container.env]):
        # threading.Thread.__init__(self)
        super().__init__(drones_ref, logger)
        self.step_size = step_size
        self.thread_name = "Drone controller"

        self.config = config
        self.logger = logger
        self.env_ref = env
        self.task_manager = task_manager
        self.all_drones = drones_ref

        self.init_plan()

        for d in self.all_drones:
            self.ready_list.append(d)

    def init_plan(self):
        for d in self.all_drones:
            self.plan[d.id] = []

    def assign_tasks(self):
        if len(self.ready_list) > 0 and self.task_manager.get_number_of_packages_left() > 0:
            curr_drone: Drone = self.ready_list.pop()
            next_task = self.task_manager.get_head_package()
            delivery_address = grid_to_pos_tuple(next_task.address, self.step_size)

            # movements
            curr_drone.add_move_point((next_task.rect.x, next_task.rect.y), Move_Type.PICKUP, next_task)
            curr_drone.add_move_point(delivery_address, Move_Type.DROP_OFF)
            curr_drone.add_move_point(self.env_ref.home)
