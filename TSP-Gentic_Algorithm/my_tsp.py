#TODO simulade annealing for TSP

import numpy as np

# parse the file and return a dict with the cities and their coordinates
def parse_file(file_name):
    locations = []
    cities_id = []
    with open("bays29.txt", 'r') as fp:
        # read all lines in a list
        lines = fp.readlines()
        for line, content in enumerate(lines):
            # check if string present on a current line
            if line > 7:
                x = content.split()  # split after each space

                cities_id.append(x[0])
                coords = " ".join(x[1:])

                location1 = coords.split(' ')
                location = (float(location1[0]), float(location1[1]))
                locations.append(location)

    # make a dict containing the cities and their coordinates
    cities = {x: y for x, y, in zip(cities_id, locations)}
    # print(cities)
    return cities

#distance berween two cities
def distance_two_points(city1, city2):
    xDis = abs(city1[0] - city2[0])
    yDis = abs(city1[1] - city2[1])
    distance = np.sqrt((xDis ** 2) + (yDis ** 2))
    return distance


def print_dict(dict):
    for key, value in dict.items():
        print(key, value)

#get distance of a path
def get_distance(route):
    d = 0.0  # total distance between cities
    n = len(route)
    for i in range(n-1):
        if route[i] < route[i+1]:
            d += (route[i+1] - route[i]) * 1.0
        else:
            d += (route[i] - route[i+1]) * 1.5
    return d

#error function for the distance
def error_function(cities_dict):
    return get_distance(cities_dict) - (len(cities_dict) -1)

#function that accepts a path and comoutes the new path
def new_path(cities_dict):
    #make a copy of the path
    new_cities_dict = cities_dict.copy()
    #choose two random cities
    i = np.random.randint(0, len(cities_dict))
    j = np.random.randint(0, len(cities_dict))
    #swap the cities
    new_cities_dict[i], new_cities_dict[j] = new_cities_dict[j], new_cities_dict[i]
    return new_cities_dict

#simulated annealing
def simulated_annealing(cities_dict, temperature, alpha, max_iterations):
    #make a random path
    soln = np.arange(len(cities_dict))
    #shuffle the path
    np.random.shuffle(soln)
    #displat the initial solution
    print("Initial solution: ", soln)
    #compute the error
    err = error_function(soln)
    #keep track of the number of iterations
    iteration = 0
    #loop until the temperature is low or the max number of iterations is reached
    while temperature > 0.01 and iteration < max_iterations:
        #get a new solution
        new_soln = new_path(soln)
        #compute the error
        new_err = error_function(new_soln)
        #check if the new solution is better
        if new_err < err: #`new solution is better, accept it
            soln = new_soln
            err = new_err
        else: #new solution is worse, accept it with a probability
            if np.random.random() < np.exp(-abs(new_err - err) / temperature):
                soln = new_soln
                err = new_err
            #else reject it
        #decrease the temperature
        temperature *= alpha
        iteration += 1
        print("Iteration: ", iteration, " Error: ", err, " Temperature: ", temperature)
    #display the final solution
    print("Final solution: ", soln)

#main function
def main():
    #get the cities and their coordinates
    cities_dict = parse_file("bays29.txt")
    #set the initial temperature
    temperature = 100
    #set the cooling rate
    alpha = 0.95
    #set the max number of iterations
    max_iterations = 10
    #run the simulated annealing algorithm
    simulated_annealing(cities_dict, temperature, alpha, max_iterations)

main()