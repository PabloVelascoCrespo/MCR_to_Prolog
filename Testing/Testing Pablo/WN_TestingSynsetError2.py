import pandas as pd

df = pd.read_csv('mcrCSV/engWN/wei_eng-30_relation.csv', index_col=[0])

fichero = open("Testing/Testing Pablo/ListaSynsetError.txt")
lineas = fichero.readlines()

lista = []
for linea in lineas:
    lista.append(linea[:-1])

res = [*set(lista)]

print('Hay un total de '+str(len(res))+' synsets que están en las relaciones pero que no están en el fichero variant, en las bases de datos de MCR en inglés.')

listaF = []
for ele in res:
    listaAux = []
    listaAux.append(ele)
    a = df[df['S_Synset'].isin([ele]) | df['T_Synset'].isin([ele])]['Rel_ID'].items()
    for e in a:
        listaAux.append(e[1])
    listaF.append(listaAux)

print(listaF)