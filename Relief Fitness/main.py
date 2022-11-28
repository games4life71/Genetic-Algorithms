# begin with a randomly chosen generation 1st generation
# evaluate each chromosome to test how well it solves the problem
# select based on evaluate which chromosomes will reproduce
# cross over the chromosomes
# mutate with a very low probability
import cProfile
import pstats


import numpy as np
from numba import njit


import math
global_minim = 1000
# generating the starting 
DEJON_INTERV = (-5.12,5.12)
RASTRING_INTERV = (-5.12,5.12)
MICHALEWICZ_INTERV = (0,math.pi)
SCHWEFEL_INTERV = (-500,500)
#a nu se pune populatie impara 
PRECISION = 5
N_DEJON = math.trunc(math.log2((DEJON_INTERV[1]- DEJON_INTERV[0])*pow(10,PRECISION))) #number of bits required
N_RAS = math.trunc(math.log2((RASTRING_INTERV[1]-RASTRING_INTERV[0])*pow(10,PRECISION)))
N_MICH = math.trunc(math.log2((MICHALEWICZ_INTERV[1]-MICHALEWICZ_INTERV[0])*pow(10,PRECISION)))
N_SCHWEL = math.trunc(math.log2((SCHWEFEL_INTERV[1]-SCHWEFEL_INTERV[0])*pow(10,PRECISION)))
MUTATION_RATE  = 0.7
CROSSOVER_RATE = 0.2
POPULATION_SIZE = 100
NO_GENERATIONS = 2000
NUMBER_OF_MUTATION = math.floor(MUTATION_RATE *POPULATION_SIZE)
ELITISM_RATE = 15
ELITE_POP_SIZE = math.floor((ELITISM_RATE/100)*POPULATION_SIZE)

def fitnessSchwefel(arr):
    suma  = sum(x  for x in arr) 
    return pow(suma+10000,-1)

def fitnessMichalewicz(arr):
    suma = sum(x for x in arr)
    return (1/suma**2)

def De_Jong(params):
   return sum(val**2 for val in params)

def Rastrigin_Function(params):
    return 10*len(params)+ sum(i**2 - 10*math.cos(2*math.pi*i) for i in params)

def Schwefel_Function(params):
    return sum((-i)*math.sin(math.sqrt(abs(i))) for i in params)

def Michalewicz_Function(params):
    return -sum(math.sin(val)* math.pow(math.sin((line*(val**2))/math.pi),2*10) for line,val in enumerate(params))


#@jit(parallel = True)
def generate_chromosome(func_params, bit_count):
    # using unsigned ints to optimize memory
    chromosome = np.random.randint(0, 2, func_params*bit_count, np.uint8)
    return chromosome



def generate_starting_pop(func_params, bit_count):
    population = []
    for i in range(0, POPULATION_SIZE):
        population.append(generate_chromosome(func_params, bit_count))
    return population

# @jit(parallel = True)


def print_population(population):
    for  entry in population:
        print(entry)


#@jit(parallel = True )
def cross_over( funct_params: int, bit_count: int,new_gen:list,elite_pop):
    

    # cross over after random  position
    
    new_pop = []    
    for i in range(0,POPULATION_SIZE - ELITE_POP_SIZE,2):
        #creating pop_size/2 parents and mating them
        chrom1= new_gen[np.random.randint(1,POPULATION_SIZE-ELITE_POP_SIZE)]
        chrom2 = new_gen[np.random.randint(1,POPULATION_SIZE-ELITE_POP_SIZE)]

        #generate a random probabillity to cross over 
        
        if np.random.random() < CROSSOVER_RATE :

            position = np.random.randint(0, funct_params)
            chrom1_cross = np.concatenate((chrom1[0:position*bit_count],chrom2[position*bit_count:chrom2.__len__()]))
            chrom2_cross = np.concatenate((chrom2[0:position*bit_count],chrom1[position*bit_count:chrom1.__len__()]))
            new_pop.append(chrom1_cross)
            new_pop.append(chrom2_cross)
            
        else:
            new_pop.append(chrom1)
            new_pop.append(chrom2)

   

    #copy the elite individuals 
    new_pop.extend(elite_pop)
    return new_pop


#mutate with a proability 

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
            gene[chromos_indx] = 1
        else : gene[chromos_indx] = 0


def binatodeci(bitstring)->int: 
    return sum(val*(2**idx) for idx, val in enumerate(reversed(bitstring)))


#Decode it so it fits into function interval 

def decode(solution, a, b, no_of_bits)->float:
    return (a + binatodeci(solution)*(b-a)/(pow(2, no_of_bits)-1))



