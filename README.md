# Model-Based Systems Engineering - Simulating a futuristic package delivery service using drones.

This project have been done as a part of the course 02223 - Model-Based Systems Engineering at DTU in the Fall of 2022

## Dependencies 

To run the project please install the following packages by using pip or pip3:

    pip3 install pygame pygame_gui dependency_injector

## Config 

The main config file **config.ini** contains all the global parameters. the file is group by sections '[section]'

* scale - the scale the simulation starts at.

# Definitions (Conventions of the project)


## ENV service (env_service.py) 

Creates the 2D representation of a neighborhood

#### Neighborhood (env) structure

* Road : "R"
* Ground: “.”
* Delivery spot: "S"
* Truck: "T"

  
For instance will the input (world_size=15, ground_size=5, road_size=1, customer_density=0.5) result in the neighborhood
below. This representation is called a layout in the code. **Please change the parameters in the main config file**.

    (layout, delivery_sports, number_of_grounds, number_of_customers), truck_pos = create_layout_env(15, 5, 1, 0.5)

     R  R  R  R  R  R  R  R  R  R  R  R  R  R  R  R 
     R  .  .  .  .  R  .  S  .  .  R  .  .  .  .  R 
     R  .  .  .  .  R  .  .  .  .  R  .  .  .  .  R 
     R  .  .  .  .  T  .  .  .  .  R  .  .  .  .  R 
     R  S  .  .  .  R  .  .  .  .  R  .  .  S  .  R 
     R  R  R  R  R  R  R  R  R  R  R  R  R  R  R  R 
     R  .  .  S  .  R  .  .  .  .  R  .  .  .  .  R 
     R  .  .  .  .  R  .  .  .  .  R  .  .  .  .  R 
     R  .  .  .  .  R  .  .  .  .  R  .  .  .  .  R 
     R  .  .  .  .  R  .  .  .  .  R  .  .  .  .  R 
     R  R  R  R  R  R  R  R  R  R  R  R  R  R  R  R 
     R  .  .  .  .  R  .  .  S  .  R  .  .  .  .  R 
     R  .  .  .  .  R  .  .  .  .  R  .  .  .  .  R 
     R  .  .  .  .  R  .  .  .  .  R  .  .  .  .  R 
     R  .  .  .  .  R  .  .  .  .  R  .  .  .  .  R 
     R  R  R  R  R  R  R  R  R  R  R  R  R  R  R  R 

A layout can be printed out byt using **print_layout(layout)**.

# truck path finding

Applying the path-finder to the layout above gives following route. 

* Start point = (0,0)
* End point = (len(layout) - 1, len(layout) - 1))


    planner = PatchFinder()

    route = planner.find_path(layout, (0, 0), (len(layout) - 1, len(layout) - 1))

The route is marked with the character "M".
    
    # the route it self
    [(0, 0), (15, 15), (14, 15), (13, 15), (12, 15), (11, 15), (10, 15), (10, 14), (10, 13), (10, 12), (10, 11), (10, 10), (9, 10), (8, 10), (7, 10), (6, 10), (5, 10), (5, 9), (5, 8), (5, 7), (5, 6), (5, 5), (4, 5), (3, 5), (2, 5), (1, 5), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (15, 15)]
    
    # shown in layout
     M  M  M  M  M  M  R  R  R  R  R  R  R  R  R  R 
     R  .  .  .  .  M  .  .  .  .  R  .  .  .  .  R 
     R  .  .  .  .  M  .  .  .  .  R  .  .  .  .  R 
     R  .  .  .  S  M  .  .  .  .  R  S  .  .  .  R 
     R  .  .  .  .  M  .  .  .  .  R  .  .  .  .  R 
     R  R  R  R  R  M  M  M  M  M  M  R  R  R  R  R 
     R  .  .  .  .  R  .  .  .  .  M  .  .  .  .  R 
     R  .  .  .  .  R  .  .  .  .  M  .  .  .  .  R 
     R  .  .  .  .  R  .  .  .  .  M  .  .  .  .  R 
     R  .  .  .  .  R  .  .  S  .  M  .  .  .  S  R 
     R  R  R  R  R  R  R  R  R  R  M  M  M  M  M  M 
     R  .  .  .  .  R  .  S  .  .  R  .  .  .  .  M 
     R  .  .  .  .  R  .  .  .  .  R  .  .  .  .  M 
     R  .  .  .  .  R  .  .  .  .  R  .  .  .  .  M 
     R  .  .  .  .  R  .  .  .  .  R  .  .  .  .  M 
     R  R  R  R  R  R  R  R  R  R  R  R  R  R  R  M 

# TODO list

  * Make sure the Drones fly with a realistic speed that is based on size of the world.
=======
# Definitions 

## Neighborhood (env) structure

* Road : "R"
* Ground: "G"
* Delivery spot: "S"
* House : "H" (could be nice)
