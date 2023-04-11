/*********************************************************/
/*                                                       */
/* Checking Properties of Binary Relations               */
/*                                                       */
/*   Developed for SWI-Prolog 7.x and above              */
/*                                                       */
/*                             Fernando Saenz-Perez 2023 */
/*                                                       */
/*             Please send comments, questions, etc. to: */
/*                                     fernan@sip.ucm.es */
/*                                                       */
/*                                                       */
/* This is free software: you can redistribute it and/or */
/* modify it under the terms of the GNU Lesser General   */
/* Public License as published by the Free Software      */
/* Foundation, either version 3 of the License, or (at   */
/* your option) any later version.                       */
/*                                                       */
/* This software is distributed in the hope that it will */
/* be useful, but WITHOUT ANY WARRANTY; without even the */
/* implied warranty of MERCHANTABILITY or FITNESS FOR A  */
/* PARTICULAR PURPOSE. See the GNU Lesser General Public */
/* License for more details.                             */
/*                                                       */
/* You should have received a copy of the GNU Lesser     */
/* General Public License and GNU General Public License */
/* along with this program. If not, see:                 */
/*                                                       */
/*            http://www.gnu.org/licenses/               */
/*********************************************************/

:- use_module('c:/WordNet3.0/wn.pl').
% :- discontiguous wordnet:s/6.

:- ensure_loaded(rp).

% tell('log_ek_rp.txt'),check_rp,told.
% tell('log_mcr_rp.txt'),check_rp,told.


% rp(+PredIndicator, +Property, +LeftArgPositions, +RightArgPositions)
%   Property of the binary relation xRy specified for the
%     relation R=PredIndicator, x=LeftArgPositions, y=RightArgPositions
%   A property can be:
%     re: reflexive
%     ir: irreflexive
%     sy: symmetric
%     as: antisymmetric
%     tr: transitive
%     at: antitransitive
%   Argument positions are 1-based

% % % Example:
% p(1,a,b,a,b).
% p(a,b,a,b,c).
% p(1,b,b,a,a).

% % % Error:
% rp(p/5, ir, [2], [3]).
% rp(p/5, as, [2], [3]).
% rp(p/5, at, [1], [2]).
% rp(p/5, tr, [4], [5]).


% check_rp/0
%   Check the relational properties as stored in rp/2
check_rp :-
  % check_re,
  check_ir,
  % check_sy,
  check_as,
  check_tr,
  check_at.

% check_ir
%   Check the irreflexive property
check_ir :-
  findall(rp(PredIndicator, ir, LArgPositions, RArgPositions), rp(PredIndicator, ir, LArgPositions, RArgPositions), IRs),
  maplist(check_ir, IRs).

check_ir(rp(PredName/Arity, ir, LArgPositions, RArgPositions)) :-
  format('  Checking irreflexive property on ~w...~n', [PredName/Arity]),
  length(ListOfArgs, Arity),
  Call =.. [PredName|ListOfArgs],
  nth1_list(LArgPositions, ListOfArgs, Args),
  nth1_list(RArgPositions, ListOfArgs, Args),
  (Call
   -> format('IR ERROR for ~w: ~w~n', [PredName/Arity, Call]),
      fail
   ;  fail).
check_ir(_) :-
  format('    DONE~n'),
  !.

% check_as
%   Check the antisymmetric property
check_as :-
  findall(rp(PredIndicator, as, LArgPositions, RArgPositions), rp(PredIndicator, as, LArgPositions, RArgPositions), ASs),
  maplist(check_as, ASs).

