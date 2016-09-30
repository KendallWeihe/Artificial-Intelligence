# Author: Kendall Weihe
# Purpose:
#     Genetic algorithm
#     Hill Climbing algorithm
#     WalkSAT algorithm
# Please refer to README.txt

import numpy as np
import os
import pdb
import sys
import time
import random

# GENETIC ALG -----------------------------------------------------------------------------------------

# General flow of control:
#     genetic_alg() calls crossover() function to compute genetic crossovers
#         I decided to implement the crossover where the first half of the child is from parent 1 and the second half is from parent 2
#     genetic_alg() calls compute_genetic_fitness() to compute fitness for entire population
#
# genetic_alg():
#     generate starting population
#     generate a random sample of 50 (20% of population) to conduct crossover with
#     call crossover()
#     mutate randomly selected children -- mutation occurs by flipping a randomly selected bit
#     compute fitness for entire population -- parents + children
#     record if there is a new maximum fitness
#     if there exists a fitness value equal to the number of clauses: return True
#     kill the 25 individuals with the lowest fitness values
#     loop until timer runs out
#
# crossover():
#     iterate over crossover population
#     for each pair:
#         extract first half of parent 1
#         extract second half of parent 2
#         concatenate both halves into the child
#     return all children
#
# compute_genetic_fitness():
#     iterate over entire population:
#         iterate over each clause
#             iterate over each variable:
#                 if there exists a truth variable, then set clause_satisfied flag to True
#             if clause_satisfied is True, then increment individuals fitness
#         append individuals fitness to array (the array will be in same ordering as the population)
#     return fitnesses array

def crossover(formula, current_generation, crossover_with_these_individuals, num_variables):

    children = []
    for i in range(0, len(crossover_with_these_individuals), 2):
        parent_1 = current_generation[crossover_with_these_individuals[i], 0:int(num_variables/2)].copy() # parent 1
        parent_2 = current_generation[crossover_with_these_individuals[i+1], int(num_variables/2):int(num_variables)].copy() # parent 2
        child = np.append(parent_1, parent_2) # append both halves and assign to child
        children.append(child)

    return np.array(children)

def compute_genetic_fitness(formula, population):

    fitnesses = []
    for i in range(population[:,0].shape[0]): # iterate over population
        individual_fitness = 0 # individuals fitness starts at 0
        for j in range(formula[:,0].shape[0]): # iterate over clauses
            clause_satisfied = False # clause satisfied starts at False
            for k in range(formula[0,:].shape[0]): # iterate over single clause
                if formula[j,k] > 0:
                    if population[i,int(formula[j,k]-1)] == 1: # if the individuals variable is set to true then set clause_satisfied to True
                        clause_satisfied = True
                elif formula[j,k] < 0:
                    if population[i,int(-1 * formula[j,k])-1] == 0:
                        clause_satisfied = True
            if clause_satisfied == True: # if the clause was satisfied, then increment the individals fitness value
                individual_fitness = individual_fitness + 1

        fitnesses.append(individual_fitness) # append the individuals fitness value to the populations fitness values

    return np.array(fitnesses)

def genetic_alg(formula, num_variables):

    starting_generation = [] # generate starting population -- randomly
    POPULATION_SIZE = 256
    for i in range(POPULATION_SIZE):
        starting_generation.append(np.random.choice(2, int(num_variables))) # random generator

    current_generation = np.array(starting_generation)

    num_epochs = 0
    start = time.time()
    max_fitness = 0
    while time.time() - start < int(sys.argv[1]): # loop until timer runs out
        crossover_with_these_individuals = random.sample(range(256), 50) # 50 is roughly 20% of 256
        children = crossover(formula, current_generation, np.array(crossover_with_these_individuals), num_variables) # perform crossover -- generate children
        for i in range(children[:,0].shape[0]): # iterate over children
            p = float(np.random.randint(100)) / 100.0
            if p > 0.5: # randomly select children to mutate
                mutate_this_random_bit = np.random.randint(num_variables) # mutate a random bit
                children[i,int(mutate_this_random_bit)] = int(not(children[i,int(mutate_this_random_bit)]))

        population = np.concatenate((current_generation, children), axis=0) # add children to entire population

        fitness = compute_genetic_fitness(formula, population) # compute entire populations fitnesses
        if np.amax(fitness) > max_fitness: # check if new max fitness
            max_fitness = np.amax(fitness)

        if formula[:,0].shape[0] in fitness: # if there exists a fitness score equal to the number of clauses, return True
            return True, None

        KILL_THIS_MANY_INDIVIDUALS = 25 # kill individals with fitness value inversely related to the number of clauses
        for i in range(KILL_THIS_MANY_INDIVIDUALS):
            lowest_fitness_individual = np.argmin(fitness)
            population = np.delete(population, lowest_fitness_individual, axis=0)
            fitness = np.delete(fitness, lowest_fitness_individual, axis=0)

        current_generation = population
        num_epochs = num_epochs + 1
        # print "Epoch #" + str(num_epochs) # TODO uncomment to print the number of epochs

    return False, max_fitness # timer expired

