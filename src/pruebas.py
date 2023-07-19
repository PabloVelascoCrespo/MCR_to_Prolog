import pandas as pd
import glob

def is_synset(synset):
    if len(synset) == 8:
        return True
    else:
        return False
    
# WIKICORPUS ##############################################################################################################

dfSynsets16 = pd.read_csv('spa/PrologCSV/Tag_Count_WikiCorpus.csv', index_col = [0], dtype = {'Synset16':'string'})

lista_ficheros = []

for archivo in glob.glob("Corpus/Wikicorpus/**", recursive = True):
    if '0' in archivo:
        lista_ficheros.append(archivo)

for fichero_ruta in lista_ficheros:
    print('Abriendo fichero ' + fichero_ruta + '.')

    fichero = open(fichero_ruta, 'r')
    lineas = fichero.readlines()

    i = 1
    x = 1

    for linea in lineas:
        porcentaje = i / len(lineas) * 100
        linea_split = linea.split(' ')

        if len(linea_split) == 4:
            if "N" == linea_split[2][0]:
                synset = str(linea_split[3][:-1])
                palabra = linea_split[1]
                if is_synset(synset):
                    if (synset in dfSynsets16.values) & (linea_split[1] in dfSynsets16.values):
                        dfSynsets16.loc[(dfSynsets16['Palabra'].str.contains(linea_split[1])) & (dfSynsets16['Synset16'].str.contains(linea_split[3][:-1])), "TagCount"] += 1

                    else:
                        dfSynsets16.loc[len(dfSynsets16)] = [linea_split[3][:-1], 'n', linea_split[1], 1]

        if  porcentaje > 5 * x:
            x = x + 1
            dfSynsets16 = dfSynsets16.sort_values(by = ['Synset16'])
            dfSynsets16 = dfSynsets16.reset_index(drop = True)
            dfSynsets16.to_csv('spa/PrologCSV/Tag_Count_WikiCorpus_Pruebas.csv')
            print(round(porcentaje, 2), "%")
        i = i + 1

dfSynsets16 = dfSynsets16.sort_values(by = ['Synset16'])
dfSynsets16 = dfSynsets16.reset_index(drop = True)
dfSynsets16.to_csv('spa/PrologCSV/Tag_Count_WikiCorpus.csv')
