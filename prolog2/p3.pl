
calculate_num_blocks(Maze, Y, Num_blocks) :-
  nth1(Y, Maze, Row),
  length(Row, Row_size),
  length(Maze, Column_size),
  Num_blocks is Row_size * Column_size.

maze(X, Y, Maze, Path, Score) :-
  calculate_num_blocks(Maze, Y, Num_blocks),
  find_eggs_and_pika(X, Y, Maze, Path, Score, 0, 0, 0, 0, Num_blocks),
  write(Score).

find_eggs_and_pika(X, Y, Maze, Path, Score, PrevDirection, Has_egg, Egg_steps, Distance_traveled, Num_blocks) :-
  Num_blocks == Distance_traveled;
  write(Score),
  walk_left(X, Y, Maze, Score, PrevDirection, Has_egg, Has_egg_af_1, Egg_steps, Egg_steps_af_1, Distance_traveled, Distance_traveled_af_1, Num_blocks);
  write(Has_egg),
  walk_right(X, Y, Maze, Score, PrevDirection, Has_egg_af_1, Has_egg_af_2, Egg_steps_af_1, Egg_steps_af_2, Distance_traveled_af_1, Distance_traveled_af_2, Num_blocks);
  walk_down(X, Y, Maze, Score, PrevDirection, Has_egg_af_2, Has_egg_af_3, Egg_steps_af_2, Egg_steps_af_3, Distance_traveled_af_2, Distance_traveled_af_3, Num_blocks);
  walk_up(X, Y, Maze, Score, PrevDirection, Has_egg_af_3, Has_egg_af_4, Egg_steps_af_3, Egg_steps_af_4, Distance_traveled_af_3, Distance_traveled_af_4, Num_blocks).

walk_left(X, Y, Maze, Score, PrevDirection, Has_egg, Has_egg_af_1, Egg_steps, Egg_steps_af_1, Distance_traveled, Distance_traveled_af_1, Num_blocks) :-
  PrevDirection \= 1,
  LeftX is X-1,
  (LeftX > 0; (Has_egg_af_1 is Has_egg, Egg_steps_af_1 is Egg_steps, Distance_traveled_af_1 is Distance_traveled, false)),
  (is_x_within_bounds(LeftX, Y, Maze); (Has_egg_af_1 is Has_egg, Egg_steps_af_1 is Egg_steps, Distance_traveled_af_1 is Distance_traveled, false)),
  (isOpen(LeftX, Y, Maze); (Has_egg_af_1 is Has_egg, Egg_steps_af_1 is Egg_steps, Distance_traveled_af_1 is Distance_traveled, false)),
  (eggs_hatched(Has_egg, Egg_steps, Score, Score_new_1); Score_new_1 is Score),
  (Has_egg == 1, increment(Egg_steps, Egg_steps_new); Egg_steps_new is 0),
  (Has_egg =\= 1, found_egg(LeftX, Y, Maze, New_has_egg); New_has_egg is 0),
  (found_pikachu(LeftX, Y, Maze, Score_new_1, Score_new_2); Score_new_2 is Score_new_1),
  New_distance_traveled is Distance_traveled+1,
  find_eggs_and_pika(LeftX, Y, Maze, [(LeftX, Y) | Path], Score_new_2, 2, New_has_egg, Egg_steps_new, New_distance_traveled, Num_blocks).

walk_right(X, Y, Maze, Score, PrevDirection, Has_egg_af_1, Has_egg_af_2, Egg_steps_af_1, Egg_steps_af_2, Distance_traveled_af_1, Distance_traveled_af_2, Num_blocks) :-
  PrevDirection \= 2,
  RightX is X+1,
  (RightX > 0; (Has_egg_af_2 is Has_egg_af_1, Egg_steps_af_2 is Egg_steps_af_1, Distance_traveled_af_2 is Distance_traveled_af_1, false)),
  (is_x_within_bounds(RightX, Y, Maze); (Has_egg_af_2 is Has_egg_af_1, Egg_steps_af_2 is Egg_steps_af_1, Distance_traveled_af_2 is Distance_traveled_af_1, false)),
  (isOpen(RightX, Y, Maze); (Has_egg_af_2 is Has_egg_af_1, Egg_steps_af_2 is Egg_steps_af_1, Distance_traveled_af_2 is Distance_traveled_af_1, false)),
  (eggs_hatched(Has_egg_af_1, Egg_steps_af_1, Score, Score_new_1); Score_new_1 is Score),
  (Has_egg_af_1 == 1, increment(Egg_steps_af_1, Egg_steps_new); Egg_steps_new is 0),
  (Has_egg_af_1 =\= 1, found_egg(RightX, Y, Maze, New_has_egg); New_has_egg is 0),
  (found_pikachu(RightX, Y, Maze, Score_new_1, Score_new_2); Score_new_2 is Score_new_1),
  New_distance_traveled is Distance_traveled_af_1+1,
  find_eggs_and_pika(RightX, Y, Maze, [(RightX, Y) | Path], Score_new_2, 1, New_has_egg, Egg_steps_new, New_distance_traveled, Num_blocks).

