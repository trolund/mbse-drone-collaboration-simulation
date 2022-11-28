import subprocess
import shutil
import configparser
import os
import time
from functools import reduce
import glob
from Logging.summary_stats import get_summary_stats
import numpy as np
import contextlib

from pathlib import Path
import json

config_name = './config.ini'
parameter_file_ext = '_params.json'

dir_path = Path(__file__).parent
simulation_batcher_data_path = Path(dir_path, './simulation_batcher/')
logging_folder = Path(dir_path, './Logging/Files/')
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


def run_simulation():
    process = subprocess.Popen(['python', 'simulation.py'],
                               stdout=subprocess.PIPE,
                               universal_newlines=True)
    while True:
        return_code = process.poll()
        if return_code is not None:
            return


def get_run_log_folder(name):
    return Path(simulation_batcher_data_path, name + '_logs')


def create_run(name, parameters, skip_completed=True):
    json_object = json.dumps(parameters, indent=4)
    parameter_file = os.path.join(
        simulation_batcher_data_path, Path('./' + name + parameter_file_ext))
    run_log_folder = get_run_log_folder(name)
    os.makedirs(run_log_folder, exist_ok=True)
    with open(parameter_file, "w") as outfile:
        outfile.write(json_object)

    step_idxes = [0] * len(parameters)
    combinations = reduce(
        lambda x, y: x*y, list(map(lambda param: len(param[1]), parameters)))

    config = configparser.RawConfigParser()
    config.read("config.ini")
    config.set('graphics', 'headless', 1)

    for i in range(combinations):
        log_destination = Path(run_log_folder, str(i) + '.log')

        if not log_destination.is_file():
            print(f'Running simulation {i + 1}/{combinations}')
            for param_idx in range(len(parameters)):
                param_name, param_range = parameters[param_idx][0], parameters[param_idx][1]
                param_val = param_range[step_idxes[param_idx]]

                config.set('setup', param_name, param_val)
                with open(config_path, 'w') as configfile:
                    config.write(configfile)

            run_simulation()

            list_of_logs = glob.glob(str(logging_folder) + '/*.log')
            latest_file = max(list_of_logs, key=os.path.getctime)
            shutil.move(latest_file, log_destination)

        def step_idx(idx):
            if idx > len(step_idxes) - 1:
                return
            step_idxes[idx] += 1
            if (step_idxes[idx] > len(parameters[idx][1]) - 1):
                step_idxes[idx] = 0
                step_idx(idx + 1)
        step_idx(0)


if __name__ == "__main__":
    name = 'droneDistance_nrDrones_customerDensity'
    create_run(name, [
        ('number_of_drones', list(range(1, 51, 1))),
        ('customer_density',  list(np.linspace(0.1, 1, 9, endpoint=False))),
        ('moving_truck',  [0, 1])
    ])
    shutil.move(config_backup_path, config_path)

    files = glob.glob(str(Path(get_run_log_folder(name), '*')))
    summery_stats_path = Path(simulation_batcher_data_path, name + '.csv')
    with contextlib.suppress(FileNotFoundError):
        os.remove(summery_stats_path)
    get_summary_stats(files, summery_stats_path)

    # os.system('shutdown /s /t 1')