# -------------------------------------------------------------------------------

# LOCAL SEARCH ------------------------------------------------------------------

# NOTE: a lot of code overlaps, I apologize, the genetic algorithm is much cleaner
#
# General flow of control:
#     random_restart_hill_climbing() invokes hill_climbing()
#         hill_climbing() invokes eval_neighbors()
#             eval_neighbors() invokes generate_neighbors()
#             eval_neighbors() invokes eval_current_state()
#     random_restart_hill_climbing() invokes is_satisfied()
#
# random_restart_hill_climbing():
#         loop until timer runs out
#             generate random starting state
#             climb the hill until a plateau is reached
#             compute fitness
#             update maximum fitness is new max found
#             if is_satisfied(): return True
#
# compute_fitness():
#     note: I could have used this function to test if satisfied -- hindsight
#     iterate through clauses
#         iterate through clause (singular)
#             if variable satisfied: increment individuals fitness
#     return individuals fitness
#
# is_satisfied():
#     iterate through clauses
#         iterate through clause (singular)
#             if no variables satisfied: return False
#     return True
#
# hill_climbing():
#     loop until plateau
#         find optimal_neighbor()
#         if optimal_neighbor < current_state: return current state --> plateau reached
#         else: current_state becomes optimal neighbor
#
# eval_neighbors():
#     generate all neighbors -- generate_neighbors()
#     iterate throuhg neighbors
#         iterate through clauses
#             iterate through clause (singular)
#                 if clause satisfied: increment individuals fitness
#         append individuals total fitness to array
#
#     if current_state fitness < optimal neighbor: return optimal neighbor
#     else: return -1
#
# eval_current_state():
#     iterate through clauses
#         iterate through clause
#             if clause is satisfied: increment individuals fitness
#     return individuals fitness
#
# generate_neighbors():
#     iterate through the length of the current state (i)
#         iterate through the length of the current state (j)
#             if j == i: flip the bit
#     return neighbors

def generate_neighbors(current_state):

    neighbors = []
    for i in range(current_state.shape[0]): # there should be as many neighbors as the length of the current state
        neighbor = np.zeros((current_state.shape[0]))
        for j in range(current_state.shape[0]):
            if j == i: # if this bit hasn't been flipped, then flip
                neighbor[j] = int(not(current_state[j]))
            else:
                neighbor[j] = current_state[j]
        neighbors.append(neighbor)

    return np.array(neighbors)

def eval_current_state(current_state, formula):
    clause_count = 0
    for i in range(formula[:,0].shape[0]): # iterate through clauses
        # x(i) == index-1
        variable_correct_count = 0
        for j in range(formula[0,:].shape[0]): # iterate through clause
            if formula[i,j] > 0:
                if current_state[int(formula[i,j]-1)] == 1:
                    variable_correct_count = variable_correct_count + 1
            elif formula[i,j] < 0:
                if current_state[int((-1 * formula[i,j])-1)] == 0:
                    variable_correct_count = variable_correct_count + 1
        if variable_correct_count > 0: # if clause satisfied, increment individuals fitness
            clause_count = clause_count + 1

    return clause_count

