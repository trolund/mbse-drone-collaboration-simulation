import pygame
import pygame_gui
from dependency_injector.wiring import Provide

from GUI.UI import UI
from Logging.eventlogger import EventLogger
from Models.settings import Settings
from Models.colors import WHITE
from Models.drone import Drone
from Models.env import Env
from Models.setup import FPS
from Models.truck import Truck
from Services.Task_creater import create_random_tasks
from Services.drone_controller import DroneController
from Services.task_manager import TaskManager
from Utils.layout_utils import draw_layout, grid_to_pos, get_world_size, create_layout_env
from containers import Container

pygame.init()
pygame.font.init()
pygame.mixer.init()

pygame.font.Font(None, 22)

name = "DRONE SIMULATION - MBSE - GROUP 2 (2022)"


class Simulation(object):

    def __init__(self, logger: EventLogger = Provide[Container.event_logger],
                 config=Provide[Container.config],
                 env: Env = Provide[Container.env]):

        pygame.display.set_caption(name)
        logger.log("Starting Simulation 🚀 - " + name, show_in_ui=False)

        self.settings = Settings(config)
        logger.log("Config loaded 🛠", show_in_ui=False)

        self.drone_controller = None
        self.task_manager = None
        self.env = env
        self.config = config

        self.screen = None
        self.drones_ref = None

        self.OffsetX = 0
        self.OffsetY = 0

        self.is_running = True

        # create the window from config
        self.create_window()

        self.Main()

    def create_drones(self, env: Env, step_size, number_of_drones: int):

        self.drones_ref = []

        for d in range(0, number_of_drones):
            drone = Drone(self.settings.scale, "done_" + str(d))
            # start at x, y
            drone.rect.x = env.home[0]
            drone.rect.y = env.home[1]
            env.sprites.add(drone)
            self.drones_ref.append(drone)

        self.drone_controller = DroneController(self.task_manager, self.drones_ref, step_size)

    def create_tasks(self, env: Env, possible_addresses, number_of_tasks):

        tasks = create_random_tasks(possible_addresses, number_of_tasks)

        for idx, t in enumerate(tasks):
            # start at truck
            t.rect.x = env.home[0]  # + (5 * idx)
            t.rect.y = env.home[1]

            env.task_ref.append(t)
            env.sprites.add(t)

        self.task_manager = TaskManager()

    def create_truck(self, env: Env, pos):
        truck = Truck(pos, self.settings.scale)
        env.home = truck.get_home()
        env.sprites.add(truck)

    def draw_layers(self, layout, x_len: int, y_len: int, step_size: int, env):
        # draw the basic layout
        draw_layout(self.screen, layout, x_len, y_len, step_size, self.settings.scale, self.OffsetX, self.OffsetY)

        # update all sprites
        env.sprites.update(self.settings.scale)
        # draw all sprites on top of layout
        for t in env.sprites:
            # scale images
            t.image = pygame.transform.scale(t.images[0],
                                             (t.width * self.settings.scale, t.height * self.settings.scale))
            self.screen.blit(t.image, [(t.rect.x * self.settings.scale + self.OffsetX),
                                       (t.rect.y * self.settings.scale + self.OffsetY)])

    def set_scale(self, val):
        temp = self.settings.scale + val
        if temp < 1:
            self.settings.scale = 1
            # self.adjust_zoom_offset(val)
        else:
            if not temp > 10:
                self.settings.scale = temp
                # self.adjust_zoom_offset(val)

    def adjust_zoom_offset(self, change):
        locationX = (self.settings.world_size - self.screen.get_width()) / self.settings.scale
        locationY = (self.settings.world_size - self.screen.get_height()) / self.settings.scale

        if change < 0:
            self.OffsetX += locationX
            self.OffsetY += locationY
        else:
            self.OffsetX -= locationX
            self.OffsetY -= locationY

    def create_window(self):
        if self.settings.is_fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.settings.width, self.settings.height))

    def keyboard_input(self):
        offset_factor = 5
        zoom_factor = 0.2

        keys = pygame.key.get_pressed()  # checking pressed keys

        # move camera
        if keys[pygame.K_LEFT]:
            self.OffsetX += offset_factor
        if keys[pygame.K_RIGHT]:
            self.OffsetX -= offset_factor
        if keys[pygame.K_UP]:
            self.OffsetY += offset_factor
        if keys[pygame.K_DOWN]:
            self.OffsetY -= offset_factor

        # zoom
        if keys[pygame.K_u]:
            self.set_scale(zoom_factor)
        if keys[pygame.K_d]:
            self.set_scale(-zoom_factor)

    def Main(self):
        # setup layout
        (layout, delivery_sports, number_of_grounds, number_of_customers), truck_pos = create_layout_env(
            self.settings.world_size,
            self.settings.ground_size,
            road_size=self.settings.road_size,
            change_of_customer=self.settings.customer_density,
            random_truck_pos=self.settings.truck_pos_random)
        (step_size, x_len, y_len) = get_world_size(self.screen, layout)

        # instance of UI
        ui = UI(self.set_scale, self.screen)

        is_paused = True

        pause_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.screen.get_width() - 400, self.screen.get_height() - 40, 100, 30),
            text="▶ Start",
            manager=ui.get_manager()
        )

        # create all objects in the environment
        self.create_truck(self.env, grid_to_pos(truck_pos[0], truck_pos[1], step_size, self.settings.scale))
        self.create_tasks(self.env, delivery_sports, self.settings.number_of_tasks)
        self.create_drones(self.env, step_size, self.settings.number_of_drones)

        self.drone_controller.start()

        # Simulation/game loop
        clock = pygame.time.Clock()

        while self.is_running:
            time_delta = clock.tick(FPS) / 1000.0
            self.keyboard_input()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == pause_btn:
                            is_paused = not is_paused
                            pause_btn.set_text("▶ Resume" if is_paused else "Pause")

                ui.handle_events(event)

            if not is_paused:
                # clear background
                self.screen.fill(WHITE)

                # draw object layers
                self.draw_layers(layout, x_len, y_len, step_size, self.env)

            # update and draw UI
            ui.update(time_delta, clock.get_fps(), self.settings.scale)

            pygame.display.flip()

            # update screen with new drawings
            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    # setup dependency injection
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    Simulation()
