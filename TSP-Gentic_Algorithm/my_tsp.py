import numpy as np
import pandas as pd

locations  =[]
with open("bays29.txt", 'r') as fp:
    # read all lines in a list
    lines = fp.readlines()
    for line, content in enumerate(lines):
        # check if string present on a current line
        if line>7:
            x = content.split()
            final = " ".join(x[1:])
            location1 = final.split(' ')
            location = (float(location1[0]), float(location1[1]))
            locations.append(location)

size = len(locations)

# distances = [] #deasupra diagonalei principale
# for i in range(0, size):
#     for j in range(i+1, size):
#             distance = np.sqrt((abs(locations[j][0]-locations[i][0]) ** 2) + (abs(locations[j][1]-locations[i][1]) ** 2))
#             distances.append(distance)
# print(distances)

class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def distance(self, city):
        xDis = abs(self.x - city.x)
        yDis = abs(self.y - city.y)
        distance = np.sqrt((xDis ** 2) + (yDis ** 2))
        return distance
    
    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

cityList = []

for city in locations:
    cityList.append(City(city[0], city[1]))

for i in range(0, size):
    print(cityList[0].distance(cityList[i]))
