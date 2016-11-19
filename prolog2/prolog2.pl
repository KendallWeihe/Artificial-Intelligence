
%global variables -- paths and blocks already visited
global_egg_path(Path).
global_egg_visited(Visited).
global_pika_path(Path).
global_pika_visited(Visited).
global_mb_path(Path).
global_mb_visited(Visited).
global_mt_path(Path).
global_mt_visited(Visited).

%main predicate
maze(X, Y, Maze, Path, Score) :-

  %find and hatch eggs:
  (g_assign(global_egg_visited, [[0,0]]), %initialize global Visited variable
  find_and_hatch_egg(X, Y, Maze, Path, 0), %find and hatch egg
  Egg_score is 1, %update score
  g_read(global_egg_path, Egg_path), %read the global path variable (assigned in a deeper predicate)
  Egg_head = Egg_path, %assign to local variable
  nth1(1, Egg_head, Egg_tuple), %extract first tuple
  nth1(1, Egg_tuple, X1), %this is the starting X coordinate for finding pikachu
  nth1(2, Egg_tuple, Y1)), %this is the starting Y coordinate for finding pikachu

  %find pikachu
  (g_assign(global_pika_visited, [[0,0]]),
  find_pikachu(X1, Y1, Maze, [X1,Y1], 0), %note that the starting coordinates are where find_and_hatch_egg predicate finished
  Pikachu_score is 10,
  g_read(global_pika_path, Pikachu_path),
  Pikachu_head = Pikachu_path,
  nth1(1, Pikachu_head, Pikachu_tuple),
  nth1(1, Pikachu_tuple, X2),
  nth1(2, Pikachu_tuple, Y2)),

  %find the masterball
  (g_assign(global_mb_visited, [[0,0]]),
  find_mb(X2, Y2, Maze, [X2, Y2], 0),
  g_read(global_mb_path, Mb_path),
  Mb_head = Mb_path,
  nth1(1, Mb_head, Mb_tuple),
  nth1(1, Mb_tuple, X3),
  nth1(2, Mb_tuple, Y3)),

  %find mewtwo
  (g_assign(global_mt_visited, [[0,0]]),
  find_mt(X3, Y3, Maze, [X3, Y3], 0),
  g_read(global_mt_path, Mt_path),
  Mt_head = Mt_path,
  nth1(1, Mt_head, Mt_tuple),
  nth1(1, Mt_tuple, X4),
  nth1(2, Mt_tuple, Y4)),

  %compute and report final score and path to destination
  Final_score is Egg_score+Pikachu_score,
  write(Final_score),
  write(Mt_head), write(Mb_head), write(Pikachu_head), write(Egg_head).

%predicate returns true once an egg has been found and the person has walked three blocks
find_and_hatch_egg(X, Y, Maze, Path, Prev_direction) :-

  g_read(global_egg_visited, Visited), %check if this block has already been visited
  \+member([X,Y], Visited),
  append([[X, Y]], Visited, New_visited),
  g_assign(global_egg_visited, New_visited),
  ( %notice this parenthesis incorporates the remainder of the overall find_and_hatch_egg predicate

  (egg_found(X, Y, Maze), %true if an egg has been found
  walk_three_steps(X, Y, Maze, [[X, Y] | Path], Prev_direction, 0)); %now begin walking three blocks

  ( Prev_direction \= 1, %walk left
    LeftX is X-1, %subtract index
    LeftX > 0, %make sure new index is not out of bounds in the negative direction
    is_x_within_bounds(LeftX, Y, Maze), %make sure index is not beyond the maximum size of the maze
    is_open(LeftX, Y, Maze), %check if the block is an open block
    find_and_hatch_egg(LeftX, Y, Maze, [[LeftX, Y] | Path], 2)); %recursive call the continue searching for eggs

  ( Prev_direction \= 2, %walk right
    RightX is X+1,
    is_x_within_bounds(RightX, Y, Maze),
    is_open(RightX, Y, Maze),
    find_and_hatch_egg(RightX, Y, Maze, [[RightX, Y] | Path], 1));

  ( Prev_direction \= 3, %walk down
    DownY is Y-1,
    DownY > 0,
    is_y_within_bounds(DownY, Maze),
    is_open(X, DownY, Maze),
    find_and_hatch_egg(X, DownY, Maze, [[X, DownY] | Path], 4));

  ( Prev_direction \= 4, %walk up
    UpY is Y+1,
    UpY > 0,
    is_y_within_bounds(UpY, Maze),
    is_open(X, UpY, Maze),
    find_and_hatch_egg(X, UpY, Maze, [[X, UpY] | Path], 3))

  ).

