README
Author: Kendall Weihe
Assignment: Satisfiability algorithms -- CS463G Fall 2016

Satisfiability algorithms implemented:
  - Genetic algorithm
  - Hill Climbing algorithm
  - WalkSAT algorithm

Brief description of assignment:
  Select three satisfiability algorithms and develop a program to test them. Use example data found in
    easy/ and hard/ directories. Collect data for the time it took for each algorithm to find a
    solution and the maximum fitness values found. To collect data, run each algorithm through 10
    trials.

---------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------


General pseudocode for Genetic algorithm: (for pseudocode of each function, please see prog3.py)
  - Generate random starting population (I chose a population size of 256)
  - Begin timer & loop
    - Generate random parents (I set the percentage of parents to be 20% of total population)
    - Generate children
    - Mutate randomly chosen children by a single bit
    - Compute fitness of entire population
    - If the number of clauses == a single fitness value: return True
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
-----------------------------------------------------------------------------------------------------------


Graph descriptions:
  Note: each graph is placed to the immediate right of the column for it's respective data.
  Note: I ran two tests -- the first had a timeout of 5 seconds and the second had a timeout of 20 seconds.
          For the second test, I only tested the hard formulas.

  GENETIC ALGORITHM ---------------------------------------------------------------------------------------------

  Column A:
    - This graph shows the time it took for the algorithm to find a solution
    - The timeout was set to 5 seconds
    - The graph covers both hard and easy formulas
    - The algorithm was unable to find any solutions for the hard formulas given a 5 second timeout
    - The average time taken was: 4.1163 seconds

  Column S:
    - This graph shows the maximum fitness values found
    - The timeout was set to 5 seconds
    - The graph covers both hard and easy formulas
    - Note: There exists NaN's for this data -- I am unsure why
    - The average maximum fitness was: (unable to compute due to NaN's)

  Column AL:
    - This graph shows the time it took for the algorithm to find a solution
    - The timeout was increased to 20 seconds
    - The graph only shows values for the hard formulas
    - The average time to solution was: 20.32 seconds

  Column BE:
    - This graph shows the maximum fitness values found
    - The timeout was increased to 20 seconds
    - The graph only shows values for the hard formulas
    - The average maximum fitness value was: 392.366

  ---------------------------------------------------------------------------------------------------------------

  HILL CLIMBING ALGORITHM ---------------------------------------------------------------------------------------

  Column BW:
    - This graph shows the time it took for the algorithm to find a solution
    - The timeout was set to 5 seconds
    - The graph covers both the easy and hard formulas
    - The average time to solution was: 5.3962

  Column CO:
    - This graph shows the maximum fitness found
    - The timeout was set to 5 seconds
    - The graph covers both the easy and hard formulas
    - The average maximum fitness found was: 230.191

  Column DF:
    - This graph shows the time it took for the algorithm to find a solution
    - The timeout was increased to 20 seconds
    - The graph only covers the hard formulas
    - The average time to solution was: 22.1392

  Column DX:
    - This graph shows the maximum fitness found
    - The timeout was increased to 20 seconds
    - The graph only covers the hard formulas
    - The average maximum fitness found was: 412.653

  -----------------------------------------------------------------------------------------------------------------

  WALKSAT ALGORITHM -----------------------------------------------------------------------------------------------

  Column EO:
    - This graph shows the time it took for the algorithm to find a solution
    - The timeout was set to 5 seconds
    - The graph covers both easy and hard formulas
    - The average time to solution was: 2.7616

  Column FG:
    - This graph shows the maximum fitness found
    - The timeout was set to 5 seconds
    - The graph covers both easy and hard formulas
    - The average maximum fitness value was: 233.748

  Column FX:
    - This graph shows the time it took for the algorithm to find a solution
    - The timeout was increased to 20 seconds
    - The graph only covers the hard formulas
    - The average time to solution was: 17.1823

  Column GN:
    - This graph shows the maximum fitness found
    - The timeout was increased to 20 seconds
    - The graph only covers the hard formulas
    - The average maximum fitness found was: 418.858

  ------------------------------------------------------------------------------------------------------------------

  Reflection:
    For the average time to solution, the order of performance from best to worst was WalkSAT, Genetic, Hill Climbing.
    For the average maximum fitness found the order of performance from best to worst was WalkSAT, Hill Climbing, Genetic.

One last note: The Genetic algorithm was written last. By the time I had written the first two algorithms,
  I found cleverer ways to implement the code. Given more time, I would've used those methods in the Hill
  Climbing and WalkSAT algorithms. I apologize for the slight inconsistencies.


------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------


How to run the code:

  Python dependencies (I recommend `pip` installations for UNIX environments):
    - numpy
    - os
    - pdb (if you want to debug, place `pdb.set_trace()` at any line)
    - sys
    - time
    - random

  execute: python prog3.py <timer threshold>
    note: <timer threshold> is an integer value for the timing threshold when the algorithms will terminate

Notes about adjusting code:

  Python is not good at sorting numeric strings, so I generated the list of files so that they
    are executed in order. If you want to use a new directory of files and you don't care about order
    uncomment the lines in the main() function under the line `for difficulty in difficulties:`

    Note about this ^^: the program iterates over the different levels of difficulties. If you want
      to use a new directory, simply add the directory name to the list `difficulties = ["easy/", "hard/"]`

  If you want to collect more data, uncomment the lines located near the bottom of the main() function.
    The code blocks begin with a # TODO comment. I would recommend created new files -- in which case,
    update the filenames in those code blocks.

----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------


What I learned:

  - I learned how to compute fitness values for satisfiability solutions for formulas in CNF
  - I learned what CNF is (conjunctive normal form)
  - I learned the pseudocode for a Genetic algorithm (and how different hyperparameters can be adjusted)
  - I learned the pseudocode for the Hill Climbing algorithm
  - I learned the pseudocode for the WalkSAT algorithm
