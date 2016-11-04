

maze(X, Y, Maze, Path, Score) :-
  calculate_num_blocks(Maze, Y, Num_blocks),
  find_eggs_and_pika(X, Y, Maze, Path, Score, 0, 0, 0, Masterball_found, 0, Num_blocks),
  Masterball_found == 1,
  write(Score).

find_eggs_and_pika(X, Y, Maze, Path, Score, PrevDirection, Has_egg, Egg_steps, Masterball_found, Distance_traveled, Num_blocks) :-

  Num_blocks == Distance_traveled;

  is_masterball(X, Y, Maze, Masterball_found);

  eggs_hatched(Has_egg, Egg_steps, Score, Score_new);

  Has_egg == 1,
  increment(Egg_steps, Egg_steps_new);

  Has_egg =\= 1,
  found_egg(X, Y, Maze, Has_egg, New_has_egg);

  var(New_has_egg), write(New_has_egg);

  found_pikachu(X, Y, Maze, Score, Score_new);

  PrevDirection \= 1,
  LeftX is X-1,
  LeftX > 0,
  is_x_within_bounds(LeftX, Y, Maze),
  isOpen(LeftX, Y, Maze),
  New_distance_traveled is Distance_traveled+1,
  find_eggs_and_pika(LeftX, Y, Maze, [(LeftX, Y) | Path], Score_new, 2, New_has_egg, Egg_steps_new, Masterball_found, New_distance_traveled, Num_blocks);

  PrevDirection \= 2,
  RightX is X+1,
  is_x_within_bounds(RightX, Y, Maze),
  isOpen(RightX, Y, Maze),
  New_distance_traveled is Distance_traveled+1,
  write(New_has_egg),
  find_eggs_and_pika(RightX, Y, Maze, [(RightX, Y) | Path], Score_new, 1, New_has_egg, Egg_steps_new, Masterball_found, New_distance_traveled, Num_blocks);


  PrevDirection \= 3,
  DownY is Y-1,
  DownY > 0,
  is_y_within_bounds(DownY, Maze),
  isOpen(X, DownY, Maze),
  New_distance_traveled is Distance_traveled+1,
  find_eggs_and_pika(X, DownY, Maze, [(X, DownY) | Path], 4, Score_new, New_has_egg, Egg_steps_new, Masterball_found, New_distance_traveled, Num_blocks);

  PrevDirection \= 4,
  UpY is Y+1,
  is_y_within_bounds(UpY, Maze),
  isOpen(X, UpY, Maze),
  New_distance_traveled is Distance_traveled+1,
  find_eggs_and_pika(X, UpY, Maze, [(X, UpY) | Path], 3, Score_new, New_has_egg, Egg_steps_new, Masterball_found, New_distance_traveled, Num_blocks).


calculate_num_blocks(Maze, Y, Num_blocks) :-
  nth1(Y, Maze, Row),
  length(Row, Row_size),
  length(Maze, Column_size),
  Num_blocks is Row_size * Column_size.


increment(Score, Score_new) :-
  Score_new is Score+1,
  false.

is_masterball(X, Y, Maze, Masterball_found) :-
  nth1(Y, Maze, Row),
  nth1(X, Row, mb),
  Masterball_found is 1,
  false.

eggs_hatched(Has_egg, Egg_steps, Score, Score_new) :-
  Has_egg == 1,
  Egg_steps == 3,
  increment(Score, Score_new),
  Has_egg is 0,
  Egg_steps is 0,
  false.

found_egg(X, Y, Maze, Has_egg, New_has_egg) :-
  nth1(Y, Maze, Row),
  nth1(X, Row, e),
  New_has_egg is 1.

found_pikachu(X, Y, Maze, Score, Score_new) :-
  nth1(Y, Maze, Row),
  nth1(X, Row, p),
  increment(Score, Score_new),
  false.


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
