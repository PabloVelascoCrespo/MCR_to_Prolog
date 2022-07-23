%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% WN_CONNECT source v1.4 : wn_entailments module
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
/*
AUTHORS: Pascual Julián-Iranzo (Universidad de Castilla-La Mancha, Spain)
Fernando Sáenz-Pérez  (Universidad Complutense de Madrid, Spain)

WN_CONNECT is licensed for research and educational purposes only and it is
distributed with NO WARRANTY OF ANY KIND. You are freely allowed to use, copy
and distribute WN_CONNECT provided that you make no modifications to any of its
files and give credit to its original authors.
*******************************************************************************/


:- module(wn_entailments, [
        %%wn_entails/2, %% (+W_Verb, -Entailed_SynSet)
		wn_entailments_of/2, %% (+W_Verb, -List_Entailed_SynSets)
        wn_entailments_of/3, %% (+W_Verb, +Verbosity, -List_Entailed_SynSets)
        wn_display_entailments_of/1, %% (+W_Verb)
        wn_display_graph_entailments_of/1 %% (+W_Verb)
   ]).


:- use_module(wn_synsets).
:- use_module(wn_utilities).

/*******************************************************************************
The predicates defined in this module only works with verbs. They mainly define
entailment relations and causal relations between verbs. The reason is because WordNet
only cover entaiment and causal relations for verbs (and not other parts of speech).

** ENTAILMENT:

The notion of linguistic entailment has been introduced for text statements:

"For an entailment to be true, the then statement (denoted as B) must always be true
when the if statement (denoted as A) is true. To judge whether an entailment is true,
one can ask, "Could it ever be the case that B isn't true while A is true?" In order
to accurately recognize entailments, a strong knowledge of the denotation of the word
is required.[Murphy, M. Lynne (2010). Lexical Meaning. Cambridge: Cambridge Textbooks
in Semantics.]"

Textual entailment is a directional relation between two texts fragments, a text t and
a textual statement (hypothesis) h. We say that t entails h, denoted t => h, if humans
reading t will infer that h is most likely true (Dagan et al., 2005). As opposed to the
linguistic definition of entailment, which requires that h will be true in every circumstance
(possible world) in which t is true, this applied definition is based on human judgment and
only requires that entailment will most likely hold.
[Eyal Shnarch "LEXICAL ENTAILMENT AND ITS EXTRACTION FROM WIKIPEDIA" Master Thesis (Advisor:
Ido Dagan)]

In logic, entailment, or strict implication, is properly defined for propositions; a proposition
P entails a proposition Q if and only if there is no conceivable state of affairs that could
make P true and Q false. Entailment is a semantic relation because it involves reference to the
states of affairs that P and Q represent. The term will be generalized here to refer to the
relation between two verbs V1 and V2 that holds when the sentence Someone V1 logically entails
the sentence Someone V2; this use of entailment can be called lexical entailment. Thus, for example,
snore lexically entails sleep because the sentence He is snoring entails He is sleeping; the second
sentence necessarily holds if the the first one does.
Lexical entailment is a unilateral relation: if a verb V1 entails another verb V2, then it cannot
be that case that V2 entails V1. The exception is that where two verbs can be said to be mutually
entailing, they must also be synonyms, that is, they must have the same sense.
["English Verbs as a Semantic Net"  Christiane Fellbaum]

*******************************************************************************/


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% wn_entailments_of(+W_Verb, -List_Entailed_SynSets)
%%% Given a word (term) "W_Verb" returns the list "List_Entailed_SynSets" of its
%%% entailed synset_IDs
%%%
%%% OBSERVATIONS:
%%% 1) The synset_ID "SS_ID_0" of the word "W_Verb" is part of the entailment List "List_Entailed_SynSets"
%%% 2) If "List_Entailed_SynSets"=[SS_ID_N, SS_ID_{N-1}, ..., SS_ID_1, SS_ID_0], SS_ID_0 entails SS_ID_1
%%% which entails ... SS_ID_{N-1} which entails SS_ID_N.
%%% 3) Entailment is a transitive relation, but not symmetric: to win entails to compite,
%%%    but to compite doesn't entail to win.
%%%
%%% EXAMPLE:
%%% ?- wn_entailments_of(snore,L).
%%% L = [200014742 (WN: sleep, kip, slumber, log Z's, catch some Z's),
%%%      200017031 (WN: snore, saw wood, saw logs)]
%%%
%%% Snore entails sleep (or, in other words, sleep is an entailment of snore).

wn_entailments_of(W_Verb, List_Entailed_SynSets):- wn_entailments_of(W_Verb, verbose(no), List_Entailed_SynSets).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% wn_entailments_of(+W_Verb, +Verbosity, -List_Entailed_SynSets)
%%% Given a word (term) "W_Verb" returns the list "List_Entailed_SynSets" of its
%%% entailed synset_IDs
%%%
%%% The word "W_Verb" is a term with the following syntax:
%%%                      Word[:SS_type[:Sense_num]]
%%% Where ss_type = v (VERB)
%%
%%% and "Sense_num" specifies the sense number (meaning) of the word, within the part of
%%% speech encoded in the synset_id. "Sense_num" is a natural number: 1, 2, 3, ...

