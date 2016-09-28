import numpy as np
import os
import pdb
import sys
import time
import subprocess
import threading

class SetTimeout(threading.Thread):
    def __init__(self, cmd, timeout):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.timeout = timeout

    def run(self):
        self.p = subprocess.Popen(self.cmd)
        self.p.wait()

    def Run(self):
        self.start()
        self.join(self.timeout)

        if self.is_alive():
            self.p.terminate()      #use self.p.kill() if process needs a kill -9
            print "             The algorithm did not find a satisfiable solution"
            self.join()

def main():
    num_algs = 3
    num_trials = 10
    difficulties = ["easy/", "hard/"]
    for difficulty in difficulties:
        filenames = os.listdir(difficulty)
        filenames.sort()
        for filename in filenames:
            print "Formula -- " + filename + "--------------------"
            file_path = difficulty + filename
            for i in range(num_algs):
                if i == 0:
                    print "     Running the DPLL algorithm..."
                elif i == 1:
                    print "     Running the Local Search algorithm..."
                else:
                    print "     Running the WalkSAT algorithm..."

                for j in range(num_trials):
                    # print "         Trial #" + str(j)
                    if i == 0:
                        pdb.set_trace()
                        start = time.time()
                        subprocess.call(["python", "dpll.py", file_path])
                        print("{:.3f} seconds".format(time.time() - start))
                        pdb.set_trace()
                    elif i == 1:
                        SetTimeout(["python", "hill_climbing.py", file_path], 5).Run()

                    # elif i == 1:
                    #     satisfiable, c = local_search(formula)
                    # else:
                    #     satisfiable, c = walk_sat(formula)

            print "-------------------------------------------------"

main()
