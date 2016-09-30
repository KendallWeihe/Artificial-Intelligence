README
Author: Kendall Weihe
Assignment: Satisfiability algorithms -- CS463G Fall 2016

Satisfiability algorithms implemented:
  - Genetic algorithm
  - Hill Climbing algorithm
  - WalkSAT algorithm

Brief description of assignment:
  All three algorithms include randomness, so data was recorded. For each test file (i.e. easy/1.cnf), then
    for each algorithm, 10 trails were ran. After each trial, the time to completion was recorded as well
    as the maximum fitness value. If the algorithm surpassed the maximum threshold of time, then I recorded
    the formula as "no satisfiable solution was found." If there was a satisfiable solution, then the maximum
    fitness value was equal to the number of clauses. Data was recorded in CSV files, and then accumulated in
    a single spreadsheet -- collected_data.xls.

  [ADD DESCRIPTION OF GRAPHS]

  [ADD PARAMETER TO SET TIMING THRESHOLD]

  [ADD TOTAL TIME TO COMPLETE PROGRAM -- started at 4:40PM THURSDAY]

  One last note: The Genetic algorithm was written last. By the time I had written the first two algorithms,
    I found cleverer ways to implement the code. Given more time, I would've used those methods in the Hill
    Climbing and WalkSAT algorithms. I apologize for the slight inconsistencies.

---------------------------------------------------------------------------------------------------------

General pseudocode for Genetic algorithm: (for pseudocode of each function, please see prog3.py)
  - Generate random starting population (I chose a population size of 256)
  - Begin timer & loop
    - Generate random parents (I set the percentage of parents to be 20% of total population)
    - Generate children
    - Randomly mutate children by a single bit
    - Compute fitness of entire population
    - If the number of clauses == a fitness value: return True
    - Kill individuals with fitness values inversely related to the number of clauses
      - Kill a number of individuals such that the population size remains constant
  - If timer expired: return False

General pseudocode for Hill Climbing algorithm: (for pseudocode of each function, please see prog3.py)
  - Set a timer & loop
    - Generate random start state
    - Begin climbing hill
      - Find all neighbors
      - If there exist a neighbor with a better fitness, then update current state to that neighbor
      - Else, the algorithm has reached a plateau: return current state
    - If current state is satisfiable: return True
  - If timer expired: return False

General pseudocode for WalkSAT algorithm: (for pseudocode of each function, please see prog3.py)
  - Generate random starting state
  - Start timer & loop
    - If current state is satisfied: return True
    - Generate probability p
    - If p < 0.3 (this can be adjusted): randomly flip a single bit
    - Else: find the bit that produces the maximum fitness and update current state
    - Compute fitness
  - If timer expired: return False

-----------------------------------------------------------------------------------------------------------

How to run the code:

  Python dependencies (I recommend `pip` installations for UNIX environments):
    - numpy
    - os
    - pdb (if you want to debug, place `pdb.set_trace()` at any line)
    - sys
    - time
    - random

  execute: python prog3.py <timer threshold>
    note: <timer threshold> is an integer value for the timing threshold whereafter the algorithms will terminate

Notes about adjusting code:

  Python is not good at sorting numeric strings, so I generated the list of files so that they
    are executed in order. If you want to use a new directory of files and you don't care about order
    uncomment the lines in the main() function under the line `for difficulty in difficulties:`

    Note about this ^^: the program iterates over the different levels of difficulties. If you want
      to use a new directory, simply add the directory name to the list `difficulties = ["easy/", "hard/"]`

----------------------------------------------------------------------------------------------------------

What I learned:

  - I learned how to compute fitness values for satisfiability solutions for formulas in CNF
  - I learned what CNF is (conjunctive normal form)
  - I learned the pseudocode for a Genetic algorithm (and how different hyperparameters can be adjusted)
  - I learned the pseudocode for the Hill Climbing algorithm
  - I learned the pseudocode for the WalkSAT algorithm
