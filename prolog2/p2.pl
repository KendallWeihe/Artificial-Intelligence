

maze(X, Y, Maze, Path, Score) :-
  find_eggs_and_pika(X, Y, Maze, Path, Score, 0),
  write(Score).

find_eggs_and_pika(X, Y, Maze, Path, Score, PrevDirection) :-

  increment(Score, Score_new);

  PrevDirection \= 1,
  LeftX is X-1,
  is_x_within_bounds(LeftX, Y, Maze),
  isOpen(LeftX, Y, Maze),
  find_eggs_and_pika(LeftX, Y, Maze, [(LeftX, Y) | Path], Score_new, 2);

  PrevDirection \= 2,
  RightX is X+1,
  is_x_within_bounds(RightX, Y, Maze),
  isOpen(RightX, Y, Maze),
  find_eggs_and_pika(RightX, Y, Maze, [(RightX, Y) | Path], Score_new, 1);

  PrevDirection \= 3,
  DownY is Y-1,
  is_y_within_bounds(DownY, Maze),
  isOpen(X, DownY, Maze),
  find_eggs_and_pika(X, DownY, Maze, [(X, DownY) | Path], Score_new, 4);

  PrevDirection \= 4,
  UpY is Y+1,
  is_y_within_bounds(UpY, Maze),
  isOpen(X, UpY, Maze),
  find_eggs_and_pika(X, UpY, Maze, [(X, UpY) | Path], Score_new, 3).

increment(Score, Score_new) :-
  Score_new is Score+1.

is_x_within_bounds(X, Y, Maze) :-
  nth1(Y, Maze, Row), %predicate always true -- instantiates Row
  length(Row, Size), %predicate always true -- instantiates Size
  X < Size. %predicate true if X < Size

is_y_within_bounds(Y, Maze) :-
  length(Maze, Size), %predicate always true -- instantiates Size
  Y < Size. %predicate true if Y < Size

isOpen(X, Y, Maze) :-
  nth1(Y, Maze, Row),
  \+ nth1(X, Row, j).
