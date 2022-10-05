from dependency_injector.wiring import Provide

from Logging.eventlogger import EventLogger
from Models.env import Env
from Models.move_type import Move_Type
from containers import Container


class DroneManager:

    def __init__(self, logger: EventLogger = Provide[Container.event_logger], env: Env = Provide[Container.env]):

        self.logger = logger
        self.env = env

    # NOT implemented this is just a placeholder
    def plan_routes(self):
        for d in range(0, len(self.env.drones_ref)):
            drone = self.env.drones_ref[d]
            # movements
            if d == 4:
                drone.add_move_point((200 + (3 * 60), 200), Move_Type.PICKUP, self.env.get_task_at(200 + (2 * 60), 200))
            else:
                drone.add_move_point((200 + (d * 60), 200), Move_Type.PICKUP, self.env.get_task_at(200 + (d * 60), 200))
                drone.add_move_point(self.env.grounds[d].get_landing_spot_pos(offset=True), Move_Type.DROP_OFF)
                drone.add_move_point((self.env.home[0], self.env.home[1] + (d * 70)))