walk_down(X, Y, Maze, Score, PrevDirection, Has_egg_af_2, Has_egg_af_3, Egg_steps_af_2, Egg_steps_af_3, Distance_traveled_af_2, Distance_traveled_af_3, Num_blocks) :-
  PrevDirection \= 3,
  DownY is Y-1,
  (DownY > 0; (Has_egg_af_3 is Has_egg_af_2, Egg_steps_af_3 is Egg_steps_af_2, Distance_traveled_af_3 is Distance_traveled_af_2, false)),
  (is_y_within_bounds(DownY, Maze); (Has_egg_af_3 is Has_egg_af_2, Egg_steps_af_3 is Egg_steps_af_2, Distance_traveled_af_3 is Distance_traveled_af_2, false)),
  (isOpen(X, DownY, Maze); (Has_egg_af_3 is Has_egg_af_2, Egg_steps_af_3 is Egg_steps_af_2, Distance_traveled_af_3 is Distance_traveled_af_2, false)),
  (eggs_hatched(Has_egg_af_2, Egg_steps_af_2, Score, Score_new_1); Score_new_1 is Score),
  (Has_egg_af_2 == 1, increment(Egg_steps_af_2, Egg_steps_new); Egg_steps_new is 0),
  (Has_egg_af_2 =\= 1, found_egg(X, DownY, Maze, New_has_egg); New_has_egg is 0),
  (found_pikachu(X, DownY, Maze, Score_new_1, Score_new_2); Score_new_2 is Score_new_1),
  New_distance_traveled is Distance_traveled_af_2+1,
  find_eggs_and_pika(X, DownY, Maze, [(X, DownY) | Path], 4, Score_new_2, New_has_egg, Egg_steps_new, New_distance_traveled, Num_blocks).

walk_up(X, Y, Maze, Score, PrevDirection, Has_egg_af_3, Has_egg_af_4, Egg_steps_af_3, Egg_steps_af_4, Distance_traveled_af_3, Distance_traveled_af_4, Num_blocks) :-
  PrevDirection \= 4,
  (UpY is Y+1; (Has_egg_af_4 is Has_egg_af_3, Egg_steps_af_4 is Egg_steps_af_3, Distance_traveled_af_4 is Distance_traveled_af_3, false)),
  (is_y_within_bounds(UpY, Maze); (Has_egg_af_4 is Has_egg_af_3, Egg_steps_af_4 is Egg_steps_af_3, Distance_traveled_af_4 is Distance_traveled_af_3, false)),
  (isOpen(X, UpY, Maze); (Has_egg_af_4 is Has_egg_af_3, Egg_steps_af_4 is Egg_steps_af_3, Distance_traveled_af_4 is Distance_traveled_af_3, false)),
  (eggs_hatched(Has_egg_af_3, Egg_steps_af_3, Score, Score_new_1); Score_new_1 is Score),
  (Has_egg_af_3 == 1, increment(Egg_steps_af_3, Egg_steps_new); Egg_steps_new is 0),
  (Has_egg_af_3 =\= 1, found_egg(X, UpY, Maze, New_has_egg); New_has_egg is 0),
  (found_pikachu(X, UpY, Maze, Score_new_1, Score_new_2); Score_new_2 is Score_new_1),
  New_distance_traveled is Distance_traveled_af_3+1,
  find_eggs_and_pika(X, UpY, Maze, [(X, UpY) | Path], 3, Score_new_2, New_has_egg, Egg_steps_new, New_distance_traveled, Num_blocks).


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
  Egg_steps is 0.

found_egg(X, Y, Maze, New_has_egg) :-
  nth1(Y, Maze, Row),
  nth1(X, Row, e),
  New_has_egg is 1.

found_pikachu(X, Y, Maze, Score, Score_new) :-
  nth1(Y, Maze, Row),
  nth1(X, Row, p),
  increment(Score, Score_new).


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
