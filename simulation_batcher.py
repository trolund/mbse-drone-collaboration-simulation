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
import pandas as pd

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
    with subprocess.Popen(['python', 'simulation.py'], stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as process:
        for line in process.stdout:
            process.stdout.flush()
            print(line, end='')  # process line here

    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, process.args)

    # process = subprocess.Popen(['python', 'simulation.py'],
    #                            stdout=subprocess.PIPE,
    #                            universal_newlines=True)
    # while True:
    #     return_code = process.poll()
    #     process.
    #     if return_code is not None:
    #         if return_code == 0:
    #             return
    #         else:
    #             raise RuntimeError()


def get_run_log_folder(name):
    return Path(simulation_batcher_data_path, name + '_logs')


def create_run(name, parameters, skip_completed=True, skip_all_simulations=False):
    json_object = json.dumps(parameters, indent=4)
    parameter_file = os.path.join(
        simulation_batcher_data_path, Path('./' + name + parameter_file_ext))
    run_log_folder = get_run_log_folder(name)
    os.makedirs(run_log_folder, exist_ok=True)
    with open(parameter_file, "w") as outfile:
        outfile.write(json_object)

    step_idxes = [0] * len(parameters)
    param_values = []
    param_names = []
    for param_idx in range(len(parameters)):
        param_names.append(parameters[param_idx][0])

    combinations = reduce(
        lambda x, y: x*y, list(map(lambda param: len(param[1]), parameters)))

    config = configparser.RawConfigParser()
    config.read("config.ini")
    config.set('graphics', 'headless', 1)

    for i in range(combinations):
        log_destination = Path(run_log_folder, str(i) + '.log')
        param_values.append([])

        should_run_this_run = (not log_destination.is_file(
        ) or not skip_completed) and not skip_all_simulations

        for param_idx in range(len(parameters)):
            param_name, param_range = parameters[param_idx][0], parameters[param_idx][1]
            param_val = param_range[step_idxes[param_idx]]
            param_values[i].append(param_val)

            if should_run_this_run:
                config.set('setup', param_name, param_val)

        if should_run_this_run:
            with open(config_path, 'w') as configfile:
                config.write(configfile)

            print(f'Running simulation {i + 1}/{combinations}')
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

    return {
        'names': param_names,
        'values': param_values
    }


if __name__ == "__main__":
    # name = 'all_the_params'
    # parameter_combinations = create_run(name, [
    #     ('number_of_tasks', list(range(1, 401, 50))),
    #     ('number_of_drones',  list(range(1, 51, 10))),
    #     ('drone_speed',  list(range(50, 601, 50))),
    #     ('truck_speed',  list(range(50, 601, 50)))
    # ], skip_all_simulations=False)

    name = 'simulationDuration_numberOfDrones_nrOfTasks'
    parameter_combinations = create_run(name, [
        ('number_of_tasks', [1, 50, 100, 150, 200, 250, 300]),
        ('number_of_drones',  list(range(1, 25, 1)))
    ], skip_all_simulations=False)

    shutil.move(config_backup_path, config_path)

    parameter_df = pd.DataFrame(columns=parameter_combinations['names'],
                                data=parameter_combinations['values'])

    # create the summary stats
    files = glob.glob(str(Path(get_run_log_folder(name), '*')))
    files.sort(key=lambda i: int(os.path.splitext(os.path.basename(i))[0]))
    summery_stats_path = Path(simulation_batcher_data_path, name + '.csv')
    with contextlib.suppress(FileNotFoundError):
        os.remove(summery_stats_path)
    get_summary_stats(files, summery_stats_path)
    # add parameters to file
    summary_stats_df = pd.read_csv(summery_stats_path)
    summary_stats_complete_df = pd.concat(
        [parameter_df, summary_stats_df], axis=1)
    summary_stats_complete_df.to_csv(summery_stats_path, index=False)

    # os.system('shutdown /s /t 1')


################  Generate droneDistance_nrDrones_customerDensity ###########
# name = 'droneDistance_nrDrones_customerDensity'
# create_run(name, [
#     ('number_of_drones', list(range(1, 51, 1))),
#     ('customer_density',  list(np.linspace(0.1, 1, 9, endpoint=False))),
#     ('moving_truck',  [0, 1])
# ])