def evaluate_fitness(population:list ,no_of_params,no_of_bits,function_name):
     fitness_population :list = []
     
     #max = None # best chrom

     for chrom in population:  
        params_decode = []
        #params decoded into real values 
        match function_name.__name__:
            case 'De_Jong':
                
                params_decode = (decode(x,DEJON_INTERV[0],DEJON_INTERV[1],3) for x in  np.split(chrom,no_of_params*no_of_bits))
                fitness_population.append(1/function_name(list(params_decode)))
                   

            case 'Rastrigin_Function':
                params_decode = (decode(x,RASTRING_INTERV[0],RASTRING_INTERV[1],N_RAS) for x in  np.split(chrom,no_of_params))
                fitness_population.append(1/function_name(list(params_decode)))
                
                

            case 'Schwefel_Function':
                params_decode = (decode(x,SCHWEFEL_INTERV[0],SCHWEFEL_INTERV[1],N_SCHWEL) for x in  np.split(chrom,no_of_params))
                fitness_population.append(1/function_name(list(params_decode)))    
               

            case 'Michalewicz_Function':
                params_decode = (decode(x,MICHALEWICZ_INTERV[0],MICHALEWICZ_INTERV[1],N_MICH) for x in  np.split(chrom,no_of_params))
                fitness_population.append(1/function_name(list(params_decode)))

                

                
        #print(params_decode)
        #print(f'the function value is {function_name(params_decode)}')
        
     total = sum(x for x in fitness_population)
     #print(fitness_population.index(max(fitness_population)))
     match function_name.__name__:
            case 'De_Jong':
                params_decode = (decode(x,DEJON_INTERV[0],DEJON_INTERV[1],N_DEJON) for x in  np.split(population[fitness_population.index(max(fitness_population))],no_of_params))    
            case 'Rastrigin_Function':
                params_decode = (decode(x,RASTRING_INTERV[0],RASTRING_INTERV[1],N_RAS) for x in  np.split(population[fitness_population.index(max(fitness_population))],no_of_params))
            case 'Schwefel_Function':
                params_decode = (decode(x,SCHWEFEL_INTERV[0],SCHWEFEL_INTERV[1],N_SCHWEL) for x in  np.split(population[fitness_population.index(max(fitness_population))],no_of_params))    
            case 'Michalewicz_Function':
                params_decode = (decode(x,MICHALEWICZ_INTERV[0],MICHALEWICZ_INTERV[1],N_MICH) for x in  np.split(population[fitness_population.index(max(fitness_population))],no_of_params))
                
     value = function_name(list(params_decode))
     global_minim = 1000
     if value < global_minim: 
       global_minim = value 
       print(f'best result is {value}',end= '\n')
     
     fitness_final = [] #probability for each chrom to be selected 


    #figure out which chormosome are fit to elitism
     sorted_fitness = sorted(fitness_population,reverse=True)
     elite_pop = []
     for i  in range  (0,ELITE_POP_SIZE):
        #indx = population.index(sorted_fitness)
        elite_pop.append(population[fitness_population.index(sorted_fitness[i])])
     

     fitness_cumulative = [] #cumulative probability for roulette wheel 

     for i in range(len(fitness_population)):
        fitness_final.append(fitness_population[i]/total)
        #print(f'fitness population[{i}] is {fitness_population[i]}')
        if i == 0 : 
                fitness_cumulative.append(fitness_final[i])
        else :
                fitness_cumulative.append(fitness_cumulative[i-1]+fitness_final[i-1]) 

     return (fitness_final,fitness_cumulative,value,elite_pop)


def print_fitness(fitness_pop):
    for entry in fitness_pop:
        print(entry)


#select using roulette-wheel
def select_chromosome(pop_cumul:list,population:list,elite_pop:list):
    probab = np.random.random(POPULATION_SIZE-ELITE_POP_SIZE)
    pop_cumul[POPULATION_SIZE-1-ELITE_POP_SIZE] = 1
    #print(f'len of cumul is {len(pop_cumul)} and len of probab is {len(probab)}')
    #print(f'len cumul is {len(pop_cumul)}')
    new_gen = []
    for i in range(len(probab)):
        for j in range(len(pop_cumul)): 
             #print(f'i is {i} j is {j}')
             if(probab[i] <= pop_cumul[j]):
                new_gen.append(population[j])
                break
            
       
    #new_gen.extend(elite_pop)
    #print(f'len new gen is {len(new_gen)}')
    return new_gen

#if __name__ == "__main__":
global_minim = 1000

