import pandas as pd

# Parte 2 falta que tenga en cuenta el PoS y que se almacene y no sé si tendré que hacer que sea más robusto en 
# cuanto a fallos, en principio no, porque todas las palabras de la 1.6 estarán en la 3.0

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

def codificacionCategoria(c):
    categorias = {
        'n':'1',
        'v':'2',
        'a':'3',
        'r':'4'
        }
    return categorias[c]

def ponerEspacios(palabra):
    if type(palabra) == str:
        return "\'" + palabra[1:-1].replace('\'','\'\'').replace('_',' ') + "\'"

def media_geometrica(na,nw,ns,Na,Nw,Ns,N):
    return round((na*Na/N) + (nw*Nw/N) + (ns*Ns/N))

def comparacionGlosas(glosa1, glosa2):
    if glosa1 == []:
        return True
    elif glosa1[0] in glosa2:
        return comparacionGlosas(glosa1[1:], glosa2[glosa2.find(glosa1[0]) + len(glosa1[0]):])
    else:
        return False

def comparacionGlosas_2(glosa1, glosa2):
    count = 0
    for palabra in glosa1:
        if " " + palabra + " " in " " + glosa2 + " ":
            count += 1
    return count / len(glosa1) * 100

# TODO: qué hacemos con los verbos?

def fusionarDF(dfAnCora, dfWikiCorpus, dfSenSem, dfWN30):
    Na = len(dfAnCora)
    Nw = len(dfWikiCorpus)
    Ns = len(dfSenSem)
    N = Na + Nw + Ns

    por = 5

    for i in dfWN30.index:

        if i/len(dfWN30)*100 > por:
            por += 5
            print(str(i) + " / " + str(len(dfWN30)) + " = " + str(i/len(dfWN30)*100))
            print(dfWN30)
            dfWN30.to_csv("spa\PrologCSV\AAAAAAAAAAAAAAAAAAAA_WN_S.CSV")

        na = 0
        nw = 0
        ns = 0

        if (dfWN30['Word'][i][1:-1] in dfSynsets30AnCora.values) & (str(dfWN30['Synset'][i]) in dfSynsets30AnCora.values):
            try:
                na = dfSynsets30AnCora.loc[(dfSynsets30AnCora['Synset16'].str.contains(str(dfWN30['Synset'][i]))) & (dfSynsets30AnCora['Palabra'].str.contains(dfWN30['Word'][i][1:-1])), "TagCount"].values[0]
            except:
                pass

        if (dfWN30['Word'][i][1:-1] in dfWikiCorpus.values) & (str(dfWN30['Synset'][i]) in dfWikiCorpus.values):
            try:
                nw = dfWikiCorpus.loc[(dfWikiCorpus['Synset16'].str.contains(str(dfWN30['Synset'][i]))) & (dfWikiCorpus['Palabra'].str.contains(dfWN30['Word'][i][1:-1])), "TagCount"].values[0]
            except:
                pass

        if (dfWN30['Word'][i][1:-1] in dfSenSem.values) & (str(dfWN30['Synset'][i]) in dfSenSem.values):
            try:
                ns = dfSenSem.loc[(dfSenSem['Synset16'].str.contains(str(dfWN30['Synset'][i]))) & (dfSenSem['Palabra'].str.contains(dfWN30['Word'][i][1:-1])), "TagCount"].values[0]
            except:
                pass

        dfWN30['Tag Count'][i] = media_geometrica(na, nw, ns, Na, Nw, Ns, N)

    return dfWN30

def obtenerWN30(synset16):

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

            lista = tokens[4:4 + (palabras * 2)]
            cadena = ""

            for j in lista:
                cadena += j + " "

    synset30 = ""

    for i in wn_30[29:]:
        if i.find(cadena) != -1:
            tokens = i.split(' ')
            synset30 = tokens[0]
    if synset30 != "":
        return synset30
    else:
        lista = cadena.split(' ')
        synset30=obtenerWN30_2(lista, glosa)
        print(synset30)
        return synset30

