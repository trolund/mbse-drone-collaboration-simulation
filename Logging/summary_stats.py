import csv
import datetime
import math
import os
from statistics import mean 
import numpy as np

def format_number(msg,decimals):
    string_decimals = '{0:.'+str(decimals)+'f}'
    return f"{string_decimals.format(msg)}"


def readLog(infile):

    positions = []
    keep = ["move to"]

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
                dist_format = float(format_number(dist,2))
        distances.append(dist_format)
        dist = 0
    return distances

def get_time(filename):
    filepos = "./Logging/Files/"+filename

    with open(filepos) as f:
        f = f.readlines()  
    
    temp = f[-1].split(':')
    return float(temp[-1])

def get_speed(time, distance):
    return distance / time

def time_per_drone(distances,speed):
    times = []
    for d in distances:
        times.append(format_number(float(d)/speed,2))
    return times

def time_per_package(filename,time):
    packages_left = number_of_packages(filename)
    return format_number(time/float(packages_left),2)
            
def number_of_packages(filename):
    filepos = "./Logging/Files/"+filename
    queue_size = []
    with open(filepos) as f:
        f = f.readlines() 

    for line in f:
        temp = line.split(';')
        if "Packages" in temp[1]:
            number = temp[1].split(':')[1].strip()
            queue_size.append(number)
    packages_left = len(queue_size)
    return packages_left

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

def avg_package_per_drone(packages,drones):
    return(format_number(packages/drones,2))

def write_to_file(filename, msg):
    with open(filename, "a") as file:
        for m in msg:
            line = f"{m}\n"
            file.write(line)

def write_to_csv(data, filename):
    file_path = "Logging\Files\\" + filename + ".csv"

    with open(file_path, 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def get_battery_info(filename):
    filepos = "./Logging/Files/"+filename
    battery_info = ""
    energy = ""
    with open(filepos) as f:
        f = f.readlines()
    for line in f:

        parts = line.split(";")
        #print(parts[1])
        info = parts[1].split(" ")
        #print(info)
        try:
            if info[2] == "power[W]:":
                battery_info += str(info[3])+","
            if info[2] == "consumption[J]:":
                energy += str(info[3])+","
        except IndexError:
            continue
        new_b = battery_info.replace("\n","")
        new_e = energy.replace("\n","")
    return new_e[:-1:], new_b[:-1:]

def customer_density(filename):
    filepos = "./Logging/Files/"+filename
    with open(filepos) as f:
        f = f.readlines()
    for line in f:
        #print(line)
        parts = line.split(";")
        #print(parts[1])
        info = parts[1].split(" ")
        #print(info)
        #print(info)
        try:
            if info[0] == "Costumer":
                density = parts[1].split(":")
                return density[1].replace("\n","")

        except IndexError:
            continue

def make_summary_file(file):
    list = readLog(file)
    dist = distances(list,get_drones(file))
    no_packages = number_of_packages(file)
    number_of_drones = get_drones(file)
    time = get_time(file)
    speed = get_speed(time, float(max(dist)))
    power, energy = get_battery_info(file)
    #date = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    no_drones = number_of_drones
    no_package = no_packages
    time_tot = format_number(time,2)
    avg_speed = format_number(speed,2)
    #msg4 = dist
    dist_tot = sum(dist)
    #msg5 = time_per_drone(dist,speed)
    avg_time_package = time_per_package(file,time)
    avg_package_drones = avg_package_per_drone(no_packages,number_of_drones)
    avg_dist = format_number(Average(dist),2)
    energy_cons = energy
    power_cons = power
    costumer_density = customer_density(file)
    messages = [no_drones,no_package,time_tot,avg_speed,dist_tot,avg_time_package,avg_package_drones,avg_dist, energy_cons, power_cons, costumer_density]
    return messages
    #write_to_csv(headers,messages,file.split(".")[0])

def Average(lst):
    return sum(lst) / len(lst)

def main():
    files = get_files("20211110","20231111")
    headers = ["No_drones","No_packages","Total_time","Avg_speed","Dist_tot","Avg_time_package","Avg_packages_drone","Avg_dist_traveled", "Energy_consumption","Avg_power","Costmer_density"]
    # removed the arrays dist_drone and working_time_drones

    date = datetime.datetime.now().strftime("%Y_%m_%d")
    Filename = "Summary_"+date
    write_to_csv(headers, Filename)

    for file in files:
        summary = make_summary_file(file)
        write_to_csv(summary,Filename)   
        print(summary)

if __name__ == "__main__":
   main()
