from enum import Enum


class DroneMode(Enum):
    BUSY = 0,  # drone is doing a task
    IDLE = 1,  # drone do nothing
    DOCK = 2   # drone is in dock on the truck
    ERROR = 3  # the drone have an error that make it unable to fly
