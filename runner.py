# Daniel Li
# 03/30/2024
#
# pyOrbitSim::runner.py
#
# process data and save into csv

from conversions.eci2ecef import eci2ecef
from conversions.eci2geodetic import eci2geodetic
from fileIO.readISSephemeris import readISSephemeris
from plot.plotMercator import plotMercator
from plot.plotLatVLocalt import plotLatVLocalt
from concatData import concatData
from saveData import saveData


data1 = readISSephemeris("./ISS.OEM_J2K_EPH.2022-01-31.2022-02-15.txt")
data2 = readISSephemeris("./ISS.OEM_J2K_EPH.2022-02-14.2022-03-01.txt")

data1 = eci2geodetic(data1)
data2 = eci2geodetic(data2)

data = concatData(data1, data2)

#for row in data:
    #print(row[0])

saveData("ISSgeodeticData.csv", data)