def eval_neighbors(current_state, formula):

    neighbors = generate_neighbors(current_state) # generate neighbors
    num_clauses_satisfied = []
    for i in range(neighbors[:,0].shape[0]): # iterate through neighbors
        clause_count = 0
        for j in range(formula[:,0].shape[0]): # iterate through clauses
            variable_correct_count = 0
            for k in range(formula[0,:].shape[0]): # iterate through clause
                if formula[j,k] > 0:
                    if neighbors[i,int(formula[j,k]-1)] == 1:
                        variable_correct_count = variable_correct_count + 1
                elif formula[j,k] < 0:
                    if neighbors[i,int((-1 * formula[j,k])-1)] == 0:
                        variable_correct_count = variable_correct_count + 1
            if variable_correct_count > 0: # if clause is satisfied, increment individuals fitness
                clause_count = clause_count + 1
        num_clauses_satisfied.append(clause_count)

    num_clauses_satisfied = np.array(num_clauses_satisfied)
    index_of_optimal_neighbor = np.argmax(num_clauses_satisfied,axis=0) # indexl of optimal_neighbor

    if eval_current_state(current_state, formula) < num_clauses_satisfied[index_of_optimal_neighbor]: # if optimal neighbor better than current state
        return neighbors[np.argmax(num_clauses_satisfied,axis=0),:] # return optimal neighbor
    else:
        return np.array([-1]) # else return -1

def hill_climbing(formula, starting_state):
    current_state = starting_state
    while 1:
        optimal_neighbor = eval_neighbors(current_state, formula) # find optimal neighbor
        if optimal_neighbor[0] == -1: # if there is no optimal neighbor, return current state
            return current_state
        else:
            current_state = optimal_neighbor # else set current_state to optimal neighbor

def is_satisfied(formula, current_state):

    # pdb.set_trace()
    for i in range(formula[:,0].shape[0]): # iterate through clauses
        clause_satisfied = False
        for j in range(formula[0,:].shape[0]): # iterate through clause
            if formula[i,j] > 0:
                if current_state[int(formula[i,j]-1)] == 1:
                    # pdb.set_trace()
                    clause_satisfied = True # if satisfied, set flag to True and break
                    break
            elif formula[i,j] < 0:
                if current_state[int(-1 * formula[i,j]-1)] == 0:
                    # pdb.set_trace()
                    clause_satisfied = True
                    break
        if clause_satisfied == False: # if clause isn't satisfied return False
            # pdb.set_trace()
            return False

    return True # all clauses are satisfied

def compute_fitness(formula, current_state):

    for i in range(formula[:,0].shape[0]): # iterate through clauses
        clause_satisfied = False
        for j in range(formula[0,:].shape[0]): # iterate through clause
            if formula[i,j] > 0:
                if population[i,int(formula[i,j]-1)] == 1:
                    clause_satisfied = True # if satisfied, set to True
            elif formula[i,j] < 0:
                if population[i,int(-1 * formula[i,j])-1] == 0:
                    clause_satisfied = True
        if clause_satisfied == True: # if clause_satisfied increment individual_fitness
            individual_fitness = individual_fitness + 1

    return individual_fitness

def random_restart_hill_climbing(formula, num_variables):

    start = time.time()
    max_fitness = 0
    while 1:
        random_start_state = np.random.randint(2, size=int(num_variables)) # random starting state
        current_state = hill_climbing(formula, random_start_state) # climb hill
        fitness = compute_fitness(formula, current_state) # compute fitness
        if fitness > max_fitness: # update max fitness
            max_fitness = fitness

        if is_satisfied(formula, current_state): # if satisfied return True
            return True, formula[:,0].shape[0]

        if time.time() - start > int(sys.argv[1]): # if timer ran out, return False
            return False, max_fitness


# -------------------------------------------------------------------------------

# WalkSAT ------------------------------------------------------------------

# NOTE: a lot of code overlaps, I apologize, the genetic algorithm is much cleaner
#
# General flow of control:
#     walksat() invokes is_satisfied()
#     walksat() invokes find_optimal_bit()
#         find_optimal_bit() invokes clause_not_satisfied()
#     walksat() invokes compute_fitness()
#
# walksat():
#     generate random starting state
#     loop until timer runs out
#         check if satisfied: return True
#         generate random probability p
#         if p < 0.3 (tunable) then flip random bit
#         else find the bit that when flipped will yield a higher fitness
#         compute fitness and update max fitness
#
# is_satisfied():
#     same as is_satisfied() from hill climbing
#
# find_optimal_bit():
#     find a random clause that isn't satisfied
#     iterate through this ^^ clause
#         iteratively flip each bit
#         compute fitness
#         keep track of which flipped bit yielded the maximum fitness
#     return state that yielded highest fitness
#
# compute_fitness():
#     same as compute_fitness() from genetic_alg()
#
# clause_not_satisfied():
#     iterate through randomly selected clause (from find_optimal_bit())
#         if a variable is satisfied within clause: return False
#     return True


