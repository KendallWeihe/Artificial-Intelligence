import numpy as np
import os
import pdb
import sys
import time
import subprocess
import threading
import itertools

# #TODO:
#     choose random 20% of pop to do crossover
#         crossover produces 1 child
#     generate mutation probability
#         if > 0.5 then pick one bit to mutate
#
#
#
# def genetic_alg(formula, num_variables):
#     # generate a population size that is of size 256
#     current_generation = []
#     for i in range(256):
#         current_generation.append(np.random.choice(2,num_variables))
#
#     num_epochs = 1000
#     for i in range(num_epochs):

# DPLL --------------------------------------------------------------------------
#
# def consistent_set_of_literals(phi):
#     explored_literals = []
#     # pdb.set_trace()
#     for i in range(phi[:,0].shape[0]):
#         for j in range(phi[0,:].shape[0]):
#             if phi[i,j] not in explored_literals:
#                 explored_literals.append(phi[i,j])
#                 if -explored_literals[len(explored_literals)-1] in phi:
#                     return False
#
#     return True
#
# def contains_empty_clause(phi):
#     for i in range(phi[:,0].shape[0]):
#         temp_clause = phi[i,:].copy()
#         truncated_clause = temp_clause[temp_clause != 0]
#         if truncated_clause.shape[0] == 0:
#             return True
#
#     return False
#
# def find_unit_clauses(phi):
#     unit_clauses = []
#     for i in range(phi[:,0].shape[0]):
#         temp_clause = phi[i,:].copy()
#         truncated_clause = temp_clause[temp_clause != 0]
#         if truncated_clause.shape[0] == 1:
#             unit_clauses.append(truncated_clause[0])
#
#     return unit_clauses
#
# def find_pure_literals(phi):
#     explored_literals = []
#     pure_literals = []
#     for i in range(phi[:,0].shape[0]):
#         for j in range(phi[0,:].shape[0]):
#             if phi[i,j] not in explored_literals:
#                 explored_literals.append(phi[i,j])
#                 if explored_literals[len(explored_literals)-1] != 0 and -explored_literals[len(explored_literals)-1] not in phi:
#                     pure_literals.append(phi[i,j])
#     return np.array(pure_literals)
#
# def dpll(phi):
#
#     if consistent_set_of_literals(phi):
#         return True
#     if contains_empty_clause(phi):
#         return False
#
#     pure_literals = find_pure_literals(phi)
#     for pure_literal in pure_literals:
#         delete_these_indices = np.where(phi==pure_literal)[0]
#         phi = np.delete(phi, (delete_these_indices), 0)
#         if phi.shape[0] == 0:
#             phi = np.array([[0,0,0,0]])
#
#     unit_clauses = find_unit_clauses(phi)
#     for unit_clause in unit_clauses:
#         delete_these_indices = np.where(phi==unit_clause)[0]
#         phi = np.delete(phi, (delete_these_indices), 0)
#         np.place(phi,phi == -unit_clause, 0)
#         if phi.shape[0] == 0:
#             phi = np.array([[0,0,0,0]])
#
#
#     first_literal = None
#     for i in range(phi[:,0].shape[0]):
#         temp_clause = phi[i,:].copy()
#         temp_clause = temp_clause[temp_clause != 0]
#         if temp_clause.shape[0] != 0:
#             first_literal = temp_clause[0]
#             break
#
#     if first_literal == None:
#         first_literal = 0
#
#     # pdb.set_trace()
#     additional_tuple = np.zeros((phi[0,:].shape[0]))
#     additional_tuple[0] = first_literal
#     phi_and_first_literal = np.vstack((phi, additional_tuple))
#     phi_and_first_literal_not = np.vstack((phi, -additional_tuple))
#
#     return dpll(phi_and_first_literal) or dpll(phi_and_first_literal_not)
#
# # -------------------------------------------------------------------------------

# DPLL --------------------------------------------------------------------------

def consistent_set_of_literals(phi):
    explored_literals = []
    # pdb.set_trace()
    all_empty = True
    for i in range(phi[:,0].shape[0]):
        for j in range(phi[0,:].shape[0]):
            if phi[i,j] not in explored_literals:
                explored_literals.append(phi[i,j])
                if explored_literals[len(explored_literals)-1] != 0:
                    all_empty = False
                    if -explored_literals[len(explored_literals)-1] in phi:
                        return False

    if all_empty:
        return False
    else:
        return True

def contains_empty_clause(phi):
    for i in range(phi[:,0].shape[0]):
        temp_clause = phi[i,:].copy()
        truncated_clause = temp_clause[temp_clause != 0]
        if truncated_clause.shape[0] == 0:
            return True

    return False

