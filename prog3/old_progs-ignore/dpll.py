import numpy as np
import os
import pdb
import sys
import time
import subprocess


# DPLL --------------------------------------------------------------------------

def consistent_set_of_literals(phi):
    explored_literals = []
    # pdb.set_trace()
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
                if explored_literals[len(explored_literals)-1] != 0 and -explored_literals[len(explored_literals)-1] not in phi:
                    pure_literals.append(phi[i,j])
    return np.array(pure_literals)

def dpll(phi):
    if consistent_set_of_literals(phi):
        return True
    if contains_empty_clause(phi):
        return False

    unit_clauses = find_unit_clauses(phi)
    for unit_clause in unit_clauses:
        delete_these_indices = np.where(phi==unit_clause)[0]
        phi = np.delete(phi, (delete_these_indices), 0)
        np.place(phi,phi == -unit_clause, 0)
        # if phi.shape[0] == 0:
        #     phi = np.array([[0,0,0,0]])

    pure_literals = find_pure_literals(phi)
    for pure_literal in pure_literals:
        delete_these_indices = np.where(phi==pure_literal)[0]
        phi = np.delete(phi, (delete_these_indices), 0)
        # if phi.shape[0] == 0:
        #     phi = np.array([[0,0,0,0]])


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

    # pdb.set_trace()
    additional_tuple = np.zeros((phi[0,:].shape[0]))
    additional_tuple[0] = first_literal
    phi_and_first_literal = np.vstack((phi, additional_tuple))
    phi_and_first_literal_not = np.vstack((phi, -additional_tuple))

    return dpll(phi_and_first_literal) or dpll(phi_and_first_literal_not)

# -------------------------------------------------------------------------------

formula = np.genfromtxt(sys.argv[1])
formula = np.genfromtxt("easy/12.cnf")
formula = formula[1:formula[:,0].shape[0],:].copy()
satisfiability = dpll(formula)
if satisfiability:
    print "             This formula was satisfied"
else:
    print "             DPLL did not find a satisfiable solution"