def clause_not_satisfied(current_state, random_clause):

    for i in range(random_clause.shape[0]): # iterate through clause
        if random_clause[i] > 0:
            if current_state[int(random_clause[i]-1)] == 1:
                return False # if there exists a variable that satisfies the clause, then return false
        elif random_clause[i] < 0:
            if current_state[int((-1 * random_clause[i])-1)] == 0:
                return False

    return True # all variables satisfied the clause

def compute_fitness(formula, temp_current_state):

    fitness = 0
    for i in range(formula[:,0].shape[0]): # iterate through clauses
        for j in range(formula[0,:].shape[0]): # iterate through clause
            if formula[i,j] > 0:
                if temp_current_state[int(formula[i,j]-1)] == 1:
                    fitness = fitness + 1 # if clause satisfied, increment fitness and break
                    break
            elif formula[i,j] < 0:
                if temp_current_state[int((-1 * formula[i,j])-1)] == 0:
                    fitness = fitness + 1
                    break

    return fitness

def find_optimal_bit(formula, current_state):
    found_unsatisifed_clause = False
    clause_index = 0
    formula_temp = formula.copy()
    while not found_unsatisifed_clause: # loop until a clause is found that is not satisfied
        random_clause_index = np.random.randint(formula[:,0].shape[0]) # generate random index
        random_clause = formula[random_clause_index,:].copy() # this is the random clause
        if clause_not_satisfied(current_state, random_clause): # check if clause is not satisfied
            found_unsatisifed_clause = True # clause not satisgied, exit loop

    max_fitness = 0
    output_current_state = current_state.copy()
    for i in range(random_clause.shape[0]): # iterate through non-satified clause
        temp_current_state = current_state.copy()
        if random_clause[i] > 0:
            temp_current_state[int(random_clause[i]-1)] = int(not(temp_current_state[int(random_clause[i]-1)])) # flip the bit
        elif random_clause[i] < 0:
            temp_current_state[int((-1 * random_clause[i])-1)] = int(not(temp_current_state[int((-1 * random_clause[i])-1)]))

        fitness = compute_fitness(formula, temp_current_state) # compute the fitness
        if fitness > max_fitness: # if a larger fitness is found, keep track of this clause
            max_fitness = fitness
            output_current_state = temp_current_state.copy()

    return output_current_state

def is_satisfied(formula, current_state):

    for i in range(formula[:,0].shape[0]):
        clause_satisfied = False
        for j in range(formula[0,:].shape[0]):
            if formula[i,j] > 0:
                if current_state[int(formula[i,j]-1)] == 1:
                    clause_satisfied = True
                    break
            elif formula[i,j] < 0:
                if current_state[int(-1 * formula[i,j]-1)] == 0:
                    clause_satisfied = True
                    break
        if clause_satisfied == False:
            return False

    return True

def walksat(formula, num_variables):

    start = time.time()
    max_fitness = 0
    current_state = np.random.randint(2, size=int(num_variables)) # generate random start state
    while 1:

        if is_satisfied(formula, current_state): # check if satisfied
            return True, formula[:,0].shape[0]

        prob = float(np.random.randint(100)) / 100.0 # generate random probability

        if prob < 0.3: # this value can be tuned
            random_bit_index = np.random.randint(current_state.shape[0]) # find random bit and flip
            np.put(current_state, random_bit_index, int(not(current_state[random_bit_index])))
        else:
            current_state = find_optimal_bit(formula, current_state) # find the the bit, that when flipped, will produce the optimal fitness

        fitness = compute_fitness(formula, current_state) # compute fitness and keep track of highest fitness found
        if fitness > max_fitness:
            max_fitness = fitness

        if time.time() - start > int(sys.argv[1]): # exit if timer ran out
            return False, max_fitness

# -------------------------------------------------------------------------------

