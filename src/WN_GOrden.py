import pandas as pd

fichero = open('spa\Prolog\wn_g.pl','r', encoding='utf-8')
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

fichero.close()

f = open("spa\Prolog\wn_g.pl", "w", encoding='utf-8')

for i in df.index:
    f.write("g("+str(df["Synset"][i])+","+str(df["Glosa"][i])+").\n")

f.close()
