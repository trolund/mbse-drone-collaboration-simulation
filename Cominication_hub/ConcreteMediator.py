from typing import List

from Cominication_hub.Mediator import Mediator


class ConcreteMediator(Mediator):

    _ready_drones = []

    def __init__(self, drones_ref) -> None:
        self.setUpDrones(drones_ref)

    # make sure all drones know how to communicate
    def setUpDrones(self, drones_ref):
        for d in drones_ref:
            d.mediator = self

    # adapt to messages from drones
    def notify(self, sender: object, event: str) -> None:
        if event == "Ready":
            self._ready_drones.append(sender)
        elif event == "Error":
            print("Drone have error")
        elif event == "Battery Low":
            print("Drone have Low battery")
