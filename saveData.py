# Daniel Li
# 03/29/2024
#
# pyOrbitSim::saveData.py
#
# plot latitude against the local time

import csv

def saveData(filename, data):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow([row[0], row[1][0].item(), row[1][1].item(), row[1][2].item()])
