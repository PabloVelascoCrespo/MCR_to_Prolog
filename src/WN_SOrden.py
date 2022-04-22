import pandas as pd

fichero = open('spa\Prolog\wn_s.pl','r', encoding='utf-8')
lineas = fichero.readlines()

Synsets = []
W_Nums = []
Words = []
Types = []
Senses = []

for linea in lineas:
    linea = linea[2:-3]
    linea = linea.split(',')
    if len(linea) == 7:
        Synsets.append(int(linea[0]))
        W_Nums.append(int(linea[1]))
        Words.append(linea[2]+linea[3])
        Types.append(linea[4])
        Senses.append(int(linea[5]))
    else:
        Synsets.append(int(linea[0]))
        W_Nums.append(int(linea[1]))
        Words.append(linea[2])
        Types.append(linea[3])
        Senses.append(int(linea[4]))

df = pd.DataFrame({"Synset":Synsets, "W Num":W_Nums, "Word":Words, "Type":Types, "Sense":Senses})
df = df.sort_values(by=['Synset','W Num'])
df = df.reset_index(drop = True)

fichero.close()

f = open("spa\Prolog\wn_s.pl", "w", encoding='utf-8')

for i in df.index:
    f.write("s("+str(df["Synset"][i])+","+str(df["W Num"][i])+","+df["Word"][i]+","+df["Type"][i]+","+str(df["Sense"][i])+",0).\n")

f.close()