import numpy as np
import os
import pdb
import sys
import time
import subprocess

# LOCAL SEARCH ------------------------------------------------------------------

def generate_neighbors(current_state):

    # for i in range(possible_neighbors[:,0].shape[0]):
    #     mask = np.bitwise_and(current_state, possible_neighbors[i,:])
    #     one_different = 0
    #     for j in range(mask.shape[0]):
    #         if current_state[j] != mask[j]:
    #             one_different = one_different + 1
    #         if one_different > 1:
    #             break
    #     if one_different == 1:
    #         neighbor.append(possible_neighbors[i,:])

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
    #TODO
        # while 1
        #     optimal_neighbor = eval_neighbors(random_start_state, formula)
        #     if optimal_neighbor == -1:
        #         return current state
        #     else:
        #         neighbor is better, keep going
        #         current_state = optimal_neighbor

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

def random_restart_hill_climbing(formula, num_variables):

    while 1:
        random_start_state = np.random.randint(2, size=int(num_variables))
        current_state = hill_climbing(formula, random_start_state)
        # pdb.set_trace()
        # import itertools
        # lst = list(itertools.product([0, 1], repeat=int(num_variables)))
        # for i in range(len(lst)):
        #     temp_arr = np.array(lst[i])
        #     satisfied = is_satisfied(formula, temp_arr)
        #     print satisfied
        # pdb.set_trace()

        if is_satisfied(formula, current_state):
            return True


# -------------------------------------------------------------------------------

# pdb.set_trace()
formula = np.genfromtxt(sys.argv[1])
num_variables = formula[0,2]
formula = formula[1:formula[:,0].shape[0],:].copy()
satisfiable = random_restart_hill_climbing(formula, num_variables)
# pdb.set_trace()
if satisfiable:
    print "             This formula was satisfied"
else:
    print "             Hill climbing did not find a satisfiable solution"
