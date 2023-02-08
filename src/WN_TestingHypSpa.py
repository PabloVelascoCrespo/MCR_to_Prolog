import pandas as pd
from pyswip import Prolog
from collections import OrderedDict
import random

def codificacionCategorias(letra):
    switch={
        'n':'1',
        'v':'2',
        'a':'3',
        'r':'4'
    }
    return switch.get(letra,'Error')

def lista_hiperonimos(synset):
    Lista_de_Hiperonimos = []
    Lista_de_Hiperonimos.append(int(synset))
    Hiperonimo = synset
    aux = []
    Hiperonimos = []

    while True:
        Hiperonimos = dfHyp.loc[dfHyp["Synset Source"] == int(Hiperonimo)]["Synset Target"]
        if(len(Hiperonimos)) == 1:
            Hiperonimo = Hiperonimos.item()
        elif len(Hiperonimos) > 1:
            lista = Hiperonimos.values.tolist()
            Hiperonimo = lista[0]
            for hiperIndex in range(1,len(lista)):
                aux += lista_hiperonimos(lista[hiperIndex])
            for elem in aux:
                condicion = True
                if type(elem) == list:
                    for a in elem:
                        if a in Lista_de_Hiperonimos:
                            condicion = False
                    if condicion:
                        elem.extend(Lista_de_Hiperonimos)
                else:
                    print('a')
                    aux.extend(Lista_de_Hiperonimos)
                    break
        else:
            break
        Lista_de_Hiperonimos.insert(0,Hiperonimo)
    if aux != []:
        aux.insert(0,Lista_de_Hiperonimos)
    else:
        return [Lista_de_Hiperonimos]
    return aux



prolog = Prolog()
prolog.consult('wn/wn_connect.pl')

dfS = pd.read_csv('src\DataFrames\dfSspa.csv', index_col = [0])
dfS = dfS.loc[dfS['Type'].isin(['n','v'])][['Word','Type']]

lista_palabras_index = []
lista_palabras = []

n = 10

while len(lista_palabras_index) < n:
    palabra_index = random.randint(0, len(dfS)-1)
    if palabra_index not in lista_palabras_index:
        lista_palabras_index.append(palabra_index)

for index in lista_palabras_index:
    lista_palabras.append(dfS.iloc[index]['Word'])

print("Se van a testear las siguientes palabras:")
num = 1
for palabra in lista_palabras:
    print(str(num) + '.- '+palabra+'.')
    num = num +1

print('\n')

contador_correctas = 0

for Hiponimo in lista_palabras:
    Lista_de_HiperonimosMCR = []
    Lista_de_HiperonimosProlog = []
    for hiperonimos in prolog.query("wn_hypernyms(\'"+ Hiponimo +"\', no, Hiperonimos)"):
        Lista_de_HiperonimosProlog.append(hiperonimos["Hiperonimos"])

    dfHyp = pd.read_csv('src\DataFrames\dfRelations_spa_hyp.csv', index_col = [0])
    Lista_de_Synsets = []

    for i in range(0,len(Lista_de_HiperonimosProlog)):
        Lista_de_Synsets.append(str(Lista_de_HiperonimosProlog[i][-1]))

    Lista_de_Synsets = list(OrderedDict.fromkeys(Lista_de_Synsets))

    for i in Lista_de_Synsets:
        listaH = lista_hiperonimos(i)
        Lista_de_HiperonimosMCR+= listaH

    print("MCR:\n",Lista_de_HiperonimosMCR,"\n\n")
    print("Prolog:\n",Lista_de_HiperonimosProlog,"\n")

    elementos_correctos = 0

    for Elemento_de_MCR in Lista_de_HiperonimosMCR:
        for Elemento_de_Prolog in Lista_de_HiperonimosProlog:
            if Elemento_de_MCR == Elemento_de_Prolog:
                elementos_correctos+=1

    if elementos_correctos == len(Lista_de_HiperonimosMCR):
        print("Las listas de hiperónimos de la palabra "+Hiponimo+" son iguales.\n\n")
        contador_correctas += 1
    else:
        print('Las listas de hiperónimos de la palabra '+Hiponimo+' NO son iguales.\n\n')

print('\nHa habido un total de '+str(contador_correctas)+'/'+str(n)+' listas iguales.')