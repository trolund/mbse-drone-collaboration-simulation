import os

def readLog(infile):
    #infile = r"C:\Users\odaby\Desktop\MBSE_Project\MBSE-Drone-Collaboration\Logging\Files\logfile_2022_11_03-10_53.log"

    positions = []
    keep = ["move to"]
    print(infile)
    filepos = "./Logging/Files/"+infile
    with open(filepos) as f:
        f = f.readlines()

    for line in f:
        line.replace("\n", "")
        parts = line.split(";")
        if parts[0] != "\n":
            stats = parts[1].split(" ")
            if stats[0]:
                print(stats[0])
        

        for phrase in keep:
            if phrase in line:
                positions.append(line)
                break

    print(positions)

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
    files = get_files("20221104","20221105")

    for file in files:
        print("NEWFILE")
        readLog(file)
        print(f'no_Drones {get_drones(file)}')


if __name__ == "__main__":
    # setup dependency injection
    main()
