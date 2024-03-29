# Daniel Li
# 03/29/2024
#
# pyOrbitSim::fileio::readISSephemeris.py
#
# extract [time (UTC), position (X,Y,Z) (km/s), velocity (X,Y,Z) (km/s)] from the ISS.OEM_J2K_EPH.txt file
# and put the data into a matrix

from pathlib import Path
from sys import exit
from datetime import datetime


def readISSephemeris(filename : str):
    # verify file exists
    filepath = Path(filename)
    if not filepath.is_file():
        exit("error: file does not exist")

    # read in file data
    data = []
    with open(filename) as ephemeris:
        data = ephemeris.readlines()

    # remove metadata and comments
    while len(data[0]) == 1 or data[0][0].isalpha():
        data.pop(0)

    # parse file data
    parseddata = []
    for line in data:
        parsedline = []

        line = line.split(" ")

        col1Split = line[0].split("T")
        dateSplit = col1Split[0].split("-")
        timeSplit = col1Split[1].split(":")
        parsedline.append(datetime(
            int(dateSplit[0]),
            int(dateSplit[1]),
            int(dateSplit[2]),
            hour=int(timeSplit[0]),
            minute=int(timeSplit[1]),
            second=int(float(timeSplit[2]))
        ))

        parsedline.append([float(line[1]), float(line[2]), float(line[3])])
        parsedline.append([float(line[4]), float(line[5]), float(line[6])])

        parseddata.append(parsedline)

    return parseddata
