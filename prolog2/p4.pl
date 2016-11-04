
global_egg_path(Path).
global_egg_visited(Visited).
global_pika_path(Path).
global_pika_visited(Visited).
global_mb_path(Path).
global_mb_visited(Visited).
global_mt_path(Path).
global_mt_visited(Visited).

maze(X, Y, Maze, Path, Score) :-

  (g_assign(global_egg_visited, [[0,0]]),
  find_egg_and_walk(X, Y, Maze, Path, 0),
  New_score is Score+1,
  g_read(global_egg_path, Egg_path),
  Egg_head = Egg_path,
  nth1(1, Egg_head, Egg_tuple),
  nth1(1, Egg_tuple, X1),
  nth1(2, Egg_tuple, Y1)),

  (g_assign(global_pika_visited, [[0,0]]),
  find_pikachu(X1, Y1, Maze, [X1,Y1], 0),
  g_read(global_pika_path, Pikachu_path),
  Pikachu_head = Pikachu_path,
  nth1(1, Pikachu_head, Pikachu_tuple),
  nth1(1, Pikachu_tuple, X2),
  nth1(2, Pikachu_tuple, Y2)),

  (g_assign(global_mb_visited, [[0,0]]),
  find_mb(X2, Y2, Maze, [X2, Y2], 0),
  g_read(global_mb_path, Mb_path),
  Mb_head = Mb_path,
  nth1(1, Mb_head, Mb_tuple),
  nth1(1, Mb_tuple, X3),
  nth1(2, Mb_tuple, Y3)),

  (g_assign(global_mt_visited, [[0,0]]),
  find_mt(X3, Y3, Maze, [X3, Y3], 0),
  g_read(global_mt_path, Mt_path),
  Mt_head = Mt_path,
  nth1(1, Mt_head, Mt_tuple),
  nth1(1, Mt_tuple, X4),
  nth1(2, Mt_tuple, Y4)),

  write(Mt_head), write(Mb_head), write(Pikachu_head), write(Egg_head).

find_egg_and_walk(X, Y, Maze, Path, Prev_direction) :-

  g_read(global_egg_visited, Visited),
  \+member([X,Y], Visited),
  append([[X, Y]], Visited, New_visited),
  g_assign(global_egg_visited, New_visited),
  (

  (egg_found(X, Y, Maze),
  walk_three_steps(X, Y, Maze, [[X, Y] | Path], Prev_direction, 0));

  ( Prev_direction \= 1,
    LeftX is X-1,
    LeftX > 0,
    is_x_within_bounds(LeftX, Y, Maze),
    is_open(LeftX, Y, Maze),
    find_egg_and_walk(LeftX, Y, Maze, [[LeftX, Y] | Path], 2));

  ( Prev_direction \= 2,
    RightX is X+1,
    is_x_within_bounds(RightX, Y, Maze),
    is_open(RightX, Y, Maze),
    find_egg_and_walk(RightX, Y, Maze, [[RightX, Y] | Path], 1));

  ( Prev_direction \= 3,
    DownY is Y-1,
    DownY > 0,
    is_y_within_bounds(DownY, Maze),
    is_open(X, DownY, Maze),
    find_egg_and_walk(X, DownY, Maze, [[X, DownY] | Path], 4));

  ( Prev_direction \= 4,
    UpY is Y+1,
    UpY > 0,
    is_y_within_bounds(UpY, Maze),
    is_open(X, UpY, Maze),
    find_egg_and_walk(X, UpY, Maze, [[X, UpY] | Path], 3))

  ).

egg_found(X, Y, Maze) :-
  nth1(Y, Maze, Row),
  nth1(X, Row, e).

walk_three_steps(X, Y, Maze, Path, Prev_direction, Num_steps) :-
  Num_steps == 3, g_assign(global_egg_path, Path);

  ( Prev_direction \= 1,
    LeftX is X-1,
    LeftX > 0,
    is_x_within_bounds(LeftX, Y, Maze),
    is_open(LeftX, Y, Maze),
    Num_steps_new is Num_steps+1,
    walk_three_steps(LeftX, Y, Maze, [[LeftX, Y] | Path], 2, Num_steps_new));

  ( Prev_direction \= 2,
    RightX is X+1,
    is_x_within_bounds(RightX, Y, Maze),
    is_open(RightX, Y, Maze),
    Num_steps_new is Num_steps+1,
    walk_three_steps(RightX, Y, Maze, [[RightX, Y] | Path], 1, Num_steps_new));

  ( Prev_direction \= 3,
    DownY is Y-1,
    DownY > 0,
    is_y_within_bounds(DownY, Maze),
    is_open(X, DownY, Maze),
    Num_steps_new is Num_steps+1,
    walk_three_steps(X, DownY, Maze, [[X, DownY] | Path], 4, Num_steps_new));

  ( Prev_direction \= 4,
    UpY is Y+1,
    UpY > 0,
    is_y_within_bounds(UpY, Maze),
    is_open(X, UpY, Maze),
    Num_steps_new is Num_steps+1,
    walk_three_steps(X, UpY, Maze, [[X, UpY] | Path], 3, Num_steps_new)).

