import datetime
import math
import os

def readLog(infile):

    positions = []
    keep = ["move to"]
    print(infile)
    filepos = "./Logging/Files/"+infile
    drones = get_drones(infile)
    temp = []
    with open(filepos) as f:
        f = f.readlines()

    for i in range(0,drones):
        for line in f:
            line.replace("\n", "")
            parts = line.split(";")
            stats = parts[1].split(" ")
            for stat in stats:
                if stat == (f"drone_{str(i)},"):
                    coordinates = parts[1].split(" ")
                    dict = {
                        "drone": (f"drone_{str(i)},"),
                        "FromX" : coordinates[3].replace("(","").replace(",",""),
                        "FromY" : coordinates[4].replace(")",""),
                        "ToX" : coordinates[6].replace("(","").replace(",",""),
                        "ToY" : coordinates[7].replace(")","").replace("\n","")
                    }
                   # endstring = (f"From {},{cordinates[4]} To {cordinates[6]},{cordinates[7]}")
                    temp.append(dict)
    return temp

def distances(coordinate_list,no_drones):

    distances = []
    for drone in range(0,no_drones):
        dist = 0
        for i in coordinate_list:
            #print(i['drone'])

            if i['drone'] == 'drone_'+str(drone)+',':
                dist = dist + math.hypot(float(i['FromX'])-float(i['ToX']), float(i['FromY'])-float(i['ToY']))
        
        distances.append(dist)
        dist = 0
    return distances
                        
def get_files(from_date, to_date):
    files = os.listdir('./Logging/Files')
    files_temp = []
    for file in files:
        line = file.split("_")
        file_name = line[0]
        if file_name == "logfile":
            year = line[1]
            month = line[2]
            day = line[3]
            date = year + month + day
            #TODO SOMETHING FROM PUT PLUS ONE ON TODATE
            if from_date <= date <= to_date:
                files_temp.append(file)
    return (files_temp)

def get_drones(filename):
    no_drones = 0
    filepos = "./Logging/Files/"+filename

    with open(filepos) as f:
        f = f.readlines()
    
    for line in f:
        parts = line.split(";")
        init = parts[1].split(" ")
        if init[1] == "TPS:":
            break
        if init[1] == "initialized\n":
            no_drones = no_drones + 1
        
    
    return no_drones


def main():
    files = get_files("20221104","20221111")
    for file in files:
        print("NEWFILE")
        list = readLog(file)
        dist = distances(list,get_drones(file))

        print(f'Distances travelled by drones: {dist}')

if __name__ == "__main__":
    # setup dependency injection
    main()