# Model-Based Systems Engineering - Simulating a futuristic package delivery service using drones.

This project have been done as a part of the course 02223 - Model-Based Systems Engineering at DTU in the Fall of 2022

## Dependencies 

To run the project please install the following packages by using pip or pip3:

  pip3 install pygame pygame_gui dependency_injector

## Config 

The config file **config.ini** contains all the global parameters. the file is group by sections '[section]'

* scale - the scale the simulation starts at.

# Definitions (Conventions of the project)

## Neighborhood (env) structure

* Road : "R"
* Ground: “.”
* Delivery spot: "S"
* House : "H" (could be nice)

# Ideas to investigate 

* speed of truck 
    * How fast will the truck be able to drive through the streets?
    * Is this practical? - will it interrupt the "normal" traffic too much?
* Optimize order of packages fetched from truck
* Optimize flying patch of drones
* Optimize with delivering multiple packages at one time. (in container (task))
* Multiple drones lifting heavy packages.


# More detailed simulation

* Centered event system to make it easy to see ordering of events. 
  * could be outputted to log-file at each run. --> timestamp.txt

* Environment can be defined in som format (could be JSON)
  * Random package/task generation
    
* Drone Controller (in the truck) communication to Drone 
  * delay, errors, range. 
  * INFO: https://www.911security.com/learn/airspace-security/drone-fundamentals/drone-communication-data-link

* Drone 
  * Battery 
  * Motor error
  * Return to home on error
    
