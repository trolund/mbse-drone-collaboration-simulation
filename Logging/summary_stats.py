

def readLog():
    infile = r"C:\Users\odaby\Desktop\MBSE_Project\MBSE-Drone-Collaboration\Logging\Files\logfile_2022_11_03-10_53.log"

    positions = []
    keep = ["move to"]

    with open(infile) as f:
        f = f.readlines()

    for line in f:
        for phrase in keep:
            if phrase in line:
                positions.append(line)
                break

    print(positions)

if __name__ == "__main__":
    # setup dependency injection
     readLog()