#TODO mejorarlo para que haga lo de comparar que estén en el mismo orden las palabras o buscar otro menos, aquí hay que decidir qué se prefiere, 
# la precisión (requisitos más difíciles pero que nos aseguren que pertenecen al mismo synset) o la cantidad (reducir los requisitos para que 
# haya más palabras que se traduzcan aunque ello conlleve a que algunas no sean las mejores palabras elegidas)

def obtenerWN30_2(lista, glosa):
    synset30 = ""
    glosa = glosa.split(";")[0]
    glosa = glosa.replace(",","")
    glosa = glosa.replace(";","")
    glosa = glosa.replace(".","")
    glosa = glosa.split(" ")
    for i in wn_30[29:]:
        synset30 = ""
        linea_dividida = i.split(' | ')        
        porcentajeLista = 0
        for j in range(0, int(len(lista) / 2)):
            if (" " + lista[j * 2] + " ") in (" " + linea_dividida[0] + " "):
                porcentajeLista = porcentajeLista + 1

        if porcentajeLista > 0:
            if comparacionGlosas(glosa, linea_dividida[1]) == True:
                synset30 = i.split(' ')[0]
                return synset30
            elif comparacionGlosas_2(glosa, linea_dividida[1]) > 50:
                    synset30 = i.split(' ')[0]
                    return synset30
            else:
                return "Synset Not Found"

def traductor16a30(dfSynsets16):
    x = 1
    for i in dfSynsets16.index:
        if ((i + 1) / len(dfSynsets16) * 100) >= 20 * x:
            print(str(i + 1) + "/" + str(len(dfSynsets16)) + " = " + str(((i + 1) / len(dfSynsets16) * 100)) + "%")
            x = x + 1
        dfSynsets16['Synset16'][i] = "1" + str(obtenerWN30(dfSynsets16['Synset16'][i]))
    return dfSynsets16

dfSynsets16AnCora = pd.read_csv('spa/PrologCSV/Tag_Count_AnCora.csv', encoding = 'utf-8', index_col=[0], dtype={'Synset16':'string'})
#dfSynsets30AnCora = pd.read_csv('spa/PrologCSV/Tag_Count_AnCora30.csv', encoding = 'utf-8', index_col=[0], dtype={'Synset16':'string'})

dfSynsets16WikiCorpus = pd.read_csv('spa/PrologCSV/Tag_Count_WikiCorpus.csv', encoding = 'utf-8', index_col=[0], dtype={'Synset16':'string'})
#dfSynsets30WikiCorpus = pd.read_csv('spa/PrologCSV/Tag_Count_WikiCorpus30.csv', encoding = 'utf-8', index_col=[0], dtype={'Synset16':'string'})

dfSynsets30SenSem = pd.read_csv('spa/PrologCSV/Tag_Count_SenSem.csv', encoding = 'utf-8', index_col=[0], dtype={'Synset16':'string'})

dfWN30 = pd.read_csv('spa/PrologCSV/wn_s.csv', encoding='utf-8', index_col=[0])

wn_16 = open('WN16/data.noun', 'r', encoding = 'utf-8')
wn_30 = open('WN30/data.noun', 'r', encoding = 'utf-8')

wn_16 = wn_16.readlines()
wn_30 = wn_30.readlines()

print("Traduciendo AnCora de WordNet 1.6 a 3.0")
dfSynsets30AnCora = traductor16a30(dfSynsets16AnCora)
print(dfSynsets30AnCora)
dfSynsets30AnCora.to_csv("spa\PrologCSV\Tag_Count_AnCora30.csv")

print("Traduciendo WikiCorpus de WordNet 1.6 a 3.0")
dfSynsets30WikiCorpus = traductor16a30(dfSynsets16WikiCorpus)
print(dfSynsets30WikiCorpus)
dfSynsets30WikiCorpus.to_csv("spa\PrologCSV\Tag_Count_WikiCorpus30.csv")

dfWN30 = fusionarDF(dfSynsets30AnCora, dfSynsets30WikiCorpus, dfSynsets30SenSem, dfWN30)

print(dfWN30)
dfWN30.to_csv("spa\PrologCSV\AAAAAAAAAAAAAAAAAAAA_WN_S.CSV")