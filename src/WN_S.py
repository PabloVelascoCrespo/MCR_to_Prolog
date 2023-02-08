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

def contarSynsets(lista, e):
   contador=0
   for i in lista:
      if i == e:
         contador+=1
   return str(contador)

for i in idiomas:
    inicio = time.time()
    ruta = 'mcr\\'+i+'WN\wei_'+i+'-30_variant.tsv'
    print('Abriendo fichero ' + ruta)

    ficheroLectura = open(ruta,'r', encoding='utf-8')
    lineas = ficheroLectura.readlines()

    Synsets = []
    W_Nums = []
    Words = []
    Types = []
    Senses = []
    Tag_counts = []

    for linea in lineas:
        linea = linea.split('\t')
        synset = codificacionCategoria(linea[3])+linea[2][7:15]
        Synsets.append(int(synset))
        W_Nums.append(int(contarSynsets(Synsets,int(synset))))
        Words.append(linea[0].replace('\'','\'\'').replace('_',' '))
        Types.append(linea[3])
        Senses.append(linea[1])
        Tag_counts = 0

    df = pd.DataFrame({"Synset":Synsets, "W Num":W_Nums, "Word":Words, "Type":Types, "Sense":Senses, "Tag Count": Tag_counts})
    df = df.sort_values(by=['Synset','W Num'])
    df = df.reset_index(drop = True)
    df.to_csv('src\DataFrames/dfS'+i+'.csv')

    ficheroEscritura = open(i+"\Prolog\wn_s.pl", "w", encoding='utf-8')

    for i in df.index:
        ficheroEscritura.write("s("+str(df["Synset"][i])+","+str(df["W Num"][i])+",\'"+df["Word"][i]+"\',"+df["Type"][i]+","+str(df["Sense"][i])+","+str(df["Tag Count"][i])+").\n")

    ficheroEscritura.close()
    ficheroLectura.close()

    final = time.time()
    print('Proceso en ruta: ' + ruta + ' finalizado. Ha tardado '+str(final-inicio)+'.\n')

print('Todos los procesos finalizados satisfactoriamente.\n')