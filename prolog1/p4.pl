
destination_found(X1, Y1, X1, Y1).

citypath(X1, Y1, X2, Y2, Maze, Path) :-
  destination_found(X1, Y1, X2, Y2),
  write(Path);
  search(X1, Y1, X2, Y2, Maze, Path, 0).

search(X1, Y1, X2, Y2, Maze, Path, PrevDirection) :-
  destination_found(X1, Y1, X2, Y2),
  write(Path);

  PrevDirection \= 3,
  UpX is X1+1,
  is_x_within_bounds(UpX, Maze),
  isOpen(UpX, Y1, Maze), search(UpX, Y1, X2, Y2, Maze, [(UpX, Y1) | Path], 1);

  PrevDirection \= 4,
  UpY is Y1+1,
  is_y_within_bounds(UpY, Maze),
  isOpen(X1, UpY, Maze), search(X1, UpY, X2, Y2, Maze, [(X1,UpY) | Path], 2);

  PrevDirection \= 1,
  DownX is X1-1,
  DownX > -1,
  isOpen(DownX, Y1, Maze), search(DownX, Y1, X2, Y2, Maze, [(DownX, Y1) | Path], 3);

  PrevDirection \= 2,
  DownY is Y1-1,
  DownY > -1,
  isOpen(X1, DownY, Maze), search(X1, DownY, X2, Y2, Maze, [(X1,DownY) | Path], 4).

is_x_within_bounds(X, Maze) :-
  nth0(0, Maze, Row),
  length(Row, R),
  X < R.

is_y_within_bounds(Y, Maze) :-
  length(Maze, C),
  Y < C.

isOpen(NewX1, NewY1, Maze) :-
  nth0(NewY1, Maze, Row),
  nth0(NewX1, Row, 0).
