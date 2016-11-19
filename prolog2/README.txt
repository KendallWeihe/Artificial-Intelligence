Author: Kendall Weihe
Assignment: CS463 Prolog assignment 2
Goal: navigate a city maze, collect pokemon, eggs, and pokeballs (order matters)
Date: November 4th 2016

--------------------------------------------------------------------

How to run:

  - this program MUST be run with gprolog (I use functions unique to gprolog)
  - I run the program like the following example (sorry so many warnings):

      Kendalls-MacBook-Pro:prolog2 kendallweihe$ gprolog
      GNU Prolog 1.4.4 (64 bits)
      Compiled Apr 23 2013, 17:26:17 with /opt/local/bin/gcc-apple-4.2
      By Daniel Diaz
      Copyright (C) 1999-2013 Daniel Diaz
      | ?- consult(prolog2).
      compiling /Users/kendallweihe/Google Drive/Academic/Fall 2016/CS463/prolog2/prolog2.pl for byte code...
      /Users/kendallweihe/Google Drive/Academic/Fall 2016/CS463/prolog2/prolog2.pl:3: warning: singleton variables [Path] for global_egg_path/1
      /Users/kendallweihe/Google Drive/Academic/Fall 2016/CS463/prolog2/prolog2.pl:4: warning: singleton variables [Visited] for global_egg_visited/1
      /Users/kendallweihe/Google Drive/Academic/Fall 2016/CS463/prolog2/prolog2.pl:5: warning: singleton variables [Path] for global_pika_path/1
      /Users/kendallweihe/Google Drive/Academic/Fall 2016/CS463/prolog2/prolog2.pl:6: warning: singleton variables [Visited] for global_pika_visited/1
      /Users/kendallweihe/Google Drive/Academic/Fall 2016/CS463/prolog2/prolog2.pl:7: warning: singleton variables [Path] for global_mb_path/1
      /Users/kendallweihe/Google Drive/Academic/Fall 2016/CS463/prolog2/prolog2.pl:8: warning: singleton variables [Visited] for global_mb_visited/1
      /Users/kendallweihe/Google Drive/Academic/Fall 2016/CS463/prolog2/prolog2.pl:9: warning: singleton variables [Path] for global_mt_path/1
      /Users/kendallweihe/Google Drive/Academic/Fall 2016/CS463/prolog2/prolog2.pl:10: warning: singleton variables [Visited] for global_mt_visited/1
      /Users/kendallweihe/Google Drive/Academic/Fall 2016/CS463/prolog2/prolog2.pl:13-56: warning: singleton variables [Score,X4,Y4] for maze/5
      /Users/kendallweihe/Google Drive/Academic/Fall 2016/CS463/prolog2/prolog2.pl compiled, 296 lines read - 40543 bytes written, 17 ms

      (6 ms) yes
      | ?- maze(1,1,[[ e,  e,  e,  o,  mb], [ o,  j,  o,  o,  o], [ o,  j, mt,  j,  o], [ o,  o,  e, o, o],[ p,  o,  j, o,  p]], Path, 0).
      11[[3,3],[3,2],[4,2],[5,2],[5,3],[5,4],[4,4],[3,4],[2,4],[1,4],[1,3],[1,2],[1,1],[2,1],[3,1],[4,1],5,1][[5,1],[4,1],[3,1],[2,1],[1,1],[1,2],[1,3],[1,4],[2,4],[3,4],[4,4],[4,5],5,5][[5,5],[5,4],[4,4],[3,4],[2,4],[1,4],[1,3],[1,2],[1,1],[2,1],[3,1],4,1][[4,1],[3,1],[2,1],[1,1]|_463]

      true ?

      (1 ms) yes

--------------------------------------------------------------------

The overall maze predicate is defined as follows:
find_and_hatch_egg() AND find_pikachu() AND find_mb() AND find_mt() --> maze()

Each "sub-predicate" (all of the "find" predicates from the above predicate) have the following general design:
[walk_left AND search] OR [walk_right AND search] OR [walk_down AND search] OR [walk_up AND search] --> find*()

