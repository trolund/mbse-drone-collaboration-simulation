import subprocess

import configparser

if __name__ == "__main__":
    for x in range(1):
        process = subprocess.Popen(['python3', 'simulation.py'],
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