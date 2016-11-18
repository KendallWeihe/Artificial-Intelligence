import numpy as np
import pdb

#TODO
    # open and read files
    # iterate 5 times
    #     randomly initialize non evidence nodes
    #     iterate 10000 times
    #         iterate over each node
    #             randomly generate number between 0 and 100
    #             if value > then flip bit
    #             if a == true: count
    #         if step % 40
    #             append count / step to array
    #     save ratio array to file

cp_table_A = np.genfromtxt("cp_mb_A.csv", delimiter=",")
cp_table_D = np.genfromtxt("cp_mb_D.csv", delimiter=",")
cp_table_E = np.genfromtxt("cp_mb_E.csv", delimiter=",")
cp_table_F = np.genfromtxt("cp_mb_F.csv", delimiter=",")

for i in range(5):
    nodes = [np.random.randint(2), 0, 1]
    for j in range(3):
        nodes.append(np.random.randint(2))

    a_true_count = 0
    ratio_list = []
    for j in range(1,10000,1):

        random_num = float(np.random.randint(100)) / 100
        for k in range(cp_table_A.shape[0]):
            if cp_table_A[k,0] == nodes[2] and cp_table_A[k,1] == nodes[3]:
                if nodes[0] == 0:
                    if random_num > cp_table_A[k,3]:
                        nodes[0] = 1 - nodes[0]
                else:
                    if random_num > cp_table_A[k,2]:
                        nodes[0] = 1 - nodes[0]

        random_num = float(np.random.randint(100)) / 100
        for k in range(cp_table_D.shape[0]):
            if cp_table_D[k,0] == nodes[0] and cp_table_D[k,1] == nodes[4] and cp_table_D[k,2] == nodes[5]:
                if nodes[3] == 0:
                    if random_num > cp_table_D[k,4]:
                        nodes[3] = 1 - nodes[3]
                else:
                    if random_num > cp_table_D[k,3]:
                        nodes[3] = 1 - nodes[3]

        random_num = float(np.random.randint(100)) / 100
        for k in range(cp_table_E.shape[0]):
            if cp_table_E[k,0] == nodes[1] and cp_table_E[k,1] == nodes[3] and cp_table_E[k,2] == nodes[5]:
                if nodes[4] == 0:
                    if random_num > cp_table_E[k,4]:
                        nodes[4] = 1 - nodes[4]
                else:
                    if random_num > cp_table_E[k,3]:
                        nodes[4] = 1 - nodes[4]

        random_num = float(np.random.randint(100)) / 100
        for k in range(cp_table_F.shape[0]):
            if cp_table_F[k,0] == nodes[3] and cp_table_F[k,1] == nodes[4]:
                if nodes[5] == 0:
                    if random_num > cp_table_F[k,3]:
                        nodes[5] = 1 - nodes[5]
                else:
                    if random_num > cp_table_F[k,2]:
                        nodes[5] = 1 - nodes[5]

        if nodes[0] == 1:
            a_true_count = a_true_count + 1

        if j % 40 == 0:
            ratio_list.append(float(a_true_count)/float(j))


    filename = "/home/kendall/Documents/Development/CS463G/bayes_net/run_" + str(i) + ".csv"
    np.savetxt(filename, np.array(ratio_list), delimiter="\n")
