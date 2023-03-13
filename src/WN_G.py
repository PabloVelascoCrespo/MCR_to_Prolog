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

def reemplazarComillas(palabra):
    if type(palabra) == str:
        return palabra.replace('\'','\'\'')

def crearSynsetID(synset):
    synset = codificacionCategoria(synset[-1])+synset[7:15]
    return int(synset)

for i in idiomas:
    inicio = time.time()
   
    ruta = "mcrCSV//"+i+"WN\wei_"+i+"-30_synset.csv"
    print("Leyendo dataframe "+ ruta)
    
    df = pd.read_csv(ruta, index_col=[0])
    df = df.drop(columns=['PoS', 'Desc', 'MaxNiv', 'Niv', 'Mark'])
    df.columns = ['Synset','Glosa']

    df['Synset'] = df['Synset'].apply(crearSynsetID)
    df['Glosa'] = df['Glosa'].apply(reemplazarComillas)
    
    df = df.sort_values(by=['Synset'])
    df = df.reset_index(drop = True)
    df.to_csv(i+"\PrologCSV\wn_g.csv")

    ficheroEscritura = open(i+"\Prolog\wn_g.pl", "w", encoding='utf-8')

    for index in df.index:
        ficheroEscritura.write("g("+str(df["Synset"][index])+",\'"+str(df["Glosa"][index])+"\').\n")
    
    final = time.time()

    ficheroEscritura.close()

    print('Proceso en ruta: ' + ruta + ' finalizado. Ha tardado '+str(final-inicio)+'.\n')