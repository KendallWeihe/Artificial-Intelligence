import numpy as np
import os
import pdb
import sys
import time
import subprocess
import threading
import itertools
import random
import re


# GENETIC ALG -----------------------------------------------------------------------------------------

def crossover(formula, current_generation, crossover_with_these_individuals, num_variables):

    children = []
    for i in range(0, len(crossover_with_these_individuals), 2):
        parent_1 = current_generation[crossover_with_these_individuals[i], 0:int(num_variables/2)].copy()
        parent_2 = current_generation[crossover_with_these_individuals[i+1], int(num_variables/2):int(num_variables)].copy()
        child = np.append(parent_1, parent_2)
        children.append(child)

    return np.array(children)

def compute_genetic_fitness(formula, population):

    fitnesses = []
    for i in range(population[:,0].shape[0]):
        individual_fitness = 0
        for j in range(formula[:,0].shape[0]):
            clause_satisfied = False
            for k in range(formula[0,:].shape[0]):
                if formula[j,k] > 0:
                    if population[i,int(formula[j,k]-1)] == 1:
                        clause_satisfied = True
                elif formula[j,k] < 0:
                    if population[i,int(-1 * formula[j,k])-1] == 0:
                        clause_satisfied = True
            if clause_satisfied == True:
                individual_fitness = individual_fitness + 1

        fitnesses.append(individual_fitness)

    return np.array(fitnesses)


def genetic_alg(formula, num_variables):

    starting_generation = []
    POPULATION_SIZE = 256
    for i in range(POPULATION_SIZE):
        starting_generation.append(np.random.choice(2, int(num_variables)))

    current_generation = np.array(starting_generation)

    num_epochs = 0
    start = time.time()
    max_fitness = 0
    while time.time() - start < 5:
        crossover_with_these_individuals = random.sample(range(256), 50) # 51 is roughly 20% of 256
        children = crossover(formula, current_generation, np.array(crossover_with_these_individuals), num_variables)
        for i in range(children[:,0].shape[0]):
            p = float(np.random.randint(100)) / 100.0
            if p > 0.5:
                mutate_this_random_bit = np.random.randint(num_variables)
                children[i,int(mutate_this_random_bit)] = int(not(children[i,int(mutate_this_random_bit)]))

        population = np.concatenate((current_generation, children), axis=0)

        fitness = compute_genetic_fitness(formula, population)
        if np.amax(fitness) > max_fitness:
            max_fitness = np.amax(fitness)

        if formula[:,0].shape[0] in fitness:
            return True, None

        KILL_THIS_MANY_INDIVIDUALS = 25
        for i in range(KILL_THIS_MANY_INDIVIDUALS):
            lowest_fitness_individual = np.argmin(fitness)
            population = np.delete(population, lowest_fitness_individual, axis=0)
            fitness = np.delete(fitness, lowest_fitness_individual, axis=0)

        current_generation = population
        num_epochs = num_epochs + 1
        # print "Epoch #" + str(num_epochs) # uncomment to print the number of epochs

    return False, max_fitness

# -------------------------------------------------------------------------------

# LOCAL SEARCH ------------------------------------------------------------------

def generate_neighbors(current_state):

    neighbors = []
    for i in range(current_state.shape[0]):
        neighbor = np.zeros((current_state.shape[0]))
        for j in range(current_state.shape[0]):
            if j == i:
                neighbor[j] = int(not(current_state[j]))
            else:
                neighbor[j] = current_state[j]
        neighbors.append(neighbor)

    return np.array(neighbors)

def eval_current_state(current_state, formula):
    clause_count = 0
    for i in range(formula[:,0].shape[0]):
        # x(i) == index-1
        variable_correct_count = 0
        for j in range(formula[0,:].shape[0]):
            if formula[i,j] > 0:
                if current_state[int(formula[i,j]-1)] == 1:
                    variable_correct_count = variable_correct_count + 1
            elif formula[i,j] < 0:
                if current_state[int((-1 * formula[i,j])-1)] == 0:
                    variable_correct_count = variable_correct_count + 1
        if variable_correct_count > 0:
            clause_count = clause_count + 1

    return clause_count

