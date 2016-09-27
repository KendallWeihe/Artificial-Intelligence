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
            self.join()

def main():
    num_algs = 3
    num_trials = 10
    difficulties = ["easy/", "hard/"]
    for difficulty in difficulties:
        filenames = os.listdir(difficulty)
        pdb.set_trace()
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
                        subprocess.call(["python", "dpll.py", file_path])
                    elif i == 1:
                        SetTimeout(["python", "hill_climbing.py", file_path], 50).Run()
                        print "this formula was not satisfied"
                    # elif i == 1:
                    #     satisfiable, c = local_search(formula)
                    # else:
                    #     satisfiable, c = walk_sat(formula)

            print "-------------------------------------------------"

main()