def find_unit_clauses(phi):
    unit_clauses = []
    for i in range(phi[:,0].shape[0]):
        temp_clause = phi[i,:].copy()
        truncated_clause = temp_clause[temp_clause != 0]
        if truncated_clause.shape[0] == 1:
            unit_clauses.append(truncated_clause[0])

    return unit_clauses

def find_pure_literals(phi):
    explored_literals = []
    pure_literals = []
    for i in range(phi[:,0].shape[0]):
        for j in range(phi[0,:].shape[0]):
            if phi[i,j] not in explored_literals:
                explored_literals.append(phi[i,j])
                if explored_literals[len(explored_literals)-1] != 0 and -explored_literals[len(explored_literals)-1] not in phi:
                    pure_literals.append(phi[i,j])
    return np.array(pure_literals)

explored_vars = []
def dpll(phi):
    if consistent_set_of_literals(phi):
        return True
    if contains_empty_clause(phi):
        return False

    pure_literals = find_pure_literals(phi)
    for pure_literal in pure_literals:
        delete_these_indices = np.where(phi==pure_literal)[0]
        phi = np.delete(phi, (delete_these_indices), 0)
        if phi.shape[0] == 0:
            phi = np.array([[0,0,0,0]])

    unit_clauses = find_unit_clauses(phi)
    for unit_clause in unit_clauses:
        delete_these_indices = np.where(phi==unit_clause)[0]
        phi = np.delete(phi, (delete_these_indices), 0)
        np.place(phi,phi == -unit_clause, 0)
        if phi.shape[0] == 0:
            phi = np.array([[0,0,0,0]])

    first_literal = None
    found = False
    for i in range(phi[:,0].shape[0]):
        temp_clause = phi[i,:].copy()
        temp_clause = temp_clause[temp_clause != 0]
        for j in range(temp_clause.shape[0]):
            if temp_clause[j] != 0:
                first_literal = temp_clause[j]
                found = True
                break
        if found == True:
            break

    if first_literal == None:
        first_literal = 0

    additional_tuple = np.zeros((phi[0,:].shape[0]))
    additional_tuple[0] = first_literal
    phi_and_first_literal = np.vstack((phi, additional_tuple))
    phi_and_first_literal_not = np.vstack((phi, -additional_tuple))
    explored_vars.append(first_literal)
    explored_vars.append(-first_literal)

    return dpll(phi_and_first_literal) or dpll(phi_and_first_literal_not)

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

def random_restart_hill_climbing(formula, num_variables):

    start = time.time()
    while 1:
        random_start_state = np.random.randint(2, size=int(num_variables))
        current_state = hill_climbing(formula, random_start_state)
        if is_satisfied(formula, current_state):
            return True

        if time.time() - start > 5:
            return False


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
    current_state = np.random.randint(2, size=int(num_variables))
    while 1:

        if is_satisfied(formula, current_state):
            pdb.set_trace()
            return True

        prob = float(np.random.randint(100)) / 100.0

        if prob < 0.3:
            random_bit_index = np.random.randint(current_state.shape[0])
            np.put(current_state, random_bit_index, int(not(current_state[random_bit_index])))
        else:
            # pdb.set_trace()
            current_state = find_min_bit(formula, current_state)

        if time.time() - start > 5:
            return False


# -------------------------------------------------------------------------------


def main():
    num_algs = 3
    num_trials = 10
    difficulties = ["easy/", "hard/"]
    for difficulty in difficulties:
        filenames = os.listdir(difficulty)
        filenames.sort()
        for filename in filenames:
            file_path = difficulty + filename
            file_path = "easy/2.cnf"
            formula = np.genfromtxt(file_path)
            print "Formula -- " + file_path + "--------------------"
            for i in range(num_algs):
                if i == 0:
                    print "     Running the DPLL algorithm..."
                elif i == 1:
                    print "     Running the Local Search algorithm..."
                else:
                    print "     Running the WalkSAT algorithm..."

                for j in range(num_trials):
                    if i == 0:
                        dpll_formula = formula[1:formula[:,0].shape[0],:].copy()
                        satisfiable = dpll(dpll_formula)
                        if satisfiable:
                            print "This is satisfiable"
                        else:
                            print "This is NOT satisfiable"
                    elif i == 1:
                        num_variables = formula[0,2]
                        hill_climbing_formula = formula[1:formula[:,0].shape[0],:].copy()
                        satisfiable = random_restart_hill_climbing(hill_climbing_formula, num_variables)
                        if satisfiable:
                            print "This is satisfiable"
                        else:
                            print "This is NOT satisfiable"
                    elif i == 2:
                        num_variables = formula[0,2]
                        walksat_formula = formula[1:formula[:,0].shape[0],:].copy()
                        satisfiable = walksat(walksat_formula, num_variables)
                        if satisfiable:
                            print "This is satisfiable"
                        else:
                            print "This is NOT satisfiable"

            print "-------------------------------------------------"

main()
