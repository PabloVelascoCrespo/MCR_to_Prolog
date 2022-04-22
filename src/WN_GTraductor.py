from operator import le
import time
import pandas as pd
from googletrans import Translator

start_time = time.time()

pd.options.display.max_colwidth = 50000

translator = Translator()

df = pd.read_csv('src\dfEspa.csv', index_col = [0])
dfNone = pd.read_csv('src\dfNone.csv', index_col = [0])

Por = 10.0
cont = 0

for i in dfNone.index:
    df['Glosa'][i] = translator.translate(df["Glosa"][i], dest = "es").text
    cont+=1
    print(cont)
    if (cont/len(dfNone.index)*100 > Por - 1)&(cont/len(dfNone.index)*100 < Por + 1):
        print(Por, "%")
        Por+= 10
        df.to_csv("src/dfEspa.csv")

df.to_csv("src/dfEspa.csv")

end_time = time.time()

print(end_time - start_time)

f = open("spa\Prolog\wn_g.pl", "w", encoding='utf-8')

for i in df.index:
    if df["Glosa"][i][0] == "'":
        if df["Glosa"][i][-1] == "'":
            f.write("g("+str(df["Synset"][i])+","+str(df["Glosa"][i])+").\n")
        else:
            f.write("g("+str(df["Synset"][i])+","+str(df["Glosa"][i])+"').\n")
    else:
        if df["Glosa"][i][-1] == "'":
            f.write("g("+str(df["Synset"][i])+",'"+str(df["Glosa"][i])+").\n")
        else:
            f.write("g("+str(df["Synset"][i])+",'"+str(df["Glosa"][i])+"').\n")

f.close()