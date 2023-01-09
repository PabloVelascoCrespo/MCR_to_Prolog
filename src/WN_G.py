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

for i in idiomas:
    inicio = time.time()
    ruta = 'mcr\\'+i+'WN\wei_'+i+'-30_synset.tsv'
    print('Abriendo fichero ' + ruta)

    ficheroLectura = open(ruta,'r', encoding='utf-8')
    lineas = ficheroLectura.readlines()

    Synsets = []
    Glosas = []

    for linea in lineas:
        linea = linea.split('\t')
        synset = codificacionCategoria(linea[1])+linea[0][7:15]
        Synsets.append(int(synset))
        Glosas.append(linea[6].replace('\'','\'\''))
    
    df = pd.DataFrame({"Synset":Synsets, "Glosa":Glosas})
    df = df.sort_values(by=['Synset'])
    df = df.reset_index(drop = True)
    df.to_csv('src\DataFrames\dfG'+i+'.csv')

    ficheroEscritura = open(i+"\Prolog\wn_g.pl", "w", encoding='utf-8')

    for i in df.index:
        ficheroEscritura.write("g("+str(df["Synset"][i])+",\'"+str(df["Glosa"][i])+"\').\n")
    
    final = time.time()

    ficheroEscritura.close()
    ficheroLectura.close()

    print('Proceso en ruta: ' + ruta + ' finalizado. Ha tardado '+str(final-inicio)+'.\n')