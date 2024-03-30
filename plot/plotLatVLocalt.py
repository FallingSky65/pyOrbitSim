# Daniel Li
# 03/29/2024
#
# pyOrbitSim::plot::plotLatVLocalt.py
#
# plot latitude against the local time

import matplotlib.pyplot as plt
from datetime import timedelta
from math import pi

def localT(longitude, utctime):
    localt = (utctime + timedelta(hours=longitude/15))
    return localt.hour + localt.minute/60

def plotLatVLocalt(data):
    lon = [timestep[1][1].item() for timestep in data]
    lat = [timestep[1][0].item() for timestep in data]
    utct = [timestep[0] for timestep in data]
    localt = [localT(lon[i],utct[i]) for i in range(len(data))]

    #print(min(lon),max(lon))

    plt.plot(localt, lat, color="red")

    plt.show()
