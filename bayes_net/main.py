import numpy as np
import pdb

# import table data
cp_table_A = np.genfromtxt("cp_mb_A.csv", delimiter=",")
cp_table_D = np.genfromtxt("cp_mb_D.csv", delimiter=",")
cp_table_E = np.genfromtxt("cp_mb_E.csv", delimiter=",")
cp_table_F = np.genfromtxt("cp_mb_F.csv", delimiter=",")

# iterate over 5 runs
for i in range(5):

    # initialize random starting states
    nodes = [np.random.randint(2), 0, 1]
    for j in range(3):
        nodes.append(np.random.randint(2))

    a_true_count = 0 # counter for number of times a is true
    ratio_list = [] # list to hold ratios

    # iterate over 10000 iterations
    for j in range(1,10000,1):

        # NODE A
        random_num = float(np.random.randint(100)) / 100 # generate random number
        for k in range(cp_table_A.shape[0]): # iterate over table rows
            if cp_table_A[k,0] == nodes[2] and cp_table_A[k,1] == nodes[3]: # case where the current row reflects the state of the net
                if nodes[0] == 0: # case where A is currently false
                    if random_num > cp_table_A[k,3]:
                        nodes[0] = 1 - nodes[0] # flip the state
                else: # case where A is currently true
                    if random_num > cp_table_A[k,2]:
                        nodes[0] = 1 - nodes[0]

        # NODE D
        random_num = float(np.random.randint(100)) / 100
        for k in range(cp_table_D.shape[0]):
            if cp_table_D[k,0] == nodes[0] and cp_table_D[k,1] == nodes[4] and cp_table_D[k,2] == nodes[5]: # case where the current row reflects the state of the net
                if nodes[3] == 0: # case where D is currently false
                    if random_num > cp_table_D[k,4]:
                        nodes[3] = 1 - nodes[3] # flip the state
                else: # case where D is currently true
                    if random_num > cp_table_D[k,3]:
                        nodes[3] = 1 - nodes[3] # flip the state

        # NODE E
        random_num = float(np.random.randint(100)) / 100
        for k in range(cp_table_E.shape[0]):
            if cp_table_E[k,0] == nodes[1] and cp_table_E[k,1] == nodes[3] and cp_table_E[k,2] == nodes[5]: # case where the current row reflects the state of the net
                if nodes[4] == 0: # case where E is currently false
                    if random_num > cp_table_E[k,4]:
                        nodes[4] = 1 - nodes[4] # flip the state
                else: # case where E is currently true
                    if random_num > cp_table_E[k,3]:
                        nodes[4] = 1 - nodes[4] # flip the state

        # NODE F
        random_num = float(np.random.randint(100)) / 100
        for k in range(cp_table_F.shape[0]):
            if cp_table_F[k,0] == nodes[3] and cp_table_F[k,1] == nodes[4]: # case where the current row reflects the state of the net
                if nodes[5] == 0: # case where F is currently false
                    if random_num > cp_table_F[k,3]:
                        nodes[5] = 1 - nodes[5] # flip the state
                else: # case where F is currently true
                    if random_num > cp_table_F[k,2]:
                        nodes[5] = 1 - nodes[5] # flip the state

        # check if A is currently true
        if nodes[0] == 1:
            a_true_count = a_true_count + 1

        # append the ratio every 40 iterations
        if j % 40 == 0:
            ratio_list.append(float(a_true_count)/float(j))


    # save the ratio list to a CSV file
    filename = "/home/kendall/Documents/Development/CS463G/bayes_net/run_" + str(i) + ".csv"
    np.savetxt(filename, np.array(ratio_list), delimiter="\n")

    # print results
    print "P(A|B = ~b AND C = c) = " + str(np.mean(np.array(ratio_list)))
