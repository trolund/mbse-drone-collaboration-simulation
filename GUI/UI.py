import os

import pygame
import pygame_gui
from dependency_injector.wiring import Provide
from pygame.surface import Surface
from pygame_gui.core import ObjectID

from Logging.eventlogger import EventLogger
from Models.colors import GREY
from Models.env import Env
from Models.settings import Settings
from Utils.Timer import Timer
from containers import Container


class UI:

    def __init__(self, setScale, set_simulation_speed, toggle_paused, settings: Settings, screen: Surface,
                 logger: EventLogger = Provide[Container.event_logger],
                 config=Provide[Container.config],
                 env: Env = Provide[Container.env]):

        # setup
        self.logger = logger
        self.config = config
        self.env = env

        self.ui_width = 400
        self.margin = 30

        self.ui_width = screen.get_width() - self.ui_width
        self.ui_x = self.ui_width

        self.screen = screen
        self.manager = pygame_gui.UIManager((screen.get_width(), screen.get_height()),
                                            os.path.join("GUI", 'theme.json'))

        # elements
        self.log_list = None
        self.FPS_label = None
        self.delta_label = None
        self.timer_label = None
        self.scale_label = None
        self.button_scale_down = None
        self.button_scale_up = None
        self.pause_btn = None
        self.packages_left_label = None

        # funcs
        self.toggle_paused = toggle_paused
        self.set_simulation_speed = set_simulation_speed
        self.set_scale = setScale

        # create all elements
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

        self.timer_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(self.ui_x + 50, self.screen.get_height() - 280, 150, 75),
            text="time",
            manager=self.manager,
            object_id=ObjectID(class_id='#timer')
        )

        self.packages_left_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(self.ui_x + 150 + 51, self.screen.get_height() - 280, 150, 75),
            text="time",
            manager=self.manager,
            object_id=ObjectID(class_id='#timer')
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

        self.pause_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.screen.get_width() - 400, self.screen.get_height() - 40, 100, 30),
            text="▶ Start",
            manager=self.manager
        )

        self.simulation_speed_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(self.ui_x + 50, self.screen.get_height() - 380, 250, 75),
            manager=self.manager,
        )

    def handle_events(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.button_scale_up:
                    self.set_scale(0.2)
                if event.ui_element == self.button_scale_down:
                    self.set_scale(-0.2)
                if event.ui_element == self.pause_btn:
                    self.toggle_paused(self.pause_btn)
            if event.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                if event.ui_element == self.simulation_speed_input:
                    try:
                        f = float(event.text)
                        if f <= 0:
                            return
                        self.set_simulation_speed(f)
                    except ValueError:
                        pass
                    

        self.manager.process_events(event)

    def on_frame(self, scale: float, timer: Timer):
        pygame.draw.rect(self.screen, GREY, pygame.Rect(self.ui_x, 0, self.ui_width, self.screen.get_height()))
        self.packages_left_label.set_text(str(len(self.env.task_ref)))
        self.scale_label.set_text(str(scale))
        self.timer_label.set_text(timer.get_time_string())
        self.manager.draw_ui(self.screen)
        self.update_event_list()
    
    def on_tick(self, delta):
        self.manager.update(delta)

    def update_event_list(self):
        self.log_list.set_item_list(self.logger.get_log())

    def get_manager(self):
        return self.manager
