
destination_found(X1, Y1, X1, Y1). %fact where the destination has been found -- note X1==X1 && Y1==Y1

citypath(X1, Y1, X2, Y2, Maze, Path) :- %predicate invoked by the tester
  nth0(Y1, Maze, Row), %predicate always true -- instantiates Row
  nth0(X1, Row, 0), %predicate true if the starting position is equal to 0 -- checks if starting at a block == 1
  search(X1, Y1, X2, Y2, Maze, Path, 0). %predicate true if destination is found through recursive calls

search(X1, Y1, X2, Y2, Maze, Path, PrevDirection) :- %predicate that declares search() algorithm
  %test if the destination has been found
  destination_found(X1, Y1, X2, Y2), %predicate true if destination is found
  write(Path); %if here, then previous predicate was true (found), so write the path to output stream and terminate

  %walk to the right a position
  PrevDirection \= 3, %predicate true if next block is not walking backwards -- this is to prevent infinite recursion
  UpX is X1+1, %declare new X (UpX) position
  is_x_within_bounds(UpX, Y1, Maze), %predicate true if UpX is less than the length of the current row
  isOpen(UpX, Y1, Maze), %predicate true if the new block is an open block
  search(UpX, Y1, X2, Y2, Maze, [(UpX, Y1) | Path], 1); %recursive call with new coordinates

  %walk up a position
  PrevDirection \= 4,  %predicate true if next block is not walking backwards -- this is to prevent infinite recursion
  UpY is Y1+1, %declare new X (UpY) position
  is_y_within_bounds(UpY, Maze), %predicate true if UpY is less than the length of the current row
  isOpen(X1, UpY, Maze), %predicate true if the new block is an open block
  search(X1, UpY, X2, Y2, Maze, [(X1,UpY) | Path], 2); %recursive call with new coordinates

  %walk to the left a position
  PrevDirection \= 1,  %predicate true if next block is not walking backwards -- this is to prevent infinite recursion
  DownX is X1-1, %declare new X (DownX) position
  DownX > -1, %predicate true if DownX is less than the length of the current row
  isOpen(DownX, Y1, Maze), %predicate true if the new block is an open block
  search(DownX, Y1, X2, Y2, Maze, [(DownX, Y1) | Path], 3); %recursive call with new coordinates

  %walk down a position
  PrevDirection \= 2,  %predicate true if next block is not walking backwards -- this is to prevent infinite recursion
  DownY is Y1-1, %declare new X (DownY) position
  DownY > -1, %predicate true if DownY is less than the length of the current row
  isOpen(X1, DownY, Maze), %predicate true if the new block is an open block
  search(X1, DownY, X2, Y2, Maze, [(X1,DownY) | Path], 4). %recursive call with new coordinates

is_x_within_bounds(X, Y, Maze) :- %predicate that declares if X is within its row boundary
  nth0(Y, Maze, Row), %predicate always true -- instantiates Row
  length(Row, Size), %predicate always true -- instantiates Size
  X < Size. %predicate true if X < Size

is_y_within_bounds(Y, Maze) :- %predicate that declares if Y is within its column boundary
  length(Maze, Size), %predicate always true -- instantiates Size
  Y < Size. %predicate true if Y < Size

isOpen(NewX1, NewY1, Maze) :- %predicate that declares if new coordinate position is an open block
  nth0(NewY1, Maze, Row), %predicate always true -- instantiates Row
  nth0(NewX1, Row, 0). %predicate true if the NewXth element of Row is 0
