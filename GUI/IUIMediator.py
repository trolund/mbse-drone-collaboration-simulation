from abc import ABC


class IUIMediator(ABC):

    def notify(self, sender: object, event: str) -> None:
        pass
