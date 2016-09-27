import numpy as np
import os
import pdb
import sys
# sys.setrecursionlimit(100000) # 10000 is an example, try with different values

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
    unit_clauses = find_unit_clauses(phi)
    for unit_clause in unit_clauses:
        delete_these_indices = np.where(phi==unit_clause)[0]
        phi = np.delete(phi, (delete_these_indices), 0)
        np.place(phi,phi == -unit_clause, 0)
        if phi.shape[0] == 0:
            phi = np.array([[0,0,0,0]])

    pure_literals = find_pure_literals(phi)
    for pure_literal in pure_literals:
        delete_these_indices = np.where(phi==pure_literal)[0]
        phi = np.delete(phi, (delete_these_indices), 0)
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
                if current_state[formula[i,j]-1] == 1:
                    variable_correct_count = variable_correct_count + 1
            else:
                if current_state[(-1 * formula[i,j])-1] == 0:
                    variable_correct_count = variable_correct_count + 1
        if variable_correct_count > 0:
            clause_count = clause_count + 1

    return clause_count

def eval_neighbors(current_state, formula):

    neighbors = generate_neighbors(current_state)

    num_clauses_satisfied = []
    for i in range(neighbors[:,0].shape[0]):
        clause_count = 0
        for j in range(formula[:,0].shape[0]):
            # x(i) == index-1
            variable_correct_count = 0
            for k in range(formula[0,:].shape[0]):
                if formula[j,k] > 0:
                    if neighbors[i,formula[j,k]-1] == 1:
                        variable_correct_count = variable_correct_count + 1
                else:
                    if neighbors[i,(-1 * formula[j,k])-1] == 0:
                        variable_correct_count = variable_correct_count + 1
            if variable_correct_count > 0:
                clause_count = clause_count + 1
        num_clauses_satisfied.append(clause_count)

    num_clauses_satisfied = np.array(num_clauses_satisfied)
    index_of_optimal_neighbor = np.argmax(num_clauses_satisfied,axis=0)

    if eval_current_state(current_state, formula) < num_clauses_satisfied[index_of_optimal_neighbor]:
        return neighbors[np.argmax(num_clauses_satisfied,axis=0),:]
    else:
        return -1

def local_search(formula, starting_state):
    #TODO
        # while 1
        #     optimal_neighbor = eval_neighbors(random_start_state, formula)
        #     if optimal_neighbor == -1:
        #         return current state
        #     else:
        #         neighbor is better, keep going
        #         current_state = optimal_neighbor

def hill_climbing(formula):
    #TODO
        # set timer
        # call local_search
        # if return:
        #     evaluate function for satisfiability
            # if satsified: return
            # else: call local_search again with new starting state
        # else:
        #     return -- no satisified solution found

# -------------------------------------------------------------------------------

def main():
    num_algs = 3
    num_trials = 10
    difficulties = ["easy/", "hard/"]
    for difficulty in difficulties:
        filenames = os.listdir(difficulty)
        pdb.set_trace()
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
                    print "         Trial #" + str(j)
                    if i == 0:
                        satisfiable = dpll(formula)
                    # elif i == 1:
                    #     satisfiable, c = local_search(formula)
                    # else:
                    #     satisfiable, c = walk_sat(formula)

                    if satisfiable == True:
                        print "     This formula is satisfiable"
                        print "     Time taken was: "
                    else:
                        print "     The algorithm was unable to find a satisfiable solution"
                        print "     Time taken was: "
            print "-------------------------------------------------"

main()
