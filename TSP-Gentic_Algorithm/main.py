# genetic algorithm that solves the Travel Salesman

import numpy as np


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


def print_dict(dict):
    for key, value in dict.items():
        print(key, value)

# distance betweeen two cities


def distance_two_points(city1, city2):
    xDis = abs(city1[0] - city2[0])
    yDis = abs(city1[1] - city2[1])
    distance = np.sqrt((xDis ** 2) + (yDis ** 2))
    return distance


# parse the file and return a dict with the cities and their coordinates
cities_dict = parse_file("bays29.txt")
# print_dict(cities_dict)

#print(distance_two_points(cities_dict['3'], cities_dict['3']))

# generate the initial population


def generate_initial_population(cities_dict, population_size):
    # generate a list of all the cities
    cities_list = []
    for key in cities_dict:
        cities_list.append(key)
    # print(cities_list)

    # generate the population
    population = []
    for i in range(population_size):
        # generate a random permutation of the cities
        random_permutation = np.random.permutation(cities_list)
        population.append(random_permutation)
        #print(f'Current population: {random_permutation} with size {np.size(random_permutation)}  ',end='\n')
    return population


init_pop = generate_initial_population(cities_dict, 4)
# print(init_pop)

# calculate the fitness of a given individual


def fitness_individual(individual, cities_dict):

    # calculate the distance between the first and the last city
    distance = distance_two_points(
        cities_dict[individual[0]], cities_dict[individual[-1]])

    # calculate the distance between the rest of the cities
    for i in range(len(individual)-1):
        distance += distance_two_points(
            cities_dict[individual[i]], cities_dict[individual[i+1]])
    return 1/distance

#print(fitness_individual(init_pop[0], cities_dict))

# fitness of the population


def fitness_population(population, cities_dict):
    fitness = np.zeros(len(population))
    for i in range(len(population)):
        fitness[i] = fitness_individual(population[i], cities_dict)
    return fitness

# select the best individuals


def selection(population, fitness_list):

    total_fit = np.sum(fitness_list)
    # print(total_fit)
    probabs_list = []
    for i in range(len(population)):
        probabs_list.append(fitness_population(
            population, cities_dict)[i]/total_fit)
    # print(probabs_list)
    # select using roulette wheel
    #print(population)
    new_pop_indx1 = []
    new_pop_indx2 = []
    for i in range(len(population)):
        new_pop_indx2.append(np.random.choice(len(population), replace=True, p=probabs_list))    
        new_pop_indx1.append(np.random.choice(len(population), replace=True, p=probabs_list))
    #print(new_pop_indx1)
    #print(new_pop_indx2)
    #transform the indexes into the actual individuals
    parent1 =[]
    parent2 =[]
    for i in range(len(new_pop_indx1)):

        parent1.append(population[new_pop_indx1[i]])
        parent2.append(population[new_pop_indx2[i]] )  
    
    return (parent1, parent2)
    


#cross over the parents
def cross_over(parent1, parent2):
    #select a random point to cross over
    cross_point = np.random.randint(0,len(parent1[1]))
    #parent1 is a population  
    print(f'cross_point is {cross_point}')
    #print(f'parent1: {parent1[1]}')
    #create the children
    new_pop = []
    for i in range(len(parent1)):
    #copy one part from parent 1 and the other from parent 2
        offspring = parent1[i][0:cross_point]
        #print(f'offspring: {offspring}')
        for city in parent2[i]:
            #print(city)
            if city not in offspring:
               np.append(offspring,city)
        #print(offspring)
        new_pop.append(offspring)
    return new_pop


#mutate the population
def mutate(population, mutation_rate):
    for i in range(len(population)):
        if np.random.random() < mutation_rate:
            #select two random cities
            city1 = np.random.randint(0,len(population[i]))
            city2 = np.random.randint(0,len(population[i]))
            #swap the cities
            population[i][city1], population[i][city2] = population[i][city2], population[i][city1]
    return population


#implement elitism to keep the best individual
# def elitism(population, fitness_list, elitism_rate):
#     #get the best individual
#     best_individual = population[np.argmax(fitness_list)]
#     #print(f'Best individual: {best_individual}')
#     #get the number of individuals to keep
#     n_keep = int(elitism_rate*len(population))
#     #print(f'Number of individuals to keep: {n_keep}')
#     #get the indexes of the best individuals
#     best_individual_indx = np.argpartition(fitness_list, -n_keep)[-n_keep:]
#     #print(f'Indexes of the best individuals: {best_individual_indx}')
#     #keep the best individuals
#     new_population = []
#     for i in range(len(best_individual_indx)):
#         new_population.append(population[best_individual_indx[i]])
#     #print(f'New population: {new_population}')
#     #add the best individual
#     new_population.append(best_individual)
#     #print(f'New population: {new_population}')
#     return new_population

#print(fitness_population(init_pop, cities_dict))
fitness_pop = fitness_population(init_pop, cities_dict)
parents = selection(init_pop, fitness_pop)
#print(parents)
#print(cross_over = cross_over(parents[0][0], parents[1][0]))
new_pop = cross_over(parents[0], parents[1])
print(new_pop)

