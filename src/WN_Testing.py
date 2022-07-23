import pandas as pd
from pyswip import Prolog

def codificacionCategorias(letra):
    switch={
        'n':'1',
        'v':'2',
        'a':'3',
        'r':'4'
    }
    return switch.get(letra,'Error')

prolog = Prolog()
prolog.consult()

fichero = open('mcr\spaWN\wei_spa-30_relation.tsv','r', encoding='utf-8')
lineas = fichero.readlines()

Source_Synset = []
Target_Synset = []


for linea in lineas:
    linea = linea.split('\t')
    if linea[0] != "12": 
        break

    Source_Synset.append(codificacionCategorias(linea[2]) + linea[1][7:15])
    Target_Synset.append(codificacionCategorias(linea[4]) + linea[3][7:15])

df = pd.DataFrame({"Source Synset":Source_Synset, "Target Synset":Target_Synset})
# df.to_csv("src/dfHiponimos.csv") 

