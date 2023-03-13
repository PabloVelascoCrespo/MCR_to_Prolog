import time
import pandas as pd
from googletrans import Translator

pd.options.display.max_colwidth = 50000

translator = Translator()

#TODO: Así vale controlar el error? B)
def traductor(synset):
    print(synset)
    cadena = ""
    try:
        cadena = translator.translate(dfEng.loc[dfEng['Synset'] == synset].Glosa.item(), dest="es").text
        cadena = cadena.replace('\'','\'\'')
        cadena = cadena.replace('"', '""')
    except:
        cadena = 'None (error al traducir)'
    return cadena

inicio = time.time()

dfSpa = pd.read_csv('spa\PrologCSV\wn_g.csv', index_col=0)
dfEng = pd.read_csv('engProlog30CSV\wn_g.csv', index_col=0)

filtro = dfSpa['Glosa'] == "None (error al traducir)"
dfNoneSpa = dfSpa[filtro]

filtro = dfEng['Glosa'] != "None"
dfEng = dfEng[filtro]

dfNoneSpa['Glosa'] = dfNoneSpa['Synset'].apply(traductor)

dfSpa.loc[dfNoneSpa.index, 'Glosa'] = dfNoneSpa['Glosa']

dfSpa.to_csv("spa\PrologCSV\wn_g.csv")

ficheroEscritura = open("spa\Prolog\wn_g.pl", "w", encoding='utf-8')

for index in dfSpa.index:
    ficheroEscritura.write("g("+str(dfSpa["Synset"][index])+",\'"+str(dfSpa["Glosa"][index])+"\').\n")

print(dfSpa.head(15))

final = time.time()
print('Ha tardado '+str(final-inicio)+'.\n')