from cairo import Surface

from Cominication_hub import Mediator


class BaseUIComponent:

    def __init__(self, screen: Surface, mediator: Mediator = None) -> None:
        self._screen = screen
        self._mediator = mediator

    @property
    def mediator(self) -> Mediator:
        return self._mediator

    @mediator.setter
    def mediator(self, mediator: Mediator) -> None:
        self._mediator = mediator