check_as(rp(PredName/Arity, as, LArgPositions, RArgPositions)) :-
  format('  Checking antisymmetric property on ~w...~n', [PredName/Arity]),
  length(ListOfArgs1, Arity),
  Call1 =.. [PredName|ListOfArgs1],
  nth1_list(LArgPositions, ListOfArgs1, LArg),
  nth1_list(RArgPositions, ListOfArgs1, RArg),
  length(ListOfArgs2, Arity),
  Call2 =.. [PredName|ListOfArgs2],
  nth1_list(LArgPositions, ListOfArgs2, RArg),
  nth1_list(RArgPositions, ListOfArgs2, LArg),
  Call1,
  (Call2
   -> format('AS ERROR for ~w: ~w, ~w~n', [PredName/Arity, Call1, Call2]),
      fail
   ;  fail).
check_as(_) :-
  format('    DONE~n'),
  !.


% check_tr
%   Check the transitive property
check_tr :-
  findall(rp(PredIndicator, tr, LArgPositions, RArgPositions), rp(PredIndicator, tr, LArgPositions, RArgPositions), ASs),
  maplist(check_tr, ASs).

check_tr(rp(PredName/Arity, tr, LArgPositions, RArgPositions)) :-
  format('  Checking antitransitive property on ~w...~n', [PredName/Arity]),
  length(ListOfArgs1, Arity),
  Call1 =.. [PredName|ListOfArgs1],
  nth1_list(LArgPositions, ListOfArgs1, XArgs),
  nth1_list(RArgPositions, ListOfArgs1, YArgs),
  length(ListOfArgs2, Arity),
  Call2 =.. [PredName|ListOfArgs2],
  nth1_list(LArgPositions, ListOfArgs2, YArgs),
  nth1_list(RArgPositions, ListOfArgs2, ZArgs),
  length(ListOfArgs3, Arity),
  Call3 =.. [PredName|ListOfArgs3],
  nth1_list(LArgPositions, ListOfArgs3, XArgs),
  nth1_list(RArgPositions, ListOfArgs3, ZArgs),
  Call1,
  Call2,
  XArgs \== ZArgs,
  (Call3
   -> fail
   ;  format('TR ERROR for ~w: ~w, ~w, Missing: ~w~n', [PredName/Arity, Call1, Call2, Call3]),
      fail).
check_tr(_) :-
  format('    DONE~n'),
  !.


% check_at
%   Check the antitransitive property
check_at :-
  findall(rp(PredIndicator, at, LArgPositions, RArgPositions), rp(PredIndicator, at, LArgPositions, RArgPositions), ASs),
  maplist(check_at, ASs).

check_at(rp(PredName/Arity, at, LArgPositions, RArgPositions)) :-
  format('  Checking antitransitive property on ~w...~n', [PredName/Arity]),
  length(ListOfArgs1, Arity),
  Call1 =.. [PredName|ListOfArgs1],
  nth1_list(LArgPositions, ListOfArgs1, XArgs),
  nth1_list(RArgPositions, ListOfArgs1, YArgs),
  length(ListOfArgs2, Arity),
  Call2 =.. [PredName|ListOfArgs2],
  nth1_list(LArgPositions, ListOfArgs2, YArgs),
  nth1_list(RArgPositions, ListOfArgs2, ZArgs),
  length(ListOfArgs3, Arity),
  Call3 =.. [PredName|ListOfArgs3],
  nth1_list(LArgPositions, ListOfArgs3, XArgs),
  nth1_list(RArgPositions, ListOfArgs3, ZArgs),
  Call1,
  Call2,
  (Call3
   -> format('AT ERROR for ~w: ~w, ~w, ~w~n', [PredName/Arity, Call1, Call2, Call3]),
      fail
   ;  fail).
check_at(_) :-
  format('    DONE~n'),
  !.


% nth1_list(+ListOfArgPos, +PredArgs, -PKArgs)
%   Return the actual arguments in PredArgs corresponding
%     to the list of argument positions ListOfArgPos
nth1_list([], _PredArgs, []) :-
  !.
nth1_list([ArgPos|ListOfArgPos], PredArgs, [PKArg|PKArgs]) :-
  nth1(ArgPos, PredArgs, PKArg),
  nth1_list(ListOfArgPos, PredArgs, PKArgs).


