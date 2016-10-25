
destination_found(X1, Y1, X1, Y1).

citypath(X1, Y1, X2, Y2, Maze, Path) :-
  destination_found(X1, Y1, X2, Y2),
  write(Path);
  search(X1, Y1, X2, Y2, Maze, Path).

search(X1, Y1, X2, Y2, Maze, Path) :-
  is_x_within_bounds(X1, Maze),
  UpX is X1+1,
  isOpen(UpX, Y1, Maze), citypath(UpX, Y1, X2, Y2, Maze, [(UpX, Y1) | Path]);

  is_y_within_bounds(Y1, Maze),
  UpY is Y1+1,
  isOpen(X1, UpY, Maze), citypath(X1, UpY, X2, Y2, Maze, [(X1,UpY) | Path]);

  X1 > -1,
  DownX is X1-1,
  write(DownX),
  isOpen(DownX, Y1, Maze), citypath(DownX, Y1, X2, Y2, Maze, [(DownX, Y1) | Path]);

  Y1 > -1,
  DownY is Y1-1,
  isOpen(X1, DownY, Maze), citypath(X1, DownY, X2, Y2, Maze, [(X1,DownY) | Path]).

is_x_within_bounds(X, Maze) :-
  nth0(X, Maze, Row),
  length(Row, R),
  X < R.

is_y_within_bounds(Y, Maze) :-
  nth0(Y, Maze, Column),
  length(Column, C),
  Y < C.


isOpen(NewX1, NewY1, Maze) :-
  nth0(NewY1, Maze, Row),
  nth0(NewX1, Row, 0).
