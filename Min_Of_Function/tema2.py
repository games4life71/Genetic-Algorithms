from asyncio.windows_events import NULL
import math
import numpy as np
import time
import random

# type 0

start_time = time.time()
def De_Jong(params):
   
   return sum(val**2 for val in params)
  
def Rastrigin_Function(params):
    return 10*len(params) + sum(i**2 - 10*math.cos(2*math.pi*i) for i in params)

def Schwefel_Function(params):
    return sum((-i)*math.sin(math.sqrt(math.abs(i))) for i in params)

def Michalewicz_Function(params):
    return sum(math.sin(i)* math.pow(math.sin((j*i**2)/math.pi),2*len(params)) for j,i in enumerate(params))

def decode(solution, a, b, no_of_bits):
    return (a + binatodeci(solution)*(b-a)/(pow(2, no_of_bits)-1))

def binatodeci(binary):
    return sum(val*(2**idx) for idx, val in enumerate(reversed(binary)))


def generate_neighbours(solution):  #length is the slicing length       
        vn = []
    
        #get the current param representation
         
        for line, entry in enumerate(solution):
            aux = solution.copy()
            if aux[line] == 1:
                aux[line] = 0
            else:
                aux[line] = 1
            vn.append(aux)
        return vn

# search for all best neighbour -- if not one return -1


def improve_best(neighbours, function, curr_sol,a,b,no_of_bits):

    best = []
    best_val = curr_sol
    for entry in neighbours:
        # convert to decimal
        # decode all params and make a list of them 
        param_list = []
        for i  in range(0,len(entry),no_of_bits):
            param_list.append(decode(entry[i:i+no_of_bits],a,b,no_of_bits))

        dec_val = function(param_list) 
        
        if  dec_val < curr_sol:
            best_val = dec_val
            best = entry

    if best_val == curr_sol:
        return None
    else:
        return best


def improve_first(neighbours, function, curr_sol,a,b,no_of_bits):

     for entry in neighbours:
        # convert to decimal
        # decode all params and make a list of them 
        param_list = []
        for i  in range(0,len(entry),no_of_bits):
            param_list.append(decode(entry[i:i+no_of_bits],a,b,no_of_bits))

        dec_val = function(param_list)  # get the real value of the function 
        
        if  dec_val < curr_sol:
            return entry





def compare_eval(sol1, sol2, function,a,b,no_of_bits):
    
    if function(convert_to_list(sol1,a,b,no_of_bits)) < function(convert_to_list(sol2,a,b,no_of_bits)):
        return True

def convert_to_list(sol , a,b,no_of_bits):
    param_list = []
    for i in range(0,len(sol),no_of_bits):
            param_list.append(decode(sol[i:i+no_of_bits],a,b,no_of_bits))
    return param_list

def hill_climbing(t, no_of_bits, a, b, function, improv,no_of_params):  # improv -- 0 for best , 1 for first

 best = None 
    #number of test to be made 
 with open("dejong_res.txt","a") as res :
    for i in range(0, t):
        #local = False
        print(f'iteration number {i}')
       # vc = np.random.randint(2, size=n*no_of_params)
        vc = []
        for i in range(0,n*no_of_params):
            vc.append(random.randint(0,1))            
       # print(vc)
        #convert to real value 
        param_list = []

        for i in range(0,len(vc),no_of_bits):
            param_list.append(decode(vc[i:i+no_of_bits],a,b,no_of_bits))
        print(param_list)
        #dec_vc = decode(vc, a, b, n)  # real value of the bitstring
        curr_sol = function(param_list)  # value of function(random_gen_sol)
        #print(f'curr_sol is {curr_sol}')
       # print(i)

        neighbours = generate_neighbours(vc)  # hamming's 1 neighbours
        #print(neighbours)
        candidate = []

        match(improv):
            case 0:
                candidate = improve_best(neighbours, function, curr_sol,a,b,no_of_bits)
               # print(candidate)
                pass
            case 1:

                candidate = improve_first(neighbours, function, curr_sol,a,b,no_of_bits)
                pass
        if candidate is not None:
            
            # if we found a smaller local value , we update
            if best is None:
                #print("best is none")
                best = candidate

            # compare  candidate with best
            elif compare_eval(candidate, best, function,a,b,no_of_bits) == True:
                best = candidate
    res.write(f'The best value found for {function} is {str(function(convert_to_list(best,a,b,no_of_bits)))}: ...exec time is  {time.time()-start_time} seconds'+"\n")
    return function(convert_to_list(best,a,b,no_of_bits))
precision= 2
n = math.trunc(math.log2((5.12+5.12)*pow(10,precision))) #number of bits required
#print(f'n is {n}')


print(hill_climbing(100000 ,n,-5.12,5.12,Rastrigin_Function,0,5))
#print(Rastrigin_Function([1,2,3]))