wn_entailments_of(Word:SS_type:Sense_num, Verbosity, List_Entailed_SynSets) :-
        !,
        wordnet:wn_s(SynSet_ID, _, Word, SS_type, Sense_num, _),
        ((SS_type=v) ->
                entailment_chain(SynSet_ID, List_Entailed_SynSets)
                ;
                (Verbosity = verbose(yes) ->
                    write(">>>> "), write(Word:SS_type:Sense_num), nl,
                    wordnet:wn_g(SynSet_ID, Glos),
                    write(Glos), nl,
                    write("The entailment relation only applies to verbs"),
                    nl),
                fail
        ).

wn_entailments_of(Word:SS_type, Verbosity, List_Entailed_SynSets) :-
        !,
        wordnet:wn_s(SynSet_ID, _, Word, SS_type, _, _),
        ((SS_type=v) ->
            entailment_chain(SynSet_ID, List_Entailed_SynSets)
            ;
            (Verbosity = verbose(yes) ->
                write(">>>> "), write(Word:SS_type), nl,
                wordnet:wn_g(SynSet_ID, Glos),
                write(Glos), nl,
                write("The entailment relation only applies to verbs"),
                nl),
            fail
        ).

wn_entailments_of(Word, Verbosity, List_Entailed_SynSets) :-
        wordnet:wn_s(SynSet_ID, _, Word, SS_type, Sense_num, _),
        ((SS_type=v) ->
            entailment_chain(SynSet_ID, List_Entailed_SynSets)
            ;
            (Verbosity = verbose(yes) ->
            write(">>>> "), write(Word:SS_type:Sense_num), nl,
            wordnet:wn_g(SynSet_ID, Glos),
            write(Glos), nl,
            write("The entailment relation only applies to verbs"),
            nl),
            fail
        ).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% entailment_chain(+SynSet_Verb, -List_Entailed_SynSets)
%%% Given a synset_ID "SynSet_Verb" returns the list "List_Entailed_SynSets" of its
%%% entailed synset_IDs
%%%
%%% OBSERVATION: We choose to store the synset_ID  "SynSet_Verb" as part of the entailment
%%% List "List_Entailed_SynSets"
%%%
entailment_chain(SynSet_Verb, List_Entailed_SynSets):-
    entailment_chain(SynSet_Verb, [SynSet_Verb], L_Entailed_SynSets),
    reverse(L_Entailed_SynSets, List_Entailed_SynSets).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% entailment_chain(+SynSet_Verb, +List_Entailed_SynSets_Acc, -List_Entailed_SynSets)
%%%
entailment_chain(SS_Verb, List_Entailed_SS_Acc, List_Entailed_SS) :-
    (wordnet:wn_ent(SS_Verb, SS_entailment),
    entailment_chain(SS_entailment, [SS_entailment|List_Entailed_SS_Acc], List_Entailed_SS)
    ;
    \+(wordnet:wn_ent(SS_Verb, _SS_entailment)),
    List_Entailed_SS = List_Entailed_SS_Acc
    ).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%  TEXTUAL REPRESENTATION OF entailment CHAINS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% wn_display_entailments_of(+W_Verb)
%%% Given a word (term) "W_Verb" prints a textual representation of the chain of its
%%% entailment synsets
%%%
%%% The word "W_Verb" is a term with the following syntax:
%%%                      Word[:SS_type[:Sense_num]]
%%% as explained in the predicate wn_entailments_of/2
%%%
wn_display_entailments_of(W_Verb) :-
        wn_entailments_of(W_Verb, List_Entailed_SynSets),
        display_entailed_list(List_Entailed_SynSets).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% display_entailed_list(+List_Entailed_SynSets)
%%%
display_entailed_list([]).
display_entailed_list([SynSet_ID|List_SynSet_IDs]):-
        wn_synsets:wn_synset_components(SynSet_ID, Synset_Words),
        write(Synset_Words), nl,
        write(' >> '),
        display_entailed_list(List_SynSet_IDs).



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%  GRAPHICAL REPRESENTATION OF entailment CHAINS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% wn_display_graph_entailments_of(+Word)
%%% It shows a graphic representation of all entailments corresponding to all the senses
%%% of the word 'Word'.
%%%
%%% A node of the graph only shows the representative word of that entailed synset (see below).
%%%
wn_display_graph_entailments_of(Word) :-
setof(arc(X,Y),List^H^T^(list_of_representative_entailments(Word,List),append(H,[X,Y|T],List)),Graph), wn_display_graph(Graph).

%%% list_of_representative_entailments(+Word,-List_representative_entailments)
%%%
%%%
list_of_representative_entailments(Word,List_representative_entailments) :-
        wn_entailments_of(Word, verbose(no), List_Entailed_SynSets),
        wn_convert_synsetIDs_to_representatives(List_Entailed_SynSets, List_representative_entailments).