def eval_neighbors(current_state, formula):

    neighbors = generate_neighbors(current_state)
    # try:
    num_clauses_satisfied = []
    for i in range(neighbors[:,0].shape[0]):
        clause_count = 0
        for j in range(formula[:,0].shape[0]):
            variable_correct_count = 0
            for k in range(formula[0,:].shape[0]):
                if formula[j,k] > 0:
                    if neighbors[i,int(formula[j,k]-1)] == 1:
                        variable_correct_count = variable_correct_count + 1
                elif formula[j,k] < 0:
                    if neighbors[i,int((-1 * formula[j,k])-1)] == 0:
                        variable_correct_count = variable_correct_count + 1
            if variable_correct_count > 0:
                clause_count = clause_count + 1
        num_clauses_satisfied.append(clause_count)

    num_clauses_satisfied = np.array(num_clauses_satisfied)
    index_of_optimal_neighbor = np.argmax(num_clauses_satisfied,axis=0)

    if eval_current_state(current_state, formula) < num_clauses_satisfied[index_of_optimal_neighbor]:
        return neighbors[np.argmax(num_clauses_satisfied,axis=0),:]
    else:
        return np.array([-1])
    # except:
    #     pdb.set_trace()
    #     print

def hill_climbing(formula, starting_state):
    current_state = starting_state
    while 1:
        optimal_neighbor = eval_neighbors(current_state, formula)
        if optimal_neighbor[0] == -1:
            return current_state
        else:
            current_state = optimal_neighbor

def is_satisfied(formula, current_state):

    # pdb.set_trace()
    for i in range(formula[:,0].shape[0]):
        clause_satisfied = False
        for j in range(formula[0,:].shape[0]):
            if formula[i,j] > 0:
                if current_state[int(formula[i,j]-1)] == 1:
                    # pdb.set_trace()
                    clause_satisfied = True
                    break
            elif formula[i,j] < 0:
                if current_state[int(-1 * formula[i,j]-1)] == 0:
                    # pdb.set_trace()
                    clause_satisfied = True
                    break
        if clause_satisfied == False:
            # pdb.set_trace()
            return False

    # pdb.set_trace()
    return True

def compute_fitness(formula, current_state):

    for i in range(formula[:,0].shape[0]):
        clause_satisfied = False
        for j in range(formula[0,:].shape[0]):
            if formula[i,j] > 0:
                if population[i,int(formula[i,j]-1)] == 1:
                    clause_satisfied = True
            elif formula[i,j] < 0:
                if population[i,int(-1 * formula[i,j])-1] == 0:
                    clause_satisfied = True
        if clause_satisfied == True:
            individual_fitness = individual_fitness + 1

    return individual_fitness

def random_restart_hill_climbing(formula, num_variables):

    start = time.time()
    max_fitness = 0
    while 1:
        random_start_state = np.random.randint(2, size=int(num_variables))
        current_state = hill_climbing(formula, random_start_state)
        fitness = compute_fitness(formula, current_state)
        if fitness > max_fitness:
            max_fitness = fitness

        if is_satisfied(formula, current_state):
            return True, formula[:,0].shape[0]

        if time.time() - start > 5:
            return False, max_fitness


# -------------------------------------------------------------------------------

# WalkSAT ------------------------------------------------------------------

def clause_not_satisfied(current_state, random_clause):

    for i in range(random_clause.shape[0]):
        if random_clause[i] > 0:
            if current_state[int(random_clause[i]-1)] == 1:
                return False
        elif random_clause[i] < 0:
            if current_state[int((-1 * random_clause[i])-1)] == 0:
                return False

    return True

def compute_fitness(formula, temp_current_state):

    fitness = 0
    for i in range(formula[:,0].shape[0]):
        for j in range(formula[0,:].shape[0]):
            if formula[i,j] > 0:
                if temp_current_state[int(formula[i,j]-1)] == 1:
                    fitness = fitness + 1
                    break
            elif formula[i,j] < 0:
                if temp_current_state[int((-1 * formula[i,j])-1)] == 0:
                    fitness = fitness + 1
                    break

    return fitness

def find_min_bit(formula, current_state):
    found_unsatisifed_clause = False
    clause_index = 0
    formula_temp = formula.copy()
    while not found_unsatisifed_clause:
        random_clause_index = np.random.randint(formula[:,0].shape[0])
        random_clause = formula[random_clause_index,:].copy()
        if clause_not_satisfied(current_state, random_clause):
            found_unsatisifed_clause = True

    max_fitness = 0
    output_current_state = current_state.copy()
    for i in range(random_clause.shape[0]):
        temp_current_state = current_state.copy()
        if random_clause[i] > 0:
            temp_current_state[int(random_clause[i]-1)] = int(not(temp_current_state[int(random_clause[i]-1)]))
        elif random_clause[i] < 0:
            temp_current_state[int((-1 * random_clause[i])-1)] = int(not(temp_current_state[int((-1 * random_clause[i])-1)]))

        fitness = compute_fitness(formula, temp_current_state)
        if fitness > max_fitness:
            max_fitness = fitness
            output_current_state = temp_current_state.copy()

    return output_current_state