%predicate returns true if the current block contains an egg
egg_found(X, Y, Maze) :-
  nth1(Y, Maze, Row),
  nth1(X, Row, e).

%predicate returns true if the person has walked three blocks -- at this point the person has already found an egg
walk_three_steps(X, Y, Maze, Path, Prev_direction, Num_steps) :-
  Num_steps == 3,
  g_assign(global_egg_path, Path); %assign the path to the egg to the global variable

  ( Prev_direction \= 1, %walk left
    LeftX is X-1,
    LeftX > 0,
    is_x_within_bounds(LeftX, Y, Maze),
    is_open(LeftX, Y, Maze),
    Num_steps_new is Num_steps+1,
    walk_three_steps(LeftX, Y, Maze, [[LeftX, Y] | Path], 2, Num_steps_new));

  ( Prev_direction \= 2, %walk right
    RightX is X+1,
    is_x_within_bounds(RightX, Y, Maze),
    is_open(RightX, Y, Maze),
    Num_steps_new is Num_steps+1,
    walk_three_steps(RightX, Y, Maze, [[RightX, Y] | Path], 1, Num_steps_new));

  ( Prev_direction \= 3, %walk down
    DownY is Y-1,
    DownY > 0,
    is_y_within_bounds(DownY, Maze),
    is_open(X, DownY, Maze),
    Num_steps_new is Num_steps+1,
    walk_three_steps(X, DownY, Maze, [[X, DownY] | Path], 4, Num_steps_new));

  ( Prev_direction \= 4, %walk up
    UpY is Y+1,
    UpY > 0,
    is_y_within_bounds(UpY, Maze),
    is_open(X, UpY, Maze),
    Num_steps_new is Num_steps+1,
    walk_three_steps(X, UpY, Maze, [[X, UpY] | Path], 3, Num_steps_new)).

%predicate returns true if a pikachu is found
find_pikachu(X, Y, Maze, Path, Prev_direction) :-

  %check if the current block has already been visited -- if not, then append the block to the global Visited variable
  g_read(global_pika_visited, Visited),
  \+member([X,Y], Visited),
  append([[X, Y]], Visited, New_visited), %append the current block to global variable
  g_assign(global_pika_visited, New_visited), %update the global variable

  ( %note this parenthesis encapsulates the remainder of the overall find_pikachu predicate
  pikachu_found(X, Y, Maze), %check if pikachu has been found
  g_assign(global_pika_path, Path); %if so, then assign the current path to the global variable

  %begin walking
  ( Prev_direction \= 1, %walk left
    LeftX is X-1,
    LeftX > 0,
    is_x_within_bounds(LeftX, Y, Maze),
    is_open(LeftX, Y, Maze),
    find_pikachu(LeftX, Y, Maze, [[LeftX, Y] | Path], 2));

  ( Prev_direction \= 2, %walk right
    RightX is X+1,
    is_x_within_bounds(RightX, Y, Maze),
    is_open(RightX, Y, Maze),
    find_pikachu(RightX, Y, Maze, [[RightX, Y] | Path], 1));

  ( Prev_direction \= 3, %walk down
    DownY is Y-1,
    DownY > 0,
    is_y_within_bounds(DownY, Maze),
    is_open(X, DownY, Maze),
    find_pikachu(X, DownY, Maze, [[X, DownY] | Path], 4));

  ( Prev_direction \= 4, %walk up
    UpY is Y+1,
    is_y_within_bounds(UpY, Maze),
    is_open(X, UpY, Maze),
    find_pikachu(X, UpY, Maze, [[X, UpY] | Path], 3))

  ).

%predicate returns true if the current block contains a pikachu
pikachu_found(X, Y, Maze) :-
  nth1(Y, Maze, Row),
  nth1(X, Row, p).

