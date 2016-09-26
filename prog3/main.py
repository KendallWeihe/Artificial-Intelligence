import numpy as np
import os
import pdb
import sys
sys.setrecursionlimit(100000) # 10000 is an example, try with different values

#TODO
    # DPLL alg:
    #     call function to check if phi is a consistent set of literals (all pure literals)
    #     call function to check if phi contains an empty set
    #     for every unit clause l
    #         set l to true
    #         remove all clauses that contain l
    #     for every pure literal
    #         set l to true
    #         remove l from all clauses
    #     l' <-- select first literal from phi
    #     return dpll(phi & l) || dpll(phi & !l)

def consistent_set_of_literals(phi):
    explored_literals = []
    for i in range(phi[:,0].shape[0]):
        for j in range(phi[0,:].shape[0]):
            if phi[i,j] not in explored_literals:
                explored_literals.append(phi[i,j])
                if -explored_literals[len(explored_literals)-1] in phi:
                    return False
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
            else:
                if -explored_literals[len(explored_literals)-1] not in phi:
                    pure_literals.append(phi[i,j])
    return np.array(pure_literals)


explored_vars = []
def dpll(phi):
    if consistent_set_of_literals(phi):
        return True
    if contains_empty_clause(phi):
        return False
    unit_clauses = find_unit_clauses(phi)
    for unit_clause in unit_clauses:
        # set unit_clause to true
        delete_these_indices = np.where(phi==unit_clause)[0]
        phi = np.delete(phi, (delete_these_indices), 0)

    pure_literals = find_pure_literals(phi)
    for pure_literal in pure_literals:
        # np.place(phi, phi==pure_literal, 1)
        delete_these_indices = np.where(phi==pure_literal)[0]
        phi = np.delete(phi, (delete_these_indices), 0)

    if phi.shape[0] == 0:
        return False

    first_literal = None
    for i in range(phi[:,0].shape[0]):
        temp_clause = phi[i,:].copy()
        temp_clause = temp_clause[temp_clause != 0]
        for j in range(temp_clause.shape[0]):
            if temp_clause[j] not in explored_vars:
                first_literal = temp_clause[j]

    if first_literal == None:
        return False

    additional_tuple = np.zeros((phi[0,:].shape[0]))
    additional_tuple[0] = first_literal
    phi_and_first_literal = np.vstack((phi, additional_tuple))
    phi_and_first_literal_not = np.vstack((phi, -additional_tuple))
    explored_vars.append(first_literal)
    explored_vars.append(-first_literal)

    return dpll(phi_and_first_literal) or dpll(phi_and_first_literal_not)

def main():
    # iterate over easy and hard
    #     read in filenames
    num_algs = 3
    num_trials = 10
    difficulties = ["easy/", "hard/"]
    for difficulty in difficulties:
        filenames = os.listdir(difficulty)
        for filename in filenames:
            print "Formula -- " + filename + "--------------------"
            formula = np.genfromtxt(difficulty + filename)
            formula = formula[1:formula[:,0].shape[0],:].copy()
            for i in range(num_algs):
                if i == 0:
                    print "     Running the DPLL algorithm..."
                elif i == 1:
                    print "     Running the Local Search algorithm..."
                else:
                    print "     Running the WalkSAT algorithm..."

                for j in range(num_trials):
                    print "Trial #" + str(j)
                    if i == 0:
                        if filename == "3.cnf":
                            pdb.set_trace()
                        satisfiable = dpll(formula)
                    # elif i == 1:
                    #     satisfiable, c = local_search(formula)
                    # else:
                    #     satisfiable, c = walk_sat(formula)

                    if satisfiable == True:
                        print "This formula is satisfiable"
                        print "Time taken was: "
                    else:
                        print "The algorithm was unable to find a satisfiable solution"
                        print "Time taken was: "
            print "-------------------------------------------------"

main()