def is_satisfied(formula, current_state):

    # pdb.set_trace()
    for i in range(formula[:,0].shape[0]):
        clause_satisfied = False
        for j in range(formula[0,:].shape[0]):
            if formula[i,j] > 0:
                if current_state[int(formula[i,j]-1)] == 1:
                    # pdb.set_trace()
                    clause_satisfied = True
                    break
            elif formula[i,j] < 0:
                if current_state[int(-1 * formula[i,j]-1)] == 0:
                    # pdb.set_trace()
                    clause_satisfied = True
                    break
        if clause_satisfied == False:
            # pdb.set_trace()
            return False

    # pdb.set_trace()
    return True

def walksat(formula, num_variables):

    start = time.time()
    max_fitness = 0
    current_state = np.random.randint(2, size=int(num_variables))
    while 1:

        if is_satisfied(formula, current_state):
            return True, formula[:,0].shape[0]

        prob = float(np.random.randint(100)) / 100.0

        if prob < 0.3:
            random_bit_index = np.random.randint(current_state.shape[0])
            np.put(current_state, random_bit_index, int(not(current_state[random_bit_index])))
        else:
            # pdb.set_trace()
            current_state = find_min_bit(formula, current_state)

        fitness = compute_fitness(formula, current_state)
        if fitness > max_fitness:
            max_fitness = fitness

        if time.time() - start > 5:
            return False, max_fitness


# -------------------------------------------------------------------------------

def main():
    num_algs = 3
    num_trials = 10
    difficulties = ["easy/", "hard/"]
    for difficulty in difficulties:

        # I chose to generate filenames since they are from 1-100
        # python isn't good at sorting numeric strings
        # if you want to test out entire directories, uncomment and comment the below lines

        # filenames = os.listdir(difficulty) # uncomment
        # filenames.sort()
        filenames = []  # comment
        for i in range(1,101):
            filenames.append(str(i) + ".cnf")

        for filename in filenames:
            file_path = difficulty + filename
            formula = np.genfromtxt(file_path)
            print "Formula -- " + file_path + "--------------------"
            for i in range(num_algs):
                if i == 0:
                    print "     Running a Genetic algorithm..."
                elif i == 1:
                    print "     Running the Hill Climbing algorithm..."
                else:
                    print "     Running the WalkSAT algorithm..."

                for j in range(num_trials):
                    if i == 0:
                        # pdb.set_trace()
                        num_variables = formula[0,2]
                        genetic_formula = formula[1:formula[:,0].shape[0],:].copy()
                        start = time.time()
                        satisfiable, max_fitness = genetic_alg(genetic_formula, num_variables)
                        if satisfiable:
                            print "                 This is satisfiable"
                        else:
                            print "                 This is NOT satisfiable"
                            print "                 Max fitness = " + str(max_fitness)
                        end = time.time() - start
                        times = np.genfromtxt("gen_alg_times.csv", delimiter="\n")
                        times = np.append(times, end)
                        np.savetxt("gen_alg_times.csv", times, delimiter="\n")
                        c = np.genfromtxt("gen_alg_c.csv", delimiter="\n")
                        c = np.append(c, max_fitness)
                        np.savetxt("gen_alg_c.csv", c, delimiter="\n")

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
                        end = time.time() - start
                        times = np.genfromtxt("hill_climbing_alg_times.csv", delimiter="\n")
                        times = np.append(times, end)
                        np.savetxt("hill_climbing_alg_times.csv", times, delimiter="\n")
                        c = np.genfromtxt("hill_climbing_alg_c.csv", delimiter="\n")
                        c = np.append(c, max_fitness)
                        np.savetxt("hill_climbing_alg_c.csv", c, delimiter="\n")

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
                        end = time.time() - start
                        times = np.genfromtxt("walksat_alg_times.csv", delimiter="\n")
                        times = np.append(times, end)
                        np.savetxt("walksat_alg_times.csv", times, delimiter="\n")
                        c = np.genfromtxt("walksat_alg_c.csv", delimiter="\n")
                        c = np.append(c, max_fitness)
                        np.savetxt("walksat_alg_c.csv", c, delimiter="\n")


            print "-------------------------------------------------"

main()
