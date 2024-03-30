# Daniel Li
# 03/29/2024
#
# pyOrbitSim::plot::plotMercator.py
#
# plot points (lon, lat) onto map

import cartopy.crs as ccrs
import matplotlib.pyplot as plt

def plotMercator(data):
    lon = [timestep[1][1] for timestep in data]
    lat = [timestep[1][0] for timestep in data]

    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.stock_img()
    ax.coastlines()

    plt.plot(lon[:100], lat[:100], color="red")

    plt.show()
