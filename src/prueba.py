import pandas as pd

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

def obtenerWN30(synset16):

    cadena16 = ""
    glosa = "" 
    for i in wn_16[29:]:
        if i[0:8] == synset16:
            glosa16 = i.split(' | ')[1][:-1]
            tokens16 = i.split(' ')
            palabras16 = 0

            try:
                palabras16 = int(tokens16[3])

            except:
                palabras16 = codificacionNumero(tokens16[3])

            lista16 = tokens16[4:4 + (palabras16 * 2)]
            cadena16 = ""

            for j in range(0,len(lista16),2):
                cadena16 += lista16[j] + " "

    synset30 = ""
    glosa30 = ""

    for i in wn_30[29:]:
        tokens30 = i.split(" ")
        palabras30 = 0

        try:
            palabras30 = int(tokens30[3])

        except:
            palabras30 = codificacionNumero(tokens30[3])
        lista30 = tokens30[4:4 + (palabras30 * 2)]
        cadena30 = ""

        for j in range(0,len(lista30),2):
            cadena30 += lista30[j] + " "

        if subsumida(cadena16, cadena30) or subsumida(cadena30, cadena16):
            synset30 = i.split(' ')[0]
            glosa30 = i.split(' | ')[1][:-1]
            try:
                if subsumida(glosa30, glosa16):
                    return synset30
            except:
                print("ERROR SYNSET: "+ synset16)


def subsumida(cadena16, subcadena16):
    cadena16 = cadena16.split(" ")
    subcadena16 = subcadena16.split(" ")
    
    i = 0
    j = 0
    
    while i < len(cadena16) and j < len(subcadena16):
        if cadena16[i] == subcadena16[j]:
            j += 1
        i += 1
    return j == len(subcadena16)
def traductor16a30(dfSynsets16, log):
    x = 1
    for i in dfSynsets16.index:
        if ((i + 1) / len(dfSynsets16) * 100) >= 20 * x:
            print(str(i + 1) + "/" + str(len(dfSynsets16)) + " = " + str(((i + 1) / len(dfSynsets16) * 100)) + "%")
            x = x + 1
        synset30 =str(obtenerWN30(dfSynsets16['Synset16'][i]))
        log += dfSynsets16['Synset16'][i] + "-" + synset30 + "\n"
        dfSynsets16['Synset16'][i] = "1" + synset30
    return dfSynsets16,log

wn_16 = open('WN16/data.noun', 'r', encoding = 'utf-8').readlines()
wn_30 = open('WN30/data.noun', 'r', encoding = 'utf-8').readlines()

dfSynsets16AnCora = pd.read_csv('spa/PrologCSV/Tag_Count_AnCora.csv', encoding = 'utf-8', index_col=[0], dtype={'Synset16':'string'})
print("Traduciendo AnCora de WordNet 1.6 a 3.0")
log = ""
dfSynsets30AnCora,log = traductor16a30(dfSynsets16AnCora, log)

with open("log.txt", "w") as archivo:
    archivo.write(log)

print(dfSynsets30AnCora)
dfSynsets30AnCora.to_csv("spa\PrologCSV\Tag_Count_AnCora30(1).csv")