%predicate returns true if a masterball has been found
find_mb(X, Y, Maze, Path, Prev_direction) :-

  %check if the current block has already been visited
  g_read(global_mb_visited, Visited),
  \+member([X,Y], Visited),
  append([[X, Y]], Visited, New_visited), %if not, then append to global variable
  g_assign(global_mb_visited, New_visited),

  ( %note this parenthesis encapsulates the remainder of the overall find_mb predicate
  mb_found(X, Y, Maze), %check if masterball is found
  g_assign(global_mb_path, Path); %if so, then assign the path to the global variable

  %begin walking
  ( Prev_direction \= 1, %walk left
    LeftX is X-1,
    LeftX > 0,
    is_x_within_bounds(LeftX, Y, Maze),
    is_open(LeftX, Y, Maze),
    find_mb(LeftX, Y, Maze, [[LeftX, Y] | Path], 2));

  ( Prev_direction \= 2, %walk right
    RightX is X+1,
    is_x_within_bounds(RightX, Y, Maze),
    is_open(RightX, Y, Maze),
    find_mb(RightX, Y, Maze, [[RightX, Y] | Path], 1));

  ( Prev_direction \= 3, %walk down
    DownY is Y-1,
    DownY > 0,
    is_y_within_bounds(DownY, Maze),
    is_open(X, DownY, Maze),
    find_mb(X, DownY, Maze, [[X, DownY] | Path], 4));

  ( Prev_direction \= 4, %walk up
    UpY is Y+1,
    is_y_within_bounds(UpY, Maze),
    is_open(X, UpY, Maze),
    find_mb(X, UpY, Maze, [[X, UpY] | Path], 3))

  ).

%predicate returns true if the current block contains a masterball
mb_found(X, Y, Maze) :-
  nth1(Y, Maze, Row),
  nth1(X, Row, mb).

%predicate returns true if a mewtwo is found
find_mt(X, Y, Maze, Path, Prev_direction) :-

  %check if the current block has already been visited
  g_read(global_mt_visited, Visited),
  \+member([X,Y], Visited),
  append([[X, Y]], Visited, New_visited), %if so, update the global Visited variable
  g_assign(global_mt_visited, New_visited),

  ( %note this parenthesis encapsulates the remainder of the find_mt predicate
  %write(X), write(Y),
  mt_found(X, Y, Maze),
  g_assign(global_mt_path, Path);

  %begin walking
  ( Prev_direction \= 1, %walk left
    LeftX is X-1,
    LeftX > 0,
    is_x_within_bounds(LeftX, Y, Maze),
    is_open(LeftX, Y, Maze),
    find_mt(LeftX, Y, Maze, [[LeftX, Y] | Path], 2));

  ( Prev_direction \= 2, %walk right
    RightX is X+1,
    is_x_within_bounds(RightX, Y, Maze),
    is_open(RightX, Y, Maze),
    find_mt(RightX, Y, Maze, [[RightX, Y] | Path], 1));

  ( Prev_direction \= 3, %walk down
    DownY is Y-1,
    DownY > 0,
    is_y_within_bounds(DownY, Maze),
    is_open(X, DownY, Maze),
    find_mt(X, DownY, Maze, [[X, DownY] | Path], 4));

  ( Prev_direction \= 4, %walk up
    UpY is Y+1,
    is_y_within_bounds(UpY, Maze),
    is_open(X, UpY, Maze),
    find_mt(X, UpY, Maze, [[X, UpY] | Path], 3))

  ).

%predicate returns true if the current block contains a mewtwo
mt_found(X, Y, Maze) :-
  nth1(Y, Maze, Row),
  nth1(X, Row, mt).

%predicate returns true if the current X index is within the Maze boundaries
is_x_within_bounds(X, Y, Maze) :-
  nth1(Y, Maze, Row), %predicate always true -- instantiates Row
  length(Row, Size), %predicate always true -- instantiates Size
  X =< Size. %predicate true if X < Size

%predicate returns true if the current Y index is within the Maze boundaries
is_y_within_bounds(Y, Maze) :-
  length(Maze, Size), %predicate always true -- instantiates Size
  Y =< Size. %predicate true if Y < Size

%predicate returns true if the current block is open
is_open(X, Y, Maze) :-
  nth1(Y, Maze, Row),
  \+ nth1(X, Row, j).
