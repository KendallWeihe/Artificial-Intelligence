
:- dynamic(test/1).

main(X,Y,Path) :-
  test(X,Y,Path,0),
  write(test).

test(X,Y,Path,Count) :-
  Count == 4,
  assertz(test(Path));

  T is Count+1,
  NewX is X+1,
  NewY is Y+1,
  test(NewX,NewY,[(X,Y) | Path],T).