find_and_hatch_egg() returns true once the egg has been found and the person has walked three blocks.
find_pikachu() returns true once pikachu is found.
find_mb() returns true once the masterball is found.
find_mt() returns true once mewtwo has been found.
The above predicates happen in the exact order (the masterball must be found before mewtwo).
After each predicate, the ending coordinates from the previous predicate serves as the starting coordinates for the next predicate.

--------------------------------------------------------------------

I store two types of global variables: blocks that have been visited and paths for each of the "sub-predicates" above.
After the maze has completed, I can read the global path and print it to the display.
Also, storing which blocks have been visited for each "sub-predicate" prevents the algorithm from entering infinite recursion.

--------------------------------------------------------------------

The output looks like this (sorry it isn't pretty):
  11[[3,3],[3,2],[4,2],[5,2],[5,3],[5,4],[4,4],[3,4],[2,4],[1,4],[1,3],[1,2],[1,1],[2,1],[3,1],[4,1],5,1][[5,1],[4,1],[3,1],[2,1],[1,1],[1,2],[1,3],[1,4],[2,4],[3,4],[4,4],[4,5],5,5][[5,5],[5,4],[4,4],[3,4],[2,4],[1,4],[1,3],[1,2],[1,1],[2,1],[3,1],4,1][[4,1],[3,1],[2,1],[1,1]|_463]

The "11" at the verying beginning is the score.
The list of list is the path the person took -- in reverse order. There are multiple path lists -- once for each "sub-predicate"

--------------------------------------------------------------------

Throughout the code you will see a lot of code blocks that look like the following:

( Prev_direction \= 1, %walk left
  LeftX is X-1, %subtract index
  LeftX > 0, %make sure new index is not out of bounds in the negative direction
  is_x_within_bounds(LeftX, Y, Maze), %make sure index is not beyond the maximum size of the maze
  is_open(LeftX, Y, Maze), %check if the block is an open block
  find_egg_and_walk(LeftX, Y, Maze, [[LeftX, Y] | Path], 2)); %recursive call the continue searching for eggs

The above code block is declaring the person walks left. I have added comments for every line in this
code block, but all the rest will not contain all comments -- use this for reference.

--------------------------------------------------------------------

Test data:
//from canvas
maze(1,1,[[ e,  e,  e,  o,  o], [ o,  j,  o,  o,  p], [ o,  j, mt,  j,  o], [ o,  o,  e, o, o],[ p,  o,  j, mb,  o]], Path, 0).

//placed pikachu much further away
maze(1,1,[[ e,  e,  e,  o,  o], [ o,  j,  o,  o,  o], [ o,  j, mt,  j,  o], [ o,  o,  e, o, o],[ p,  o,  j, mb,  p]], Path, 0).

//placed masterball further away from pikachu so that the person will have to backtrack
maze(1,1,[[ e,  e,  e,  o,  mb], [ o,  j,  o,  o,  o], [ o,  j, mt,  j,  o], [ o,  o,  e, o, o],[ p,  o,  j, o,  p]], Path, 0).

//unsolvable
maze(1,1,[[ e,  j,  j,  o,  mb], [ j,  j,  o,  o,  o], [ o,  j, mt,  j,  o], [ o,  o,  e, o, o],[ p,  o,  j, o,  p]], Path, 0).

--------------------------------------------------------------------

Notes:
  - this is a very naive implementation -- I think this algorithm could be implemented in much fewer lines of code
  - a lot of the major predicates have overlapping features (walk_left, walk_right, etc.)
    - it would be nice if I could somehow simplify this

--------------------------------------------------------------------

What I learned:
  - prolog does not return values
    - I thought I could instantiate variables in an invoked predicate such that
        when I assigned values to them in the invoked predicate, the value would return to the callee's scope
    - I had to make use of global variables for this reason
  - declarative programming is much different than functional
    - I have a difficult time trying to avoid "functional programming" techniques
  - I learned ways to prevent stack overflows
    - don't visit blocks that have already been visited
