# Load and initialize Modules here
import pygame
import pygame_gui
from dependency_injector.wiring import Provide

from GUI.UI import UI
from Logging.eventlogger import EventLogger
from Models.basic_types import Pos
from Models.colors import WHITE
from Models.drone import Drone
from Models.env import Env
from Models.setup import FPS
from Models.task import Task
from Models.truck import Truck
from Services.env_service import draw_layout, grid_to_pos, get_world_size, create_layout_env
from Services.task_manager import create_random_tasks, sort_tasks, print_tasks
from containers import Container

pygame.init()
pygame.font.init()
pygame.mixer.init()

pygame.display.set_caption("DRONE SIMULATION - MBSE - GROUP 2 (2022)")
pygame.font.Font(None, 22)


# Main Class
class MainRun(object):

    def __init__(self, logger: EventLogger = Provide[Container.event_logger], config=Provide[Container.config],
                 env: Env = Provide[Container.env]):
        logger.log("Starting Simulation 🚀")
        self.env = env
        self.config = config

        self.scale: int = 1
        self.truck_pos_random: bool = False
        self.fixed_truck_pos: Pos = (0, 0)

        self.OffsetX = 0
        self.OffsetY = 0

        self.screen = pygame.display.set_mode((1200, 800))

        self.is_running = True
        self.Main()

    def create_drones(self, env: Env, number_of_drones: int):
        for d in range(0, number_of_drones):
            drone = Drone(self.scale, "done_" + str(d))
            # start at x, y
            drone.rect.x = env.home[0]
            drone.rect.y = env.home[1]
            env.sprites.add(drone)

    def create_tasks(self, env: Env, possible_addresses, number_of_tasks):
        tasks = create_random_tasks(possible_addresses, number_of_tasks)

        for idx, t in enumerate(tasks):
            # start at truck
            t.rect.x = env.home[0] + (5 * idx)
            t.rect.y = env.home[1]

            env.task_ref.append(t)
            env.sprites.add(t)

        env.task_ref = sort_tasks(env.task_ref, env.home)

        print_tasks(env.task_ref, env.home)


    def create_truck(self, env: Env, pos):
        truck = Truck(pos, self.scale)
        env.home = truck.get_home()
        env.sprites.add(truck)

    def draw_layers(self, layout, x_len: int, y_len: int, step_size: int, env):
        # draw the basic layout
        draw_layout(self.screen, layout, x_len, y_len, step_size, self.scale, self.OffsetX, self.OffsetY)

        # update all sprites
        env.sprites.update(self.scale)
        # draw all sprites
        for t in env.sprites:
            # scale images
            t.image = pygame.transform.scale(t.images[0], (t.width * self.scale, t.height * self.scale))
            self.screen.blit(t.image, [(t.rect.x * self.scale + self.OffsetX), (t.rect.y * self.scale + self.OffsetY)])

    def set_scale(self, val):
        temp = self.scale + val
        if temp < 1:
            self.scale = 1
            # self.adjust_zoom_offset(val)
        else:
            if not temp > 10:
                self.scale = temp
                # self.adjust_zoom_offset(val)


    def adjust_zoom_offset(self, change):
        locationX = (self.world_size - self.screen.get_width()) / self.scale
        locationY = (self.world_size - self.screen.get_height()) / self.scale

        if change < 0:
           self.OffsetX += locationX
           self.OffsetY += locationY
        else:
           self.OffsetX -= locationX
           self.OffsetY -= locationY

    def create_window(self, config):
        is_fullscreen = False if config["graphics"]["fullscreen"] == "0" else True

        if is_fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            w = float(config["graphics"]["window_w"])
            h = float(config["graphics"]["window_h"])
            self.screen = pygame.display.set_mode((w, h))

    def get_config(self, config):
        self.scale = float(config["graphics"]["scale"])
        self.truck_pos_random = bool(config["setup"]["truck_pos_random"])
        a = config["setup"]["fixed_truck_pos"].split(",")
        self.fixed_truck_pos = (int(a[0]), int(a[1]))

        self.world_size = int(self.config["setup"]["world_size"])
        self.ground_size = int(self.config["setup"]["ground_size"])
        self.road_size = int(self.config["setup"]["road_size"])
        self.customer_density = float(self.config["setup"]["customer_density"])
        self.truck_pos_random = False if self.config["setup"]["truck_pos_random"] == "0" else True
        a = self.config["setup"]["fixed_truck_pos"].split(",")
        self.fixed_truck_pos = (int(a[0]), int(a[1]))
        self.number_of_tasks = int(self.config["setup"]["number_of_tasks"])
        self.number_of_drones = int(self.config["setup"]["number_of_drones"])

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
        # create the window from config
        self.create_window(self.config)

        # get config
        self.get_config(self.config)

        # setup layout
        (layout, delivery_sports, number_of_grounds, number_of_customers), truck_pos = create_layout_env(self.world_size,
                                                                                                         self.ground_size,
                                                                                                         road_size=self.road_size,
                                                                                                         change_of_customer=self.customer_density,
                                                                                                         random_truck_pos=self.truck_pos_random)
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
        self.create_truck(self.env, grid_to_pos(truck_pos[0], truck_pos[1], step_size, self.scale))
        self.create_tasks(self.env, delivery_sports, self.number_of_tasks)
        self.create_drones(self.env, self.number_of_drones)

        # Simulation/game loop
        clock = pygame.time.Clock()

        while self.is_running:
            time_delta = clock.tick(FPS) / 1000.0
            self.keyboard_input()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
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
            ui.update(time_delta, clock.get_fps(), self.scale)

            pygame.display.flip()

            # update screen with new drawings
            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    # setup dependency injection
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    MainRun()
