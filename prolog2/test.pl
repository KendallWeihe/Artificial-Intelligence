
fact(Path).

main(X,Y,Path) :-
  increment(X,Y,Path,0),
  g_read(fact, T),
  write(T).

increment(X,Y,Path,Count) :-
  Count == 3,
  g_assign(fact,Path);

  NewX is X+1,
  NewY is Y+1,
  NewCount is Count+1,
  increment(NewX,NewY,[(NewX,NewY)|Path],NewCount).
