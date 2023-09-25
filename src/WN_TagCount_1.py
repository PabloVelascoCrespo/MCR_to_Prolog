import pandas as pd
import glob

def is_synset(synset):
    if len(synset) == 8:
        return True
    else:
        return False

def codificacionCategoria(c):
    categorias = {
        'n':'1',
        'v':'2',
        'a':'3',
        'r':'4'
        }
    return categorias[c]

# Parte 1 TODO, dudas: debería hacer un programa por cada corpus, porque cada uno tiene su estructura y almacenar
# los conjuntos de datos en algún formato y así ya solo leerlos desde aquí y hacer todo ese proceso

# ANCORA ##############################################################################################################

lista_ficheros = []

for archivo in glob.glob("Corpus/Ancora/**", recursive = True):
    if 'xml' in archivo:
        lista_ficheros.append(archivo)

dfSynsets16 = pd.DataFrame(columns = ['Synset16', 'PoS', 'Palabra', 'TagCount'])

for file in lista_ficheros:
    print('Abriendo fichero ' + file + '.')

    xml = open(file, 'r', encoding = 'utf-8')
    xml_lineas = xml.readlines()

    lineas = []

    for linea in xml_lineas:
        index = linea.find('<n')

        if index != -1:
            lineas.append(linea[index:])

    for linea in lineas:
        if linea.find('lem') != -1 & linea.find('sense') != -1:
            if 'cs' not in linea:
                tokens = linea.split(' ')

                for token in tokens:
                    if token.find('lem') != -1:
                        palabra = token[5:-1]

                    if token.find('sense') != -1:
                        synset = token[10:-1]

                if '+' in synset:
                    synsets = synset.split('+')
                    for syn in synsets:
                        if (syn in dfSynsets16.values) & (palabra in dfSynsets16.values):
                            dfSynsets16.loc[(dfSynsets16['Palabra'].str.contains(palabra)) & (dfSynsets16['Synset16'].str.contains(syn)), "TagCount"] += 1

                        else:
                            dfSynsets16.loc[len(dfSynsets16)] = [syn, 'n', palabra, 1]
                else:
                    if (synset in dfSynsets16.values) & (palabra in dfSynsets16.values):
                        dfSynsets16.loc[(dfSynsets16['Palabra'].str.contains(palabra)) & (dfSynsets16['Synset16'].str.contains(synset)), "TagCount"] += 1

                    else:
                        dfSynsets16.loc[len(dfSynsets16)] = [synset, 'n', palabra, 1]

dfSynsets16.to_csv('spa/PrologCSV/Tag_Count_AnCora.csv')

# WIKICORPUS ##############################################################################################################

dfSynsets16 = pd.read_csv('spa/PrologCSV/Tag_Count_WikiCorpus.csv',index_col=[0], dtype={"Synset16":"string"})

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
            dfSynsets16.to_csv('spa/PrologCSV/Tag_Count_WikiCorpus.csv')
            print(round(porcentaje, 2), "%")
        i = i + 1

dfSynsets16.to_csv('spa/PrologCSV/Tag_Count_WikiCorpus.csv')

# SENSEM ##############################################################################################################
dfSynsetsSenSem = pd.DataFrame(columns=['Synset', 'PoS', 'Palabra','TagCount'])

rutaSenSem = "Corpus/SenSem/spsemcor.utf8.xml"

archivoSenSem = open(rutaSenSem, 'r', encoding='utf-8')

for linea in archivoSenSem:
    if 'WN30_S=' in linea:
        synset30SenSem = codificacionCategoria(linea[linea.find('WN30_S')+16]) +  linea[linea.find('WN30_S')+8:linea.find('WN30_S')+16]
        PoS = linea[linea.find('WN30_S')+16]
        palabra = ""
        if 'lema=' in linea:
            palabra = linea[linea.find('lema=')+6:linea.find('lema=')+6+linea[linea.find('lema=')+6:].find('"')]
        elif 'lema_verbo=' in linea:
            palabra = linea[linea.find('lema_verbo=')+12:linea.find('lema_verbo=')+12+linea[linea.find('lema_verbo=')+12:].find('"')]
        if palabra == "":
            print("No se ha encontrado la palabra con SYNSET: " + synset30SenSem)
        else:
            if (synset30SenSem in dfSynsetsSenSem.values) & (palabra in dfSynsetsSenSem.values):
                dfSynsetsSenSem.loc[(dfSynsetsSenSem['Palabra'].str.contains(palabra)) & (dfSynsetsSenSem['Synset'].str.contains(synset30SenSem)), "TagCount"] += 1
            else:
                dfSynsetsSenSem.loc[len(dfSynsetsSenSem)] = [synset30SenSem, PoS, palabra, 1]

dfSynsetsSenSem = dfSynsetsSenSem.sort_values(['Synset', 'TagCount', 'Palabra'])    
dfSynsetsSenSem = dfSynsetsSenSem.reset_index(drop=True)       
dfSynsetsSenSem.to_csv('spa/PrologCSV/Tag_Count_SenSem.csv')