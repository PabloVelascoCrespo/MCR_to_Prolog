/*********************************************************/
/*                                                       */
/* Checking Relational Constraints                       */
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

% tell('log_ek_pk.txt'),check_pk,told.
% tell('log_ek_fk.txt'),check_fk,told.
% tell('log_mcr_pk.txt'),check_pk,told.
% tell('log_mcr_fk.txt'),check_fk,told.

:- ensure_loaded(pk).
:- ensure_loaded(fk).

% pk(+PredIndicator, +ListOfArgPos)
%   Primary key of PredIndicator as a list of argument 
%    positions ListOfArgPos
%   Argument positions are 1-based

% % Example:
% p(1,a,x).
% p(1,a,y).
% p(1,b,z).

% q(x,1,a).

% % Error, duplicates:
% pk(p/3, [1, 2]).
% pk(p/3, [2]).
% % Ok, No duplicates:
% %  pk(p/3, [3]).

% fk(+FPredIndicator, +ListOfFArgPos, +RPredIndicator, +ListOfRArgPos)
%   Foreign key of FPredIndicator as a list of argument 
%    positions ListOfFArgPos, which must find a correspondence
%    in the primary key ListOfRArgPos of RPredIndicator
% NOTE: Order of arguments in FKs are assumed to be the same in both
%       predicates.

% % Example (Continued):
%
% % Error:
% fk(p/3, [1, 2], q/3, [2, 3]).
% fk(p/3, [3], q/3, [1]).
% % Ok, No duplicates:
% fk(p/3, [1], q/3, [2]).


% check_pk/0
%   Check the primary key constraints as stored in pk/2
check_pk :-
  findall(pk(PredIndicator, ListOfArgPos), pk(PredIndicator, ListOfArgPos), PKs),
  maplist(check_pk, PKs).

% check_pk(+PK)
%   Check the primary key pk(PredIndicator, ListOfArgPos)
check_pk(pk(PredName/Arity, ListOfArgPos)) :-
  format('  Checking ~w...~n', [pk(PredName/Arity, ListOfArgPos)]),
  length(PredArgs, Arity),
  Call =.. [PredName|PredArgs],
  nth1_list(ListOfArgPos, PredArgs, PKArgs),
  group_by(PKArgs, 1, Call, [_, _|_]), % Try to find a duplicate
  findall(Call, Call, Calls),
  format('PK ERROR for ~w: ~w~n', [PredName/Arity, Calls]),
  fail.
check_pk(_) :-
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


% check_fk/0
%   Check the foreign key constraints as stored in fk/4
check_fk :-
  findall(fk(FPredIndicator, ListOfFArgPos, RPredIndicator, ListOfRArgPos), fk(FPredIndicator, ListOfFArgPos, RPredIndicator, ListOfRArgPos), FKs),
  maplist(check_fk, FKs).

% check_fk(+FK)
%   Check the primary key fk(FPredIndicator, ListOfFArgPos, RPredIndicator, ListOfRArgPos)
check_fk(fk(FPredName/FArity, ListOfFArgPos, RPredName/RArity, ListOfRArgPos)) :-
  format('  Checking ~w...~n', [fk(FPredName/FArity, ListOfFArgPos, RPredName/RArity, ListOfRArgPos)]),
  length(ListOfFArgs, FArity),
  FCall =.. [FPredName|ListOfFArgs],
  nth1_list(ListOfFArgPos, ListOfFArgs, Args),
  length(ListOfRArgs, RArity),
  RCall =.. [RPredName|ListOfRArgs],
  nth1_list(ListOfRArgPos, ListOfRArgs, Args),
  FCall,
  (RCall
   -> true
   ;  format('FK ERROR for ~w: ~w~n', [FPredName/FArity, FCall])),
  fail.
check_fk(_FK) :-
  format('    DONE~n'),
  !.


