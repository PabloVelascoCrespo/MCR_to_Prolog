import pandas as pd
import time

idiomas = ['cat', 'eng', 'eus', 'glg', 'por', 'spa']

def codificacionCategoria(c):
    categorias = {
        'n':'1',
        'v':'2',
        'a':'3',
        'r':'4'
        }
    return categorias[c]

def crearSynsetID(synset):
    synset = codificacionCategoria(synset[-1]) + synset[7:15]
    return int(synset)

def contarSynsets(lista, e):
   contador = 0
   for i in lista:
      if i == e:
         contador += 1
   return str(contador)

def ponerEspacios(palabra):
    if type(palabra) == str:
        return "\'" + palabra[1:-1].replace('\'','\'\'').replace('_',' ') + "\'"

for i in idiomas:
    inicio = time.time()

    ruta = "mcrCSV//" + i + "WN\wei_" + i + "-30_variant.csv"
    print("Leyendo dataframe " + ruta)
    
    df = pd.read_csv(ruta, index_col = [0])
    df = df.drop(columns = ['Conf', 'Exp', 'Mark'])
    df.columns = ['Word', 'Sense', 'Synset', 'Type']

    df['Synset'] = df['Synset'].apply(crearSynsetID)
    df['Word'] = df["Word"].apply(ponerEspacios)

    W_Nums = []
    Synsets_list = df.Synset.value_counts()

    # TODO: se podría optimizar un poco más? Se puede utilizar apply o transform al revés? :D
    # Tiempos de la última ejecución:
    # cat ha tardado 16.22.
    # eng ha tardado 39.88.
    # eus ha tardado  7.83.
    # glg ha tardado  8.45.
    # por ha tardado  4.94.
    # spa ha tardado 25.50.

    for index in reversed(df.index):
        fila = df.loc[index]
        W_Nums.insert(0, Synsets_list[fila['Synset']])
        Synsets_list[fila['Synset']] = Synsets_list[fila['Synset']] - 1

    df['W Num'] = W_Nums
    df['Tag Count'] = [0] * len(df['Word'])

    df = df[['Synset', 'W Num', 'Word', 'Type', 'Sense', 'Tag Count']]

    df = df.sort_values(by = ['Synset','W Num'])
    df = df.reset_index(drop = True)
    df.to_csv(i + "\PrologCSV\wn_s.csv")

    ficheroEscritura = open(i + "\Prolog\wn_s.pl", "w", encoding = 'utf-8')

    for i in df.index:
        ficheroEscritura.write("s(" + str(df["Synset"][i]) + "," + str(df["W Num"][i]) + "," + str(df["Word"][i]) + "," + df["Type"][i] + "," + str(df["Sense"][i]) + "," + str(df["Tag Count"][i]) + ").\n")

    ficheroEscritura.close()

    final = time.time()
    print('Proceso en ruta: ' + ruta + ' finalizado. Ha tardado ' + str(final-inicio) + '.\n')
