README
Author: Kendall Weihe
Date: October 25th, 2016
Assignment: CS463G Prolog assignment #1
Purpose: Navigate a maze and find the specified position


How I have ran the code (yours may be different):
  - installed gprolog with Homebrew (Mac)
  - navigated a terminal to the correct directory and executed:
      Kendalls-MacBook-Pro:prolog1 kendallweihe$ gprolog
      GNU Prolog 1.4.4 (64 bits)
      Compiled Apr 23 2013, 17:26:17 with /opt/local/bin/gcc-apple-4.2
      By Daniel Diaz
      Copyright (C) 1999-2013 Daniel Diaz
      | ?- consult(prolog1).
      compiling /Users/kendallweihe/Google Drive/Academic/Fall 2016/CS463/prolog1/prolog1.pl for byte code...
      /Users/kendallweihe/Google Drive/Academic/Fall 2016/CS463/prolog1/prolog1.pl compiled, 51 lines read - 6823 bytes written, 6 ms

      (1 ms) yes
  - execute example test cases (below)
  - note: the path list is printed in reverse order
  - note: I did not implement a maze() predicate -- instead, just pass the list of lists directly as an input to citypath() (see test cases below)

Algorithm:
  In general terms, the search algorithm can be defined by the following predicates:

    destination_found() OR [walk_right() AND search()] OR [walk_down() AND search()]
                  OR [walk_left() AND search()] OR [walk_up() AND search()] --> search()
    search() --> citypath()

  The algorithm will check if the starting position is a blocked block.

  The Maze is represented as a list of lists (see example test cases below).

  The stopping condition for this algorithm is handled by the predicate destination_found(X1, Y1, X1, Y1).
  destination_found() will evaluate to true since variables X1==X1 and Y1==Y1. Once the algorithm has found the
  destination position, then the algorithm will stop and return true.

  The stopping case will be once that algorithm has searched the entire maze -- at that point all predicates will evaluate
  to false.

  My algorithm to find the destination is declared by the predicate search(X1, Y1, X2, Y2, Maze, Path, PrevDirection).
  This algorithm has the same inputs as citypath() with the addition of PrevDirection. PrevDirection was
  introduced to prevent the algorithm from entering infinite recursion. Infinite recursion would happen if the algorithm
  (the "maze walker") walks backwards -- recursion automatically handles "backtracking."

  The first predicate in search() is to test whether the destination has been found -- "destination_found(X1, Y1, X2, Y2),".
  Given that this predicate is false, then the algorithm continues on to the next predicate "PrevDirection \= 3," -- note
  that the algorithm skipped over "write(Path);" because the first predicate (destination_found) evaluated to false.

  Given that the previous direction is equal to 3, then the next predicate "PrevDirection \= 3," will evaluate to false
  (again, this is to prevent walking backwards) and will move onto the next predicate "PrevDirection \= 4,".

  Given that "PrevDirection \= 4," is true, then the algorithm increments the Y index with "UpY is Y1+1,".
  Then, the algorithm will test whether the new Y index is within the Maze boundaries by instantiating the
  predicate "isOpen(X1, UpY, Maze),".

  Given that "isOpen(X1, UpY, Maze)," evaluates to true, then the algorithm makes a recursive call with the
  new coordinates "search(X1, UpY, X2, Y2, Maze, [(X1,UpY) | Path], 2);". Note that each "direction" has
  been given an arbitrary value such that, for example, walking down prevents the algorithm from then walking up.



What I learned:
  - I learned the essential differences between a declarative language and a functional language, although,
      I do wish I knew more of the terminology (i.e. predicate vs function).
  - I learned how to execute mathematical operators in prolog
  - I learned built in prolog functions such as "nth0()" and "length()"
  - I learned that the syntax "x() :- y()." is the mathematical equivalent of y() --> x()


Improvements:
  - This still looks like naive prolog code
  - I am getting warning messages upon `consult(prolog1).`


Some example test cases I ran were:
YES
citypath(1,1,2,2,[[0,0,0],[0,0,0],[0,0,0],[0,0,0]],Path).

YES
citypath(0,0,4,4,[[0,1,1,1,1],[0,1,1,1,1],[0,0,0,1,1],[1,1,0,1,1],[1,1,0,0,0]],Path).

YES
citypath(4,4,0,0,[[0,1,1,1,1],[0,1,1,1,1],[0,0,0,1,1],[1,1,0,1,1],[1,1,0,0,0]],Path).

NO
citypath(0,0,4,4,[[0,1,1,1,1],[0,1,1,1,1],[0,0,0,1,1],[1,1,1,1,1],[1,1,0,0,0]],Path).

NO
citypath(4,4,0,0,[[0,1,1,1,1],[0,1,1,1,1],[0,0,0,1,1],[1,1,1,1,1],[1,1,0,0,0]],Path).

YES
citypath(5,0,0,0,[[0,0,1,1,1,0],[1,0,0,0,1,0],[1,1,1,0,1,0],[1,1,1,0,0,0]],Path).

YES
citypath(0,0,5,0,[[0,0,1,1,1,0],[1,0,0,0,1,0],[1,1,1,0,1,0],[1,1,1,0,0,0]],Path).

YES
citypath(5,0,0,0,[[0,0,1,1,1,0],[1,0,0,0,1,0],[1,1,1,0,1,0],[1,0,0,0,0,0]],Path).

YES
citypath(0,0,1,3,[[0,0,1,1,1,0],[1,0,0,0,1,0],[1,1,1,0,1,0],[1,0,0,0,0,0]],Path).

NO
citypath(0,0,1,3,[[0,0,1,1,1,0],[1,1,0,0,1,0],[1,1,1,0,1,0],[1,0,0,0,0,0]],Path).