def ga(function_name):
    no_params = 10
    global CROSSOVER_RATE
    global MUTATION_RATE
    not_found = 0  
    match function_name.__name__:
        case 'De_Jong':
            start_population = generate_starting_pop(no_params,N_DEJON)

            global_minim = 1000

            for i in range(0,NO_GENERATIONS):
                print(f'generation no : {i}',end='\n')
                eval_fit = evaluate_fitness(start_population,no_params,N_DEJON,De_Jong)
                if  eval_fit[2] < global_minim:
                    global_minim = eval_fit[2]
                    print(f'new minim is {global_minim}')
                else :
                    not_found+=1

                if not_found == 20 and MUTATION_RATE >0.1 and CROSSOVER_RATE < 1 :
                    CROSSOVER_RATE *= 1.1
                    MUTATION_RATE *= 0.9
                    print(CROSSOVER_RATE)
                    print(MUTATION_RATE)
                    not_found = 0

                new_gen = select_chromosome(eval_fit[1],start_population,eval_fit[3])
                new_pop = cross_over(no_params,N_DEJON,new_gen,eval_fit[3]) 

                mutate_gene(new_pop,no_params,N_DEJON)

                start_population = new_gen
            print(global_minim)
                
            
        case 'Rastrigin_Function':
            
            start_population = generate_starting_pop(no_params,N_RAS)

            global_minim = 1000
            
            for i in range(0,NO_GENERATIONS):
                print(f'generation no : {i}',end='\n')
                eval_fit = evaluate_fitness(start_population,no_params,N_RAS,function_name)
                if  eval_fit[2] < global_minim:
                    global_minim = eval_fit[2]
                    print(f'new minim is {global_minim}')
                else :
                    not_found+=1

                if not_found == 20 and MUTATION_RATE >0.1 and CROSSOVER_RATE < 1 :
                    CROSSOVER_RATE *= 1.1
                    MUTATION_RATE *= 0.9
                    print(CROSSOVER_RATE)
                    print(MUTATION_RATE)
                    not_found = 0

                new_gen = select_chromosome(eval_fit[1],start_population,eval_fit[3])
                new_pop = cross_over(no_params,N_RAS,new_gen,eval_fit[3]) 

                mutate_gene(new_pop,no_params,N_RAS)
                start_population = new_gen
            print(global_minim)
                

        case 'Schwefel_Function':   
                
            start_population = generate_starting_pop(no_params,N_SCHWEL)

            global_minim = 1000
            
            for i in range(0,NO_GENERATIONS):
                print(f'generation no : {i}',end='\n')
                eval_fit = evaluate_fitness(start_population,5,N_SCHWEL,function_name)
                if  eval_fit[2] < global_minim:
                    global_minim = eval_fit[2]
                    print(f'new minim is {global_minim}')
                else :
                    not_found+=1

                if not_found == 100 and MUTATION_RATE >0.1 and CROSSOVER_RATE < 1 :
                    CROSSOVER_RATE *= 1.1
                    MUTATION_RATE *= 0.8
                    print(CROSSOVER_RATE)
                    print(MUTATION_RATE)
                    not_found = 0
                new_gen = select_chromosome(eval_fit[1],start_population,eval_fit[3])
                new_pop = cross_over(no_params,N_SCHWEL,new_gen,eval_fit[3]) 

                mutate_gene(new_pop,no_params,N_SCHWEL)
                start_population = new_gen
            print(global_minim)
                
            

        case 'Michalewicz_Function':
            start_population = generate_starting_pop(no_params,N_MICH)
           

            global_minim = 1000
              
            for i in range(0,NO_GENERATIONS):
                print(f'generation no : {i}',end='\n')
                eval_fit = evaluate_fitness(start_population,no_params,N_MICH,function_name)
               
                if  eval_fit[2] < global_minim:
                    global_minim = eval_fit[2]
                    print(f'new minim is {global_minim}')
                else :
                    not_found+=1

                if not_found == 100 and MUTATION_RATE >0.1 or CROSSOVER_RATE < 1 :
                    CROSSOVER_RATE *= 1.1
                    MUTATION_RATE *= 0.9
                    print(CROSSOVER_RATE)
                    print(MUTATION_RATE)
                    not_found = 0
                    #print("modified!!!!!!")
                new_gen = select_chromosome(eval_fit[1],start_population,eval_fit[3])
                new_pop = cross_over(no_params,N_MICH,new_gen,eval_fit[3]) 

                mutate_gene(new_pop,no_params,N_MICH)
                start_population = new_gen
            print(global_minim)
            
#ga(Rastrigin_Function)
cProfile.run('ga(Michalewicz_Function)','res_file', sort= True)
file = open('formatted_profile.txt', 'w')
profile = pstats.Stats('./res_file', stream=file)
profile.sort_stats('time')
profile.print_stats(50)
file.close()

