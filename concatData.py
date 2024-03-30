# Daniel Li
# 03/30/2024
#
# pyOrbitSim::concatData.py
#
# concatenate data sorted by time

def concatData(data1, data2):
    data = []
    i = 0
    j = 0
    while i < len(data1) and j < len(data2):
        if data1[i][0] < data2[j][0]:
            data.append(data1[i])
            i += 1
        elif data1[i][0] > data2[j][0]:
            data.append(data2[j])
            j += 1
        else:
            data.append([data1[i][0], [
                (data1[i][1][0] + data2[j][1][0])/2,
                (data1[i][1][1] + data2[j][1][1])/2,
                (data1[i][1][2] + data2[j][1][2])/2,
            ]])
            i += 1
            j += 1

    while i < len(data1):
        data.append(data1[i])
        i += 1

    while j < len(data2):
        data.append(data2[j])
        j += 1

    return data
