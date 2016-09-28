import numpy as np
import os
import pdb
import sys
import time
import subprocess

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

    current_state = np.random.randint(2, size=int(num_variables))
    while 1:

        if is_satisfied(formula, current_state):
            return True

        prob = float(np.random.randint(100)) / 100.0

        if prob < 0.3:
            random_bit_index = np.random.randint(current_state.shape[0])
            np.put(current_state, random_bit_index, int(not(current_state[random_bit_index])))
        else:
            # pdb.set_trace()
            current_state = find_min_bit(formula, current_state)

# -------------------------------------------------------------------------------

# pdb.set_trace()
formula = np.genfromtxt(sys.argv[1])
num_variables = formula[0,2]
formula = formula[1:formula[:,0].shape[0],:].copy()
satisfiable = walksat(formula, num_variables)
# pdb.set_trace()
if satisfiable:
    print "             This formula was satisfied"