find_pikachu(X, Y, Maze, Path, Prev_direction) :-

  g_read(global_pika_visited, Visited),
  \+member([X,Y], Visited),
  append([[X, Y]], Visited, New_visited),
  g_assign(global_pika_visited, New_visited),

  (
  pikachu_found(X, Y, Maze),
  g_assign(global_pika_path, Path);

  ( Prev_direction \= 1,
    LeftX is X-1,
    LeftX > 0,
    is_x_within_bounds(LeftX, Y, Maze),
    is_open(LeftX, Y, Maze),
    find_pikachu(LeftX, Y, Maze, [[LeftX, Y] | Path], 2));

  ( Prev_direction \= 2,
    RightX is X+1,
    is_x_within_bounds(RightX, Y, Maze),
    is_open(RightX, Y, Maze),
    find_pikachu(RightX, Y, Maze, [[RightX, Y] | Path], 1));

  ( Prev_direction \= 3,
    DownY is Y-1,
    DownY > 0,
    is_y_within_bounds(DownY, Maze),
    is_open(X, DownY, Maze),
    find_pikachu(X, DownY, Maze, [[X, DownY] | Path], 4));

  ( Prev_direction \= 4,
    UpY is Y+1,
    is_y_within_bounds(UpY, Maze),
    is_open(X, UpY, Maze),
    find_pikachu(X, UpY, Maze, [[X, UpY] | Path], 3))

  ).

pikachu_found(X, Y, Maze) :-
  nth1(Y, Maze, Row),
  nth1(X, Row, p).

find_mb(X, Y, Maze, Path, Prev_direction) :-

  g_read(global_mb_visited, Visited),
  \+member([X,Y], Visited),
  append([[X, Y]], Visited, New_visited),
  g_assign(global_mb_visited, New_visited),
  (

  mb_found(X, Y, Maze),
  g_assign(global_mb_path, Path);

  ( Prev_direction \= 1,
    LeftX is X-1,
    LeftX > 0,
    is_x_within_bounds(LeftX, Y, Maze),
    is_open(LeftX, Y, Maze),
    find_mb(LeftX, Y, Maze, [[LeftX, Y] | Path], 2));

  ( Prev_direction \= 2,
    RightX is X+1,
    is_x_within_bounds(RightX, Y, Maze),
    is_open(RightX, Y, Maze),
    find_mb(RightX, Y, Maze, [[RightX, Y] | Path], 1));

  ( Prev_direction \= 3,
    DownY is Y-1,
    DownY > 0,
    is_y_within_bounds(DownY, Maze),
    is_open(X, DownY, Maze),
    find_mb(X, DownY, Maze, [[X, DownY] | Path], 4));

  ( Prev_direction \= 4,
    UpY is Y+1,
    is_y_within_bounds(UpY, Maze),
    is_open(X, UpY, Maze),
    find_mb(X, UpY, Maze, [[X, UpY] | Path], 3))

  ).


mb_found(X, Y, Maze) :-
  nth1(Y, Maze, Row),
  nth1(X, Row, mb).


find_mt(X, Y, Maze, Path, Prev_direction) :-

  g_read(global_mt_visited, Visited),
  \+member([X,Y], Visited),
  append([[X, Y]], Visited, New_visited),
  g_assign(global_mt_visited, New_visited),
  (

  %write(X), write(Y),
  mt_found(X, Y, Maze),
  g_assign(global_mt_path, Path);

  ( Prev_direction \= 1,
    LeftX is X-1,
    LeftX > 0,
    is_x_within_bounds(LeftX, Y, Maze),
    is_open(LeftX, Y, Maze),
    find_mt(LeftX, Y, Maze, [[LeftX, Y] | Path], 2));

  ( Prev_direction \= 2,
    RightX is X+1,
    is_x_within_bounds(RightX, Y, Maze),
    is_open(RightX, Y, Maze),
    find_mt(RightX, Y, Maze, [[RightX, Y] | Path], 1));

  ( Prev_direction \= 3,
    DownY is Y-1,
    DownY > 0,
    is_y_within_bounds(DownY, Maze),
    is_open(X, DownY, Maze),
    find_mt(X, DownY, Maze, [[X, DownY] | Path], 4));

  ( Prev_direction \= 4,
    UpY is Y+1,
    is_y_within_bounds(UpY, Maze),
    is_open(X, UpY, Maze),
    find_mt(X, UpY, Maze, [[X, UpY] | Path], 3))

  ).


mt_found(X, Y, Maze) :-
  nth1(Y, Maze, Row),
  nth1(X, Row, mt).

is_x_within_bounds(X, Y, Maze) :-
  nth1(Y, Maze, Row), %predicate always true -- instantiates Row
  length(Row, Size), %predicate always true -- instantiates Size
  X =< Size. %predicate true if X < Size

is_y_within_bounds(Y, Maze) :-
  length(Maze, Size), %predicate always true -- instantiates Size
  Y =< Size. %predicate true if Y < Size

is_open(X, Y, Maze) :-
  nth1(Y, Maze, Row),
  \+ nth1(X, Row, j).
