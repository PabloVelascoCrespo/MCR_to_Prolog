import os
from pyswip import Prolog
import random
import pandas as pd

def palabra_tiene_mayus(palabra):
    for letra in palabra:
        if letra.isupper():
            return True
    return False

pathWNDB_ENG_MCR = r'C:\Users\Usuario\Desktop\UNI\4º\2C\TFG\TFG_PabloVelascoCrespo\eng\Prolog'
pathWNDB_ENG_Kafe = r'C:\Users\Usuario\Desktop\UNI\4º\2C\TFG\TFG_PabloVelascoCrespo\engProlog30'

paths = [pathWNDB_ENG_MCR,pathWNDB_ENG_Kafe]

dfS = pd.read_csv('eng\PrologDF\wn_s.csv', index_col = [0])
dfS = dfS.loc[dfS['Type'].isin(['n','v'])][['Word']]

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
    num = num + 1

print('\n')

prolog = Prolog()
prolog.consult('wn/wn_connect.pl')

print('KAFE:')
Lista_de_Hiponimos_Kafe=[]
for Hiponimo in lista_palabras:
    aux = []
    os.environ['WNDB'] = pathWNDB_ENG_Kafe

    for hiperonimosK in prolog.query("wn_hypernyms(\'"+ Hiponimo +"\', no, H)"):
        aux.append(hiperonimosK["H"])
    Lista_de_Hiponimos_Kafe += [aux]
    print(Hiponimo+':\n')
    print(Lista_de_Hiponimos_Kafe[-1])
    print('-----------------------------------------------------------------\n')

print('MCR:')
Lista_de_Hiponimos_MCR=[]
for Hiponimo in lista_palabras:
    aux = []
    os.environ['WNDB'] = pathWNDB_ENG_MCR
    bool(list(prolog.query('wordnet:load_wordnet')))

    for hiperonimos in prolog.query("wn_hypernyms(\'"+ Hiponimo +"\', no, Hiperonimos)"):
        aux.append(hiperonimos["Hiperonimos"])
    Lista_de_Hiponimos_MCR += [aux]
    print(Hiponimo+':\n')
    print(Lista_de_Hiponimos_MCR[-1])
    print('-----------------------------------------------------------------\n')

lista_incorrectas = []
contador_correctas = 0
for index in range(n):
    if Lista_de_Hiponimos_Kafe[index] == Lista_de_Hiponimos_MCR[index]:
        print("Las listas de hiperónimos de la palabra "+lista_palabras[index]+" son iguales.\n\n")
        contador_correctas += 1
    else:
        lista_incorrectas.append(lista_palabras[index])
        print("Las listas de hiperónimos de la palabra "+lista_palabras[index]+" NO son iguales.\n\n")
    print('-----------------------------------------------------------------')

print('Ha habido un total de',contador_correctas,'/',n,'palabras iguales.\n')
print('Lista de palabras que son diferentes:')
for palabra_incorrecta in lista_incorrectas:
    if not palabra_tiene_mayus(palabra_incorrecta):
        print(palabra_incorrecta)