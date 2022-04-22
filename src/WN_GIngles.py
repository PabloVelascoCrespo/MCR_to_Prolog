import time
import pandas as pd

pd.options.display.max_colwidth = 50000

start_time = time.time()

ficheroSRC = open('engProlog30\wn_g.pl','r', encoding='utf-8')
fichero = open('spa\Prolog\wn_g.pl','r', encoding='utf-8')
lineasSRC = ficheroSRC.readlines()
lineas = fichero.readlines()

Synsets = []
Glosa = []

for linea in lineas:
    linea = linea[2:-3]
    linea = linea.split(',')
    Synsets.append(int(linea[0]))
    if len(linea) == 2:
        Glosa.append(linea[1])
    else:
        cadena = "" 
        for a in linea[1:]:
            cadena+=a+","
        Glosa.append(cadena)

df = pd.DataFrame({"Synset":Synsets, "Glosa":Glosa})
df = df.sort_values(by='Synset')
df = df.reset_index(drop = True)

SynsetsSRC = []
GlosaSRC = []

for linea in lineasSRC:
    linea = linea[2:-3]
    linea = linea.split(',')
    SynsetsSRC.append(int(linea[0]))
    if len(linea) == 2:
        GlosaSRC.append(linea[1])
    else:
        cadena = "" 
        for a in linea[1:]:
            cadena+=a+","
        GlosaSRC.append(cadena)

dfSRC = pd.DataFrame({"Synset":SynsetsSRC, "Glosa":GlosaSRC})
dfSRC = dfSRC.sort_values(by='Synset')
dfSRC = dfSRC.reset_index(drop = True)

filtro = df['Glosa'] == "'None'"
dfNone = df[filtro]

#df = pd.read_csv('src\dfIngles.csv')
#dfNone = pd.read_csv('src\dfNone.csv')

Por = 10.0
cont = 0

for i in dfNone.index:
    aux = dfSRC[dfSRC['Synset'] == dfNone["Synset"][i]].copy()
    df['Glosa'][i] = aux["Glosa"].to_string(index=False)
    cont+=1
    if (cont/len(dfNone.index)*100 > Por - 1)&(cont/len(dfNone.index)*100 < Por + 1):
        print(Por, "%")
        Por+= 10

'''Por = 10.0
cont = 0

for i in dfNone.index:
    df['Glosa'][i] = translator.translate(df["Glosa"][i], dest = "es").text
    cont+=1
    if (cont/len(dfNone.index)*100 > Por - 1)&(cont/len(dfNone.index)*100 < Por + 1):
        print(Por, "%")
        Por+= 10
        df.to_csv("src/dfEspa.csv")'''

end_time = time.time()

print(end_time - start_time)

print(df.head(20))
print(df.tail(20))

df.to_csv('src\dfIngles.csv')

'''fichero.close()

f = open("spa\Prolog\wn_g.pl", "w", encoding='utf-8')

for i in df.index:
    f.write("g("+str(df["Synset"][i])+","+df["Glosa"][i]+").\n")
f.close()'''