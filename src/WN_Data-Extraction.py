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

def get_antonyms(wn_line):
    return wn_line.count(" ! ")

def get_hypernyms(wn_line):
    return wn_line.count(" @ ")

def get_i_hypernyms(wn_line):
    return wn_line.count(" @i ")
    
def get_hyponym(wn_line):
    return wn_line.count(" ~ ")
    
def get_i_hyponym(wn_line):
    return wn_line.count(" ~i ")

def get_m_holonym(wn_line):
    return wn_line.count(" #m ")

def get_s_holonym(wn_line):
    return wn_line.count(" #s ")

def get_p_holonym(wn_line):
    return wn_line.count(" #p ")

def get_m_meronym(wn_line):
    return wn_line.count(" %m ")

def get_s_meronym(wn_line):
    return wn_line.count(" %s ")

def get_p_meronym(wn_line):
    return wn_line.count(" %p ")

def get_attribute(wn_line):
    return wn_line.count(" = ")

def get_d_r_t(wn_line):
    return wn_line.count(" + ")

def get_list_hypenyms(cadena):
    resultados = []
    indice = 0
    
    while indice < len(cadena):
        # Buscar el siguiente "@"
        indice = cadena.find("@", indice)
        
        # Si no se encuentra "@" se rompe el bucle
        if indice == -1:
            break
        
        # Obtener los siguientes 9 caracteres después del "@"
        segmento = cadena[indice+2:indice+10]
        
        # Agregar el segmento a la lista de resultados
        resultados.append(segmento)
        
        # Mover el índice más allá del "@" encontrado para continuar la búsqueda
        indice += 1
    
    return resultados

def getDF(wn):
    wn_synsets = list(map(get_synset, wn))
    wn_words =  list(map(get_words, wn))
    wn_gloss = list(map(get_gloss, wn))
    wn_list_hypernyms = list(map(get_list_hypenyms, wn))
    wn_antonyms = list(map(get_antonyms, wn))
    wn_hypernyms = list(map(get_hypernyms, wn))
    wn_i_hypernyms = list(map(get_i_hypernyms, wn))
    wn_hyponym = list(map(get_hyponym, wn))
    wn_i_hyponym = list(map(get_i_hyponym, wn))
    wn_m_holonym = list(map(get_m_holonym, wn))
    wn_s_holonym = list(map(get_s_holonym, wn))
    wn_p_holonym = list(map(get_p_holonym, wn))
    wn_m_meronym = list(map(get_m_meronym, wn))
    wn_s_meronym = list(map(get_s_meronym, wn))
    wn_p_meronym = list(map(get_p_meronym, wn))
    wn_attribute = list(map(get_attribute, wn))
    wn_d_r_t = list(map(get_d_r_t, wn))

    df = pd.DataFrame(columns=["Synset","Words","Gloss"])
    df["Synset"] = wn_synsets
    df["Words"] = wn_words
    df["Gloss"] = wn_gloss
    df["Hypernyms"] = wn_list_hypernyms
    df["antonyms"] = wn_antonyms
    df["hypernyms"] = wn_hypernyms
    df["i_hypernyms"] = wn_i_hypernyms
    df["hyponym"] = wn_hyponym
    df["i_hyponym"] = wn_i_hyponym
    df["m_holonym"] = wn_m_holonym
    df["s_holonym"] = wn_s_holonym
    df["p_holonym"] = wn_p_holonym
    df["m_meronym"] = wn_m_meronym
    df["s_meronym"] = wn_s_meronym
    df["p_meronym"] = wn_p_meronym
    df["attribute"] = wn_attribute
    df["d_r_t"] = wn_d_r_t
    return df

wn_16 = open('WN16/data.noun', 'r', encoding = 'utf-8').readlines()[29:]
wn_30 = open('WN30/data.noun', 'r', encoding = 'utf-8').readlines()[29:]

df16 = getDF(wn_16)
df30 = getDF(wn_30)

df16.to_csv("Words&Gloss16.csv")
df30.to_csv("Words&Gloss30.csv")
