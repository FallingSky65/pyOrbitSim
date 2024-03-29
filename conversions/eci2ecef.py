# Daniel Li
# 03/29/2024
#
# pyOrbitSim::conversions::eci2ecef.py
#
# convert the positions in the matrix from the ephemeris to ecef from eci

from pymap3d.eci import eci2ecef as pm_eci2ecef
from datetime import datetime

def eci2ecef(ecidata):
    times : list[datetime] = [timestep[0] for timestep in ecidata]
    ecipositions = [timestep[1] for timestep in ecidata]
    ecefpositions = [
        list(
            pm_eci2ecef(
                ecipositions[i][0],
                ecipositions[i][1],
                ecipositions[i][2],
                times[i]
            )) for i in range(len(ecipositions))]
    ecefdata = [[times[i], ecefpositions[i]] for i in range(len(ecefpositions))]
    return ecefdata
