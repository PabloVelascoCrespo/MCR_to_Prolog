%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% WN_CONNECT source v1.4 : wn_fuzzy_predicates module
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
/*
AUTHORS: Pascual Julián-Iranzo (Universidad de Castilla-La Mancha, Spain)
Fernando Sáenz-Pérez  (Universidad Complutense de Madrid, Spain)

WN_CONNECT is licensed for research and educational purposes only and it is
distributed with NO WARRANTY OF ANY KIND. You are freely allowed to use, copy
and distribute WN_CONNECT provided that you make no modifications to any of its
files and give credit to its original authors.
*******************************************************************************/


:- module(wn_fuzzy_predicates, [
    none_wn_path/5, %%(+Word1, +Word2, +ConstraintsIn, -ConstraintsOut, -Degree)
    none_wn_wup/5,  %%(+Word1, +Word2, +ConstraintsIn, -ConstraintsOut, -Degree)
    none_wn_lch/5,  %%(+Word1, +Word2, +ConstraintsIn, -ConstraintsOut, -Degree)
    none_wn_res/5,  %%(+Word1, +Word2, +ConstraintsIn, -ConstraintsOut, -Degree)
    none_wn_jcn/5,  %%(+Word1, +Word2, +ConstraintsIn, -ConstraintsOut, -Degree)
    none_wn_lin/5,  %%(+Word1, +Word2, +ConstraintsIn, -ConstraintsOut, -Degree)		
    none_wn_yarm/5  %%(+Word1, +Word2, +ConstraintsIn, -ConstraintsOut, -Degree)		
   ]).

:- use_module(wn_sim_measures).
:- use_module(wn_ic_measures).
:- use_module(wn_rel_measures).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Automatic compilations for each fuzzy predicate

none_wn_path(_20496,_20502,Ci,Co,Deg):-evaluator:unify_arguments_a3([[_20496,_19626,Ci,_20562,_20508],[_20502,_19632,_20562,Co,_20514]]),wn_path(_19626,_19632,D),evaluator:degree_composition([D,_20508,_20514],Deg).

none_wn_wup(_21672,_21678,Ci,Co,Deg):-evaluator:unify_arguments_a3([[_21672,_20808,Ci,_21738,_21684],[_21678,_20814,_21738,Co,_21690]]),wn_wup(_20808,_20814,D),evaluator:degree_composition([D,_21684,_21690],Deg).

none_wn_lch(_22848,_22854,Ci,Co,Deg):-evaluator:unify_arguments_a3([[_22848,_21984,Ci,_22914,_22860],[_22854,_21990,_22914,Co,_22866]]),wn_lch(_21984,_21990,D),evaluator:degree_composition([D,_22860,_22866],Deg).

none_wn_res(_24024,_24030,Ci,Co,Deg):-evaluator:unify_arguments_a3([[_24024,_23160,Ci,_24090,_24036],[_24030,_23166,_24090,Co,_24042]]),wn_res(_23160,_23166,D),evaluator:degree_composition([D,_24036,_24042],Deg).

none_wn_jcn(_25200,_25206,Ci,Co,Deg):-evaluator:unify_arguments_a3([[_25200,_24336,Ci,_25266,_25212],[_25206,_24342,_25266,Co,_25218]]),wn_jcn(_24336,_24342,D),evaluator:degree_composition([D,_25212,_25218],Deg).

none_wn_lin(_26376,_26382,Ci,Co,Deg):-evaluator:unify_arguments_a3([[_26376,_25512,Ci,_26442,_26388],[_26382,_25518,_26442,Co,_26394]]),wn_lin(_25512,_25518,D),evaluator:degree_composition([D,_26388,_26394],Deg).

none_wn_yarm(_26376,_26382,Ci,Co,Deg):-evaluator:unify_arguments_a3([[_26376,_25512,Ci,_26442,_26388],[_26382,_25518,_26442,Co,_26394]]),wn_yarm(_25512,_25518,D),evaluator:degree_composition([D,_26388,_26394],Deg).
