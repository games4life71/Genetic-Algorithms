#genetic algorithm that solves the Travel Salesman 

import numpy as np




def parse_file(file_name):
    locations  =[]
    cities_id  =[]
    with open("bays29.txt", 'r') as fp:
        # read all lines in a list
        lines = fp.readlines()
        for line, content in enumerate(lines):
            # check if string present on a current line
            if line>7:
                x = content.split() # split after each space

                
                cities_id.append(x[0])
                coords = " ".join(x[1:])
                

                location1 = coords.split(' ')
                location = (float(location1[0]), float(location1[1]))
                locations.append(location)

    #make a dict containing the cities and their coordinates
    cities = { x:y for x,y, in zip(cities_id, locations)}
    #print(cities)
    return cities

def print_dict (dict):
    for key, value in dict.items():
        print(key, value)

#distance betweeen two cities
def distance_two_points (city1, city2):
    xDis = abs(city1[0] - city2[0])
    yDis = abs(city1[1] - city2[1])
    distance = np.sqrt((xDis ** 2) + (yDis ** 2))
    return distance





distances = []

cities_dict = parse_file("bays29.txt") #parse the file and return a dict with the cities and their coordinates
print_dict(cities_dict)





# for i in range(0, size):
#     for j in range(i+1, size):
#             distance = np.sqrt((abs(locations[j][0]-locations[i][0]) ** 2) + (abs(locations[j][1]-locations[i][1]) ** 2))
#             distances.append(distance)
#print(distances)








