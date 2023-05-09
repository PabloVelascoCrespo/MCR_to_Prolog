import pandas as pd
import glob

# Parte 1 TODO, dudas: debería hacer un programa por cada corpus, porque cada uno tiene su estructura y almacenar
# los conjuntos de datos en algún formato y así ya solo leerlos desde aquí y hacer todo ese proceso

lista_ficheros = []

for archivo in glob.glob("Corpus/ancora-3.0.1es/**", recursive = True):
    if 'xml' in archivo:
        lista_ficheros.append(archivo)

dfSynsets16 = pd.DataFrame(columns = ['Synset16', 'PoS', 'Palabra', 'TagCount'])
df_no_encontrados = pd.DataFrame(columns = ['PoS', 'Palabra', 'TagCount', 'Lista', 'Glosa'])

def codificacionCategoria(c):
    categorias = {
        'n':'1',
        'v':'2',
        'a':'3',
        'r':'4'
        }
    return categorias[c]

def codificacionNumero(c):
    numeros = {
        '0a':10,
        '0b':11,
        '0c':12,
        '0d':13,
        '0e':14,
        '0f':15,
        '0g':16,
        '0h':17,
        '0i':18,
        '0j':19,
        '0k':20,
        '0l':21,
        '0m':22,
        '0n':23,
        '0o':24,
        '0p':25,
        '1a':26,
        '1b':27,
        '1c':28,
        '1d':29,
        '1e':30
        }
    return numeros[c]

for file in lista_ficheros:
    print('Abriendo fichero ' + file + '.')

    xml = open(file,'r', encoding = 'utf-8')
    xml_lineas = xml.readlines()

    lineas = []

    for linea in xml_lineas:
        index = linea.find('<n')

        if index != -1:
            lineas.append(linea[index:])

    for linea in lineas:
        if linea.find('lem') != -1 & linea.find('sense')!=-1 & linea.find('cs1') == -1:

            tokens = linea.split(' ')

            for token in tokens:
                if token.find('lem') != -1:
                    palabra = token[5:-1]

                if token.find('sense') != -1:
                    synset = token[10:-1]

            if (synset in dfSynsets16.values) & (palabra in dfSynsets16.values):
                dfSynsets16.loc[(dfSynsets16['Palabra'].str.contains(palabra)) & (dfSynsets16['Synset16'].str.contains(synset)), "TagCount"] += 1

            else:
                dfSynsets16.loc[len(dfSynsets16)] = [synset, 'n', palabra, 1]

dfSynsets16.to_csv('spa/PrologCSV/Tag_Count.csv')

    # Parte 2 falta que tenga en cuenta el PoS y que se almacene y no sé si tendré que hacer que sea más robusto en 
    # cuanto a fallos, en principio no, porque todas las palabras de la 1.6 estarán en la 3.0

#dfSynsets16 = pd.read_csv('spa/PrologCSV/Tag_Count.csv', encoding = 'utf-8', index_col=[0])

wn_16 = open('WN16/data.noun', 'r', encoding = 'utf-8')
wn_30 = open('WN30/data.noun', 'r', encoding = 'utf-8')

wn_16 = wn_16.readlines()
wn_30 = wn_30.readlines()

df = pd.read_csv('spa/PrologCSV/wn_s.csv', encoding = 'utf-8', index_col = [0])

def obtenerWN30(palabra, pos, synset16, tagcount):

    cadena = ""

    for i in wn_16[29:]:
        if i[0:8] == synset16:
            glosa = i.split(' | ')[1]
            tokens = i.split(' ')
            palabras = 0

            try:
                palabras = int(tokens[3])
            except:
                palabras = codificacionNumero(tokens[3])

            lista = tokens[4:4+(palabras*2)]
            cadena = ""

            for j in lista:
                cadena += j + " "

    synset30 = ""

    for i in wn_30[29:]:
        if i.find(cadena) != -1:
            tokens = i.split(' ')
            synset30 = tokens[0]

    if synset30 != "":
        synset30 = codificacionCategoria(pos) + synset30
        df.loc[(df['Word'].str.contains(palabra)) & (df['Synset'] == int(synset30)), "Tag Count"] = tagcount

    else:
        df_no_encontrados.loc[len(df_no_encontrados)] = [pos, palabra, tagcount, lista, glosa]

def obtenerWN30_2(palabra, pos, tagcount, lista, glosa):
    synset30 = ""
    porcentajeLista = 0
    porcentajeGlosa = 0

    for i in wn_30[29:]:
        synset30 = ""
        linea_dividida = i.split(' | ')

        for j in range(0, int(len(lista)/2)):
            if lista[j*2] in linea_dividida[0]:
                porcentajeLista = porcentajeLista+1

        if porcentajeLista > 2:
            for elem in glosa:
                if elem in linea_dividida[1]:
                    porcentajeGlosa = porcentajeGlosa + 1

        porcentajeGlosa = porcentajeGlosa / len(linea_dividida[1]) * 100

        if porcentajeGlosa > 75:
            synset30 = i.split(' ')[0]
            break

    if synset30 != "":
        synset30 = codificacionCategoria(pos) + synset30
        df.loc[(df['Word'].str.contains(palabra)) & (df['Synset'] == int(synset30)), "Tag Count"] = tagcount

for i in dfSynsets16.index:
    print(str(i+1) + "/" + str(len(dfSynsets16)) + " = " + str(((i+1)/len(dfSynsets16)*100)) + "%")
    obtenerWN30(dfSynsets16['Palabra'][i], dfSynsets16['PoS'][i], dfSynsets16['Synset16'][i], dfSynsets16['TagCount'][i])

for i in df_no_encontrados.index:
    print(str(i+1) + "/" + str(len(df_no_encontrados)) + " = " + str(((i+1)/len(df_no_encontrados)*100)) + "%")
    obtenerWN30_2(df_no_encontrados['Palabra'][i], df_no_encontrados['PoS'][i], df_no_encontrados['TagCount'][i], df_no_encontrados['Lista'][i], df_no_encontrados['Glosa'][i])

df.to_csv("spa\PrologCSV\wn_s.csv")