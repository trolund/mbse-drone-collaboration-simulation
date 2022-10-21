import os

import pygame
import pygame_gui
from dependency_injector.wiring import Provide
from pygame.surface import Surface
from pygame_gui.core import ObjectID

from Logging.eventlogger import EventLogger
from Models.colors import GREY
from containers import Container


class UI:

    def __init__(self, setScale, screen: Surface,
                 logger: EventLogger = Provide[Container.event_logger],
                 config=Provide[Container.config]):
        self.log_list = None
        self.FPS_label = None
        self.delta_label = None
        self.label1 = None
        self.scale_label = None
        self.button_scale_down = None
        self.button_scale_up = None
        self.logger = logger
        self.config = config
        self.set_scale = setScale

        self.ui_width = 400
        self.margin = 30

        self.ui_width = screen.get_width() - self.ui_width
        self.ui_x = self.ui_width

        self.screen = screen
        self.manager = pygame_gui.UIManager((screen.get_width(), screen.get_height()),
                                            os.path.join("GUI", 'theme.json'))

        self.create_ui_elements()

    def create_ui_elements(self):

        self.button_scale_up = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.ui_x + self.margin, 200, 100, 30),
            text='scale up',
            manager=self.manager
        )

        self.button_scale_down = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.ui_x + self.margin, 235, 100, 30),
            text='scale down',
            manager=self.manager
        )

        self.scale_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(self.ui_x + self.margin, 100, 300, 100),
            text="scale: ",
            manager=self.manager
        )

        self.label1 = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(self.ui_x + self.margin, 100, 200, 100),
            text="Value",
            manager=self.manager
        )

        self.delta_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(self.screen.get_width() - 150, self.screen.get_height() - 80, 200, 100),
            text="Delta: 0.0",
            manager=self.manager,
            object_id=ObjectID(class_id='#debug_text', object_id="debug")
        )

        self.FPS_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(self.screen.get_width() - 150, self.screen.get_height() - 60, 200, 100),
            text="FPS: 0.0",
            manager=self.manager,
            object_id=ObjectID(class_id='#debug_text', object_id="debug")
        )

        self.log_list = pygame_gui.elements.UISelectionList(
            relative_rect=pygame.Rect(self.ui_x, self.screen.get_height() - 200, 400, 150),
            manager=self.manager, item_list=[]
        )

    def handle_events(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.button_scale_up:
                    self.set_scale(0.2)
                if event.ui_element == self.button_scale_down:
                    self.set_scale(-0.2)

        self.manager.process_events(event)

    def update(self, time_delta: float, fps: float, scale: float):
        pygame.draw.rect(self.screen, GREY, pygame.Rect(self.ui_x, 0, self.ui_width, self.screen.get_height()))
        self.delta_label.set_text("Delta: " + str(time_delta))
        self.FPS_label.set_text("FPS: " + str(fps))
        self.scale_label.set_text(str(scale))
        self.update_event_list()
        self.manager.update(time_delta)
        self.manager.draw_ui(self.screen)

    def update_event_list(self):
        self.log_list.set_item_list(self.logger.get_log())

    def get_manager(self):
        return self.manager
