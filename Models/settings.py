class Settings:

    def __init__(self, config):

        # simulation config
        a = config["setup"]["fixed_truck_pos"].split(",")
        self.fixed_truck_pos = (int(a[0]), int(a[1]))
        self.world_size = int(config["setup"]["world_size"])
        self.ground_size = int(config["setup"]["ground_size"])
        self.road_size = int(config["setup"]["road_size"])
        self.customer_density = float(config["setup"]["customer_density"])
        self.moving_truck = False if config["setup"]["moving_truck"] == "0" else True
        self.random_position = False if config["setup"]["random_position"] == "0" else True
        self.number_of_tasks = int(config["setup"]["number_of_tasks"])
        self.number_of_drones = int(config["setup"]["number_of_drones"])
        self.truck_pos = None
        self.simulation_speed = int(config["setup"]["simulation_speed"])
        self.auto_close_window = False if config["setup"]["auto_close_window"] == "0" else True
        self.seed = 1

        if 'fixed_package_weight' in config["setup"]:
            fixed_package_weight = int(config["setup"]["fixed_package_weight"])
            print('setting the package weight to', fixed_package_weight)
            self.max_package_weight = fixed_package_weight
            self.min_package_weight = fixed_package_weight
        else:
            print('no fixed package weight')
            self.max_package_weight = int(
                config["setup"]["max_package_weight"])
            self.min_package_weight = int(
                config["setup"]["min_package_weight"])

        # screen
        self.scale = float(config["graphics"]["scale"])
        self.is_fullscreen = False if config["graphics"]["fullscreen"] == "0" else True
        self.width = float(config["graphics"]["window_w"])
        self.height = float(config["graphics"]["window_h"])
        self.headless = bool(int(config["graphics"]["headless"]))
