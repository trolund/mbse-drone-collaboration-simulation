from dependency_injector.wiring import Provide

from Models.drone import Drone
from Models.env import Env
from Models.ground import Ground
from Models.move_type import Move_Type
from Models.truck import Truck
from containers import Container
from Models.task import Task


class EnvBuilder:

    def __init__(self, env: Env = Provide[Container.env]):
        self.env = env
        self.create_env()

    def create_env(self):
        truck = Truck()
        self.env.trucks.add(truck)
        self.create_tasks()
        self.create_grounds()
        self.create_drones()

    def create_drones(self):
        for d in range(0, 4):
            drone = Drone("done_" + str(d))
            # start at x, y
            drone.rect.x = 0
            drone.rect.y = 0

            # movements
            # drone.add_move_point(300, 300)
            drone.add_move_point((200 + (d * 60), 200), Move_Type.PICKUP, self.env.get_task_at(200 + (d * 60), 200))
            # drone.add_move_point(300 * d, 300)
            # drone.add_move_point(900, 600 * d)
            drone.add_move_point(self.env.grounds[d].get_landing_spot_pos(True), Move_Type.DROP_OFF)
            # drone.add_move_point(900, 600 * d)
            drone.add_move_point((self.env.home[0], self.env.home[1] + (d * 70)))

            self.env.drones.add(drone)

    def create_tasks(self):
        for d in range(0, 4):
            task = Task()
            # start at x, y
            task.rect.x = 200 + (d * 60)
            task.rect.y = 200

            self.env.tasks.add(task)

    def create_grounds(self):
        self.env.grounds.append(Ground([(0, 0), (0, 500), (500, 500), (500, 0)], (0, 0)))
        self.env.grounds.append(Ground([(0, 0), (0, 500), (500, 500), (500, 0)], (700, 0)))
        self.env.grounds.append(Ground([(0, 0), (0, 500), (500, 500), (500, 0)], (0, 700)))
        self.env.grounds.append(Ground([(0, 0), (0, 500), (500, 500), (500, 0)], (700, 700)))