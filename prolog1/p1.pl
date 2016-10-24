
solved(X1, Y1, X1, Y1).

citypath([], [], [], [], [], []).

citypath(X1, Y1, X2, Y2, [H| [H2|T]], Path) :-
  solved(X1, Y1, X2, Y2);
  print(X1),
  navigate(X1, Y1, [H| [H2|T]], Path).

navigate(X1, Y1, [H| [H2|T]], Path) :-
  NewX1 is X1+1,
  NewY1 is Y1+1,
  nth0(NewX1, [H| [H2|T]], 0),
  nth0(NewY1, [H| [H2|T]], 0);
  print(NewX1),
  citypath(NewX1, NewY1, X2, Y2, [H2|T], Path).

isOpen(NewX1, NewY1, [H| [H2|T]]) :-
  nth0(NewX1, [H| [H2|T]], 0), nth0(NewY1, [H| [H2|T]], 0).
