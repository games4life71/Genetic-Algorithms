# begin with a randomly chosen generation 1st generation
# evaluate each chromosome to test how well it solves the problem
# select based on evaluate which chromosomes will reproduce
# cross over the chromosomes
# mutate with a very low probability

import numpy as np
from numba import jit
import math

# generating the starting 
DEJON_INTERV = (-5.12,5.12)
POPULATION_SIZE = 5
PRECISION = 5
N_DEJON = math.trunc(math.log2((DEJON_INTERV[1]- DEJON_INTERV[0])*pow(10,PRECISION))) #number of bits required
MUTATION_RATE  = 0.9
NUMBER_OF_MUTATION = math.floor(MUTATION_RATE *POPULATION_SIZE)

def De_Jong(params):
   return sum(val**2 for val in params)

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

#mutate with a proability 
@jit(parallel = True)
def mutate_gene(population,funct_params, bit_count):
    for i in range (0,NUMBER_OF_MUTATION):
        #generate a number between 1 and number of total genes 
        val = np.random.randint(1,funct_params*bit_count*POPULATION_SIZE)
        #print(f'number is {val}')
        #change the bit from correct chromosome 
        chromos_indx = val%(funct_params*bit_count)
        chrom_indx  = math.floor(val/(funct_params*bit_count))
        gene = population[chrom_indx]
        #print(f'gene is{gene}')
        if gene[chromos_indx] == 0 :
            gene[chromos_indx] =1
        else : gene[chromos_indx] = 0


def binatodeci(bitstring)->int: 
    return sum(val*(2**idx) for idx, val in enumerate(reversed(bitstring)))


#Decode it so it fits into function interval 
#@jit(parallel = True)
def decode(solution, a, b, no_of_bits)->float:
    return (a + binatodeci(solution)*(b-a)/(pow(2, no_of_bits)-1))



def evaluate_fitness(population,no_of_params,function_name):
     fitness_population :list = []
     #max = None # best chrom
     for chrom  in population:  
        #params decoded into real values 
        params_decode = (decode(x,DEJON_INTERV[0],DEJON_INTERV[1],N_DEJON) for x in  np.split(chrom,no_of_params))        
        #print(params_decode)
        #print(f'the function value is {function_name(params_decode)}')
        fitness_population.append(1/function_name(params_decode))
     total = sum(x for x in fitness_population)
     #print(max(fitness_population))
     fitness_final = []
     fitness_cumulative = []
     for i in range(len(fitness_population)):
        fitness_final.append(fitness_population[i]/total)
        if i == 0 : 
            fitness_cumulative.append(fitness_final[i])
        else :
            fitness_cumulative.append(fitness_cumulative[i-1]+fitness_final[i]) 

     return (fitness_final,fitness_cumulative)


def print_fitness(fitness_pop):
    for entry in fitness_pop:
        print(entry)


#select using roulette-wheel
def select_chromosome(pop_cumul:list,population):
    probab = np.random.random(POPULATION_SIZE)
    new_gen = []
    for i in range(len(probab)):
        for j in range(len(pop_cumul)): 
            if probab[i]<pop_cumul[j]:
                new_gen.append(population[j])
                break
    return new_gen
    

    
if __name__ == "__main__":
    start_population = generate_starting_pop(2,N_DEJON)
    print_population(f'start pop is {start_population}')
    eval_fit = evaluate_fitness(start_population,2,De_Jong)
    new_gen = select_chromosome(eval_fit[1],start_population)
    print_population(new_gen)
    # print(mutate_gene(start_population,3,3))
    # print_population(start_population)

    # print(cross_over(start_population[0].tolist(),
    #       start_population[1].tolist(), 2, 2))
    #print(mutate_gene(start_population[0].tolist(),2,2))
    # fitness_info= De_Jong_Fitness(start_population,2)
    # new_gen =select_chromosome(fitness_info[1],start_population)
    # print_population(new_gen)
    # print_fitness(fitness_info[1])
    # print_fitness(fitness_info[0])
    #print(f'total is {fitness_info[0]}')

    pass