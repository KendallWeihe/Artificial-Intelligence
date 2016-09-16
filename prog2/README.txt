README
Author: Kendall Weihe
CS463G Fall 2016
Programming Assignment #2 -- Solving the Atomic Chaos Puzzle

Requirements:
  - Generate randomized states that can be solved in at least k states
    - k will be tested for values in between 5-20
  - Apply the IDA* Search algorithm to solve the puzzle
  - Use a valid admissible heuristic
  - Graph search outcomes (see details below)

In order to run the program:
  - Python 2.7
  - Python dependencies:
    - numpy
    - heapq
    - itertools
    - subprocess
    - sys

Citations:
  - I used a heuristic provided by Anton [LASTNAME] on the discussion board
  - I used a randomizer also provided by Anton [LASTNAME] on the discussion board
    - Go here for the original code: http://codepen.io/garyyo/pen/mAdjVG

Heuristic:
  I chose to use a heuristic that Anton [LASTNAME] provided to the
    class on the discussion board. There are three parts to the heuristic.

  1. Count the number of rotations the puzzle needs to make in order
      for the correct tubes to be aligned -- a maximum of 3.
  2. Check if the puzzle is in a flat state -- 0 means the puzzle IS in
      a flat state and 1 means the puzzle IS NOT in a flat state
  3. Check if the balls located in the bottom half of the puzzle
      are in the correct tubes -- 0 means all of the balls ARE in the
      correct tube, and 1 means at least some of the balls ARE NOT in the
      correct tube.

  The resulting heuristic value is the sum of all three parts -- a maximum
    of 5.

  This heuristic is admissible since k can be no less than 5. Since the
    three parts of the heuristic (above) sum to 5, the value of h
    can never exceed k. While this heuristic produces correct results,
    I think there are better -- more clever -- heuristics that can
    be applied to the chaos puzzle.

  I built a Multilayered Perceptron (MLP) neural network in an attempt to
    compute an h value that would produce quicker and shallower
    solutions. I hoped that a neural network could compute better
    h values since the entire scope of the puzzle is visible.
    However, typically a neural network is only
    as good as the ground truth fed in, and I used ground truth
    collected by using the above heuristic. The MLP produced
    results consistent with Anton's heuristic.

For description of the program, see `ida_search.py`

Relevant data structures:
  - The puzzle:
      I stored the puzzle in a 6x12 numpy array. In relation to the bottom
      half of the puzzle, index 0 is the red tube, index 1 is the green tube,
      index 2 is the yellow tube, index 3 is the blue tube, index 4 is the
      white tube, and index 5 is the black tube.

      And example (solved) puzzle printed to the terminal looks like the following:

      [[ 12.   3.   4.   7.  11.   2.   0.   0.   0.   0.   0.   0.]
       [ 99.  15.  14.  16.  18.   6.   0.   0.   0.   0.   0.  99.]
       [ 99.  99.  10.  20.  13.   8.   0.   0.   0.   0.  99.  99.]
       [ 99.  99.  99.   9.   5.  17.   0.   0.   0.  99.  99.  99.]
       [ 99.  99.  99.  99.  19.   1.   0.   0.  99.  99.  99.  99.]
       [ 99.  99.  99.  99.  99.  21.   0.  99.  99.  99.  99.  99.]]

      0's are empty spaces
      99's are non existent spaces
      All other values are balls

      Anton's method of randomizing the puzzle assigns numbers to random
      balls -- thus each ball is a different number. In order to verify
      the puzzle is in a solved state, you will have to run Anton's
      randomizer in a browser (locally -- see below).

  - Heap:
    I used Python's heap queue algorithm for my heap structure
      -- documentation here: https://docs.python.org/2/library/heapq.html

    The heap is a list of nodes. Each node is a tuple with the following
      attributes:

        [f, depth, tiebreaker, moves_to_solve, current_state, string_of_previous_states]

        Where:
          f = g(i) + h(i) //cost value + heuristic value
          depth --> depth from root
          tiebreaker --> this is needed because heapq inserts nodes based
                          on a comparison. If there is a tie, the algorithm
                          compares the next elements. Numpy arrays are not easily
                          comparable.
          moves_to_solve --> a list of moves to the current state
                              note: in order to solve, the reverse path is required
          current_state --> what the current puzzle looks like
          string_of_previous_puzzle_states --> a string of puzzle states from
                                                the root to the current state

          note: string_of_previous_puzzle_states was used in the MLP

In order to run the program:
  1. ensure dependencies are installed (example way to test below)
      kendall@kendall-XPS-8500:~/Documents/Development/CS463G/prog2$ python
      Python 2.7.6 (default, Jun 22 2015, 17:58:13)
      [GCC 4.8.2] on linux2
      Type "help", "copyright", "credits" or "license" for more information.
      >>> import numpy
      >>>

  2. At this point you are ready to test the program with 5 randomized puzzles
      that I have already downloaded (see step 4 for details). If you want
      to generate new randomized puzzle states, go to step 4.

  3. In the programs working directory, execute `python main.py`
      This will run 5 IDA* searches with puzzles that I have already randomized.
      The run time for this program is roughly 1.5 minutes.

  4. If you want to test your own randomized states, then do the following steps...

  5.
      kendall@kendall-XPS-8500:~/Documents/Development/CS463G/prog2$ cd antons_randomizer/
      kendall@kendall-XPS-8500:~/Documents/Development/CS463G/prog2/antons_randomizer$ python -m SimpleHTTPServer
      Serving HTTP on 0.0.0.0 port 8000 ...

      Now open browser and go to localhost:8000

  6. Enter k in the text field box, then click "Magic Solve"
      At this point, 5 files will be automatically downloaded.
      You need to move them into the working directory of my
      Python program. These contain the randomized
      puzzle state, and the steps needed to solve.

  7. In the programs working directory, execute
      `python ida_search.py top.csv top_location.csv bottom.csv bottom_location.csv steps.csv`
      If you downloaded multiple randomized puzzles, you may need to adjust the filename arguments

  What is going on here:
    `main.py` is a script with the names of the files for the
      5-already-generated puzzle states. This script calls a subprocess
      that executes `ida_search.py` and passes the file names (just like step 7)
