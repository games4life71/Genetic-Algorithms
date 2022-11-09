# begin with a randomly chosen generation 1st generation
# evaluate each chromosome to test how well it solves the problem
# select based on evaluate which chromosomes will reproduce
# cross over the chromosomes
# mutate with a very low probability

import numpy as np
from numba import jit

# generating the starting population
POPULATION_SIZE = 10

@jit(parallel = True)
def generate_chromosome(func_params, bit_count):
    # using unsigned ints to optimize memory
    chromosome = np.random.randint(0, 2, func_params*bit_count, np.uint8)
    return chromosome


@jit(parallel=True)
def generate_starting_pop(func_params, bit_count):
    population = []
    for i in range(0, POPULATION_SIZE):
        population.append(generate_chromosome(func_params, bit_count))
    return population

# @jit(parallel = True)


def print_population(population):
    for line, entry in enumerate(population):
        print(entry, end='\n')


def cross_over(chrom1: list, chrom2: list, funct_params: int, bit_count: int):
    position = np.random.randint(0, funct_params*bit_count)
    # cross over after random  position
    print(f'position is {position}')
    # 10|110  11|1001
    chrom1_cross = chrom1[0:position]+chrom2[position:chrom2.__len__()]
    chrom2_cross = chrom2[0:position]+chrom1[position:chrom1.__len__()]
    return (chrom1_cross, chrom2_cross)


def mutate_gene(chromo, funct_params, bit_count):
    position = np.random.randint(0, funct_params*bit_count)
    if chromo[position] == 1:
        chromo[position] = 0
    else:
        chromo[position] = 1

    return chromo
if __name__ == "__main__":
    start_population = generate_starting_pop(2, 2)
    print_population(start_population)

    # print(cross_over(start_population[0].tolist(),
    #       start_population[1].tolist(), 2, 2))
    print(mutate_gene(start_population[0].tolist(),2,2))