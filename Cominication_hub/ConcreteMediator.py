from Cominication_hub.Mediator import Mediator
from Logging.eventlogger import EventLogger
from Models.drone import Drone


class ConcreteMediator(Mediator):

    ready_list = []

    def __init__(self, drones_ref, logger: EventLogger) -> None:
        self.logger = logger
        self.setUpDrones(drones_ref)

    # make sure all drones know how to communicate
    def setUpDrones(self, drones_ref):
        for d in drones_ref:
            d.mediator = self

    # adapt to messages from drones
    def notify(self, sender: Drone, event: str) -> None:
        if event == "Ready":
            if sender not in self.ready_list:
                self.logger.log(sender.name + " " + "ready")
                self.ready_list.append(sender)
        elif event == "Error":
            print("Drone have error")
        elif event == "Battery Low":
            print("Drone have Low battery")
