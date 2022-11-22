# begin with a randomly chosen generation 1st generation
# evaluate each chromosome to test how well it solves the problem
# select based on evaluate which chromosomes will reproduce
# cross over the chromosomes
# mutate with a very low probability

import numpy as np
from numba import jit
import math
global_minim = 1000
# generating the starting 
DEJON_INTERV = (-5.12,5.12)
RASTRING_INTERV = (-5.12,5.12)
MICHALEWICZ_INTERV = (0,math.pi)
SCHWEFEL_INTERV = (-500,500)
#a nu se pune populatie impara 
POPULATION_SIZE = 100
PRECISION = 5

N_DEJON = math.trunc(math.log2((DEJON_INTERV[1]- DEJON_INTERV[0])*pow(10,PRECISION))) #number of bits required
N_RAS = math.trunc(math.log2((RASTRING_INTERV[1]-RASTRING_INTERV[0])*pow(10,PRECISION)))
N_MICH = math.trunc(math.log2((MICHALEWICZ_INTERV[1]-MICHALEWICZ_INTERV[0])*pow(10,PRECISION)))
N_SCHWEL = math.trunc(math.log2((SCHWEFEL_INTERV[1]-SCHWEFEL_INTERV[0])*pow(10,PRECISION)))

MUTATION_RATE  = 0.1
NUMBER_OF_MUTATION = math.floor(MUTATION_RATE *POPULATION_SIZE)
CROSSOVER_RATE = 0.25


def De_Jong(params):
   return sum(val**2 for val in params)

def Rastrigin_Function(params):
    return 10*len(params) + sum(i**2 - 10*math.cos(2*math.pi*i) for i in params)

def Schwefel_Function(params):
    return sum((-i)*math.sin(math.sqrt(abs(i))) for i in params)

def Michalewicz_Function(params):
    return sum(math.sin(i)* math.pow(math.sin((j*i**2)/math.pi),2*len(params)) for j,i in enumerate(params))


#@jit(parallel = True)
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
    for  entry in population:
        print(entry)


@jit(parallel = True )
def cross_over( funct_params: int, bit_count: int,new_gen:list):
    

    # cross over after random  position
    
    new_pop = []    
    for i in range(0,POPULATION_SIZE,2):
        #creating pop_size/2 parents and mating them
        chrom1= new_gen[np.random.randint(1,POPULATION_SIZE)]
        chrom2 = new_gen[np.random.randint(1,POPULATION_SIZE)]

        #generate a random probabillity to cross over 
        
        if np.random.random() < CROSSOVER_RATE:
            position = np.random.randint(0, funct_params*bit_count)
            chrom1_cross = np.concatenate((chrom1[0:position],chrom2[position:chrom2.__len__()]))
            chrom2_cross = np.concatenate((chrom2[0:position],chrom1[position:chrom1.__len__()]))
            new_pop.append(chrom1_cross)
            new_pop.append(chrom2_cross)
            
        else:
            new_pop.append(chrom1)
            new_pop.append(chrom2)

    #print(f'position is {position}')
    # 10|110  11|1001

    return new_pop


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
@jit(parallel = True)
def decode(solution, a, b, no_of_bits)->float:
    return (a + binatodeci(solution)*(b-a)/(pow(2, no_of_bits)-1))



# @jit(fastmath = True)
def evaluate_fitness(population,no_of_params,no_of_bits,function_name):
     fitness_population :list = []
    
     #max = None # best chrom
     for chrom  in population:  
        params_decode = []
        #params decoded into real values 
        match function_name.__name__:
            case 'De_Jong':
                
                params_decode = (decode(x,DEJON_INTERV[0],DEJON_INTERV[1],N_DEJON) for x in  np.split(chrom,no_of_params*no_of_bits))
                fitness_population.append(1/function_name(params_decode))
                

            case 'Rastrigin_Function':
                params_decode = (decode(x,RASTRING_INTERV[0],RASTRING_INTERV[1],N_RAS) for x in  np.split(chrom,no_of_params))
                #TODO fill with fitness function
                

            case 'Schwefel_Function':
                params_decode = (decode(x,SCHWEFEL_INTERV[0],SCHWEFEL_INTERV[1],N_SCHWEL) for x in  np.split(chrom,no_of_params))

               

            case 'Michalewicz_Function':
                params_decode = (decode(x,MICHALEWICZ_INTERV[0],MICHALEWICZ_INTERV[1],N_MICH) for x in  np.split(chrom,no_of_params))
                
                

                
        #print(params_decode)
        #print(f'the function value is {function_name(params_decode)}')
        
     total = sum(x for x in fitness_population)
     #print(fitness_population.index(max(fitness_population)))
     params_decode = (decode(x,DEJON_INTERV[0],DEJON_INTERV[1],N_DEJON) for x in  np.split(population[fitness_population.index(max(fitness_population))],5))
     value = De_Jong(params_decode)
    #  if value < global_minim: 
    #      global_minim = value 
     print(f'best result is {value}',end= '\n')
     fitness_final = []
     fitness_cumulative = []
     for i in range(len(fitness_population)):
        fitness_final.append(fitness_population[i]/total)
        #print(f'fitness population[{i}] is {fitness_population[i]}')
        if i == 0 : 
                fitness_cumulative.append(fitness_final[i])
        else :
                fitness_cumulative.append(fitness_cumulative[i-1]+fitness_final[i]) 

     return (fitness_final,fitness_cumulative,value)


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
    start_population = generate_starting_pop(5,N_DEJON)
   
    for i in range(0,1000):
        #print(f'start pop is {start_population}')
        #print("start pop is :",end = '\n')
        #print_population(start_population)
        params_decode = (decode(x,DEJON_INTERV[0],DEJON_INTERV[1],N_DEJON) for x in  np.split(start_population[2],5))
        #print(f'first result is {De_Jong(params_decode)}',end= '\n')
        eval_fit = evaluate_fitness(start_population,5,N_DEJON,De_Jong)
        if  eval_fit[2] < global_minim:
            global_minim = eval_fit[2]
        #print(eval_fit[1])
        new_gen = select_chromosome(eval_fit[1],start_population)
        #print(f'the new gen is {new_gen}')
        # print('\n')
        # print_population(new_gen)
        new_pop = cross_over(5,N_DEJON,new_gen)
        print('\n')
       #print_population(new_pop)
        # params_decode = (decode(x,DEJON_INTERV[0],DEJON_INTERV[1],N_DEJON) for x in  np.split(new_pop[1],5))
        # print(f'best result is {De_Jong(params_decode)}',end= '\n')
        #mutate with a probability 
        mutate_gene(new_pop,5,N_DEJON)
        start_population = new_pop
    print(global_minim)
       
