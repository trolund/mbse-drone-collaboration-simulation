import pygame
import pygame_gui

from GUI.BaseUIComponent import BaseUIComponent


class LogComponent(BaseUIComponent):

    def __init__(self):
        self.list = pygame_gui.elements.UISelectionList(
            relative_rect=pygame.Rect(self.ui_x, self.screen.get_height() - 200, 400, 150),
            manager=self.manager, item_list=[]
        )

    def do_a(self) -> None:
        print("Component 1 does A.")
        self.mediator.notify(self, "A")

    def do_b(self) -> None:
        print("Component 1 does B.")
        self.mediator.notify(self, "B")