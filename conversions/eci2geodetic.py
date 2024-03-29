# Daniel Li
# 03/29/2024
#
# pyOrbitSim::conversions::eci2geodetic.py
#
# convert the positions in the matrix from the ephemeris to geodetic from eci

from pymap3d.ecef import eci2geodetic as pm_eci2geodetic
from datetime import datetime

def eci2geodetic(ecidata):
    times : list[datetime] = [timestep[0] for timestep in ecidata]
    ecipositions = [timestep[1] for timestep in ecidata]
    gdcoords = [
        list(
            pm_eci2geodetic(
                ecipositions[i][0],
                ecipositions[i][1],
                ecipositions[i][2],
                times[i]
            )) for i in range(len(ecipositions))]
    ecefdata = [[times[i], gdcoords[i]] for i in range(len(gdcoords))]
    return ecefdata
