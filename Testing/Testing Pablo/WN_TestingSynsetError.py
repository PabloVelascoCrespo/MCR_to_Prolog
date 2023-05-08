import pandas as pd

dfVar = pd.read_csv('mcrCSV/engWN/wei_eng-30_variant.csv', index_col=[0])
dfRel = pd.read_csv('mcrCSV/engWN/wei_eng-30_relation.csv', index_col=[0])

listVar   = dfVar['SynsetPoS'].to_list()
sourceRel = dfRel['S_Synset'].to_list()
targetRel = dfRel['T_Synset'].to_list()

ListaSynsetError = []

for i in sourceRel:
    if i not in listVar:
        ListaSynsetError.append(i)

for i in targetRel:
    if i not in listVar:
        ListaSynsetError.append(i)

#Escribir Fichero Lista Synset Error