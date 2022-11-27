import subprocess
import shutil
import configparser
import os
import time
from functools import reduce

from pathlib import Path
import json

config_name = './config.ini'
parameter_file_ext = '_params.json'

dir_path = Path(__file__).parent
simulation_batcher_data_path = Path(dir_path, './simulation_batcher/')
config_path = Path(dir_path, config_name)
config_backup_path = Path(simulation_batcher_data_path, config_name)

os.makedirs(simulation_batcher_data_path, exist_ok=True)
if not config_backup_path.is_file():
    shutil.copyfile(config_path, config_backup_path)


# Parameters structure:
# [
#    (parameter1_name, [0, 1, 3])
#    (parameter2_name, [0, 1, 3, 5, 6])
# ]
config = configparser.RawConfigParser()


def create_run(name, parameters):
    json_object = json.dumps(parameters, indent=4)
    parameter_file = os.path.join(
        simulation_batcher_data_path, Path('./' + name + parameter_file_ext))
    with open(parameter_file, "w") as outfile:
        outfile.write(json_object)

    step_idxes = [0] * len(parameters)
    combinations = reduce(
        lambda x, y: x*y, list(map(lambda param: len(param[1]), parameters)))

    param_list = []
    for i in range(combinations):
        print(f'Running simulation {i + 1}/{combinations}')
        config.read("config.ini")
        param_list.append([])
        for param_idx in range(len(parameters)):
            param_name, param_range = parameters[param_idx][0], parameters[param_idx][1]
            param_val = param_range[step_idxes[param_idx]]
            param_list[i].append(param_val)

            config.set('setup', param_name, param_val)
            with open(config_path, 'w') as configfile:
                config.write(configfile)

        # run simulation
        time.sleep(2)

        def step_idx(idx):
            if idx > len(step_idxes) - 1:
                return
            step_idxes[idx] += 1
            if (step_idxes[idx] > len(parameters[idx][1]) - 1):
                step_idxes[idx] = 0
                step_idx(idx + 1)
        step_idx(0)
    print(param_list)


create_run('test', [
    ('param1', [0, 2]),
    ('param2', list(range(5, 20, 2))),
    ('param3', [0, 2, 9]),
])

if __name__ == "__main__":
    for x in range(1):
        process = subprocess.Popen(['python', 'simulation.py'],
                                   stdout=subprocess.PIPE,
                                   universal_newlines=True)

        config = configparser.RawConfigParser()
        config.read("config.ini")
        print("-----------------------------")
        print(config.get("setup", "moving_truck"))
        print("-----------------------------")

        print(config)

        while True:
            output = process.stdout.readline()
            print(output.strip())
            # Do something else
            return_code = process.poll()
            if return_code is not None:
                print('RETURN CODE', return_code)
                # Process has finished, read rest of the output
                for output in process.stdout.readlines():
                    print(output.strip())
                break
