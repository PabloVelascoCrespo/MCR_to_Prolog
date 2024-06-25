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

def get_synset(wn_line):
    return wn_line.split(' ')[0]

def get_words(wn_line):
    num_palabras = 0
    words = ""
    try:
        num_palabras = int(wn_line[14:16])
    except:
        num_palabras = codificacionNumero(wn_line[14:16])
    line_splited = wn_line.split(" ")
    for index in range(0,num_palabras):
        words += line_splited[4 + 2*index] + " "
    return words[:-1]

def get_gloss(wn_line):
    return wn_line.split(" | ")[1][:-1]

def getDF(wn):
    wn_synsets = list(map(get_synset, wn))
    wn_words =  list(map(get_words, wn))
    wn_gloss = list(map(get_gloss, wn))

    df = pd.DataFrame(columns=["Synset","Words","Gloss"])
    df["Synset"] = wn_synsets
    df["Words"] = wn_words
    df["Gloss"] = wn_gloss

    return df

wn_16 = open('WN16/data.noun', 'r', encoding = 'utf-8').readlines()[29:]
wn_30 = open('WN30/data.noun', 'r', encoding = 'utf-8').readlines()[29:]

df16 = getDF(wn_16)
df30 = getDF(wn_30)

df16.to_csv("Words&Gloss16.csv")
df30.to_csv("Words&Gloss30.csv")