def main():
    num_algs = 3
    num_trials = 10

    # TODO: to add new directories, edit the below array
    difficulties = ["easy/", "hard/"]
    for difficulty in difficulties: # loop through directories

        # TODO
        # I chose to generate filenames since they are from 1-100
        # python isn't good at sorting numeric strings
        # if you want to test out entire directories, uncomment and comment the below lines

        # filenames = os.listdir(difficulty) # uncomment
        # filenames.sort()
        filenames = []  # comment
        for i in range(1,101):
            filenames.append(str(i) + ".cnf")

        for filename in filenames: # loop through formulas
            file_path = difficulty + filename
            formula = np.genfromtxt(file_path)
            print "Formula -- " + file_path + "--------------------"
            for i in range(num_algs): # loop through the three different algorithms
                if i == 0:
                    print "     Running a Genetic algorithm..."
                elif i == 1:
                    print "     Running the Hill Climbing algorithm..."
                else:
                    print "     Running the WalkSAT algorithm..."

                for j in range(num_trials): # conduct num_trails experiments
                    if i == 0:
                        num_variables = formula[0,2]
                        genetic_formula = formula[1:formula[:,0].shape[0],:].copy()
                        start = time.time()
                        satisfiable, max_fitness = genetic_alg(genetic_formula, num_variables)
                        if satisfiable:
                            print "                 This is satisfiable"
                        else:
                            print "                 This is NOT satisfiable"
                            print "                 Max fitness = " + str(max_fitness)

                        # TODO: to record times and maximum fitnesses, uncomment below lines
                        # end = time.time() - start
                        # times = np.genfromtxt("gen_alg_times_hard.csv", delimiter="\n")
                        # times = np.append(times, str(end))
                        # np.savetxt("gen_alg_times_hard.csv", times, delimiter="\n", fmt="%s")
                        # c = np.genfromtxt("gen_alg_c_hard.csv", delimiter="\n")
                        # c = np.append(c, str(max_fitness))
                        # np.savetxt("gen_alg_c_hard.csv", c, delimiter="\n", fmt="%s")

                    elif i == 1:
                        num_variables = formula[0,2]
                        hill_climbing_formula = formula[1:formula[:,0].shape[0],:].copy()
                        start = time.time()
                        satisfiable, max_fitness = random_restart_hill_climbing(hill_climbing_formula, num_variables)
                        if satisfiable:
                            print "                 This is satisfiable"
                        else:
                            print "                 This is NOT satisfiable"
                            print "                 Max fitness = " + str(max_fitness)

                        # TODO: to record times and maximum fitnesses, uncomment below lines
                        # end = time.time() - start
                        # times = np.genfromtxt("hill_climbing_alg_times_hard.csv", delimiter="\n")
                        # times = np.append(times, str(end))
                        # np.savetxt("hill_climbing_alg_times_hard.csv", times, delimiter="\n", fmt="%s")
                        # c = np.genfromtxt("hill_climbing_alg_c_hard.csv", delimiter="\n")
                        # c = np.append(c, str(max_fitness))
                        # np.savetxt("hill_climbing_alg_c_hard.csv", c, delimiter="\n", fmt="%s")

                    elif i == 2:
                        num_variables = formula[0,2]
                        walksat_formula = formula[1:formula[:,0].shape[0],:].copy()
                        start = time.time()
                        satisfiable, max_fitness = walksat(walksat_formula, num_variables)
                        if satisfiable:
                            print "                 This is satisfiable"
                        else:
                            print "                 This is NOT satisfiable"
                            print "                 Max fitness = " + str(max_fitness)

                        # TODO: to record times and maximum fitnesses, uncomment below lines
                        # end = time.time() - start
                        # times = np.genfromtxt("walksat_alg_times_hard.csv", delimiter="\n")
                        # times = np.append(times, str(end))
                        # np.savetxt("walksat_alg_times_hard.csv", times, delimiter="\n", fmt="%s")
                        # c = np.genfromtxt("walksat_alg_c_hard.csv", delimiter="\n")
                        # c = np.append(c, str(max_fitness))
                        # np.savetxt("walksat_alg_c_hard.csv", c, delimiter="\n", fmt="%s")


            print "-------------------------------------------------"


try:
    sys.argv[1]
except:
    print "Wrong arguments"
    print "Usage: python prog3.py <timer threshold>"
    sys.exit()

main() # call main function
