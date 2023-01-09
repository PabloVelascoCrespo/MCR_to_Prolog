import pandas as pd
import time
import os

idiomas = ['cat', 'eng', 'eus', 'glg', 'por', 'spa']
Relations = ["hyp","der","vgp","per","sim","sub","ant","xphyp","rel","cat","rgloss","rterm","uterm","mm","mp","sa","bis","cau","fuz","ml","mmof","hp","m","in","ina","ind","ini","inl","inp","isd","itd","xpfuz","xpant","xpsim","near"]

for i in idiomas:
    for rel in Relations:
        inicio = time.time()
        if not os.path.isfile(i+'\Prolog\wn_'+rel+'.pl'):
            break

        fichero = open(i+'\Prolog\wn_'+rel+'.pl','r', encoding='utf-8')
        print('Ordenando fichero: '+i+'\Prolog\wn_'+rel+'.pl')
        lineas = fichero.readlines()

        df = pd.DataFrame()
        SynsetSource = []
        SynsetTarget = []
        W_NumSource = []
        W_NumTarget = []

        for linea in lineas:
            linea = linea[linea.find('(')+1:linea.find(')')]
            linea = linea.split(',')
            if len(linea) == 2:
                SynsetSource.append(linea[0])
                SynsetTarget.append(linea[1])
            elif len(linea) == 4:
                SynsetSource.append(linea[0])
                W_NumSource.append(linea[1])
                SynsetTarget.append(linea[2])
                W_NumTarget.append(linea[3])
            else:
                break

        if W_NumSource == []:
            df = pd.DataFrame({"Synset Source":SynsetSource, "Synset Target":SynsetTarget})
            df = df.sort_values(by=["Synset Source", "Synset Target"])
            df = df.reset_index(drop = True)
            df.to_csv('src\DataFrames\dfRelations_'+i+'_'+rel+'.csv')

            fichero.close()

            f = open(i+"\Prolog\wn_"+rel+".pl", "w", encoding='utf-8')

            for index in df.index:
                f.write(rel+"("+str(df["Synset Source"][index])+","+str(df["Synset Target"][index])+").\n")

            f.close()
        else:
            df = pd.DataFrame({"Synset Source":SynsetSource, "W_Num Source": W_NumSource,"Synset Target":SynsetTarget, "W_Num Target": W_NumTarget})
            df = df.sort_values(by=["Synset Source", "Synset Target"])
            df = df.reset_index(drop = True)
            df.to_csv('src\DataFrames\dfRelations_'+i+'_'+rel+'.csv')

            fichero.close()

            f = open(i+"\Prolog\wn_"+rel+".pl", "w", encoding='utf-8')

            for index in df.index:
                f.write(rel+"("+str(df["Synset Source"][index])+","+str(df["W_Num Source"][index])+","+str(df["Synset Target"][index])+","+str(df["W_Num Target"][index])+").\n")
            f.close()
        
        final = time.time()
        print("Fichero "+i+"\Prolog\wn_"+rel+".pl finalizado. Se ha tardado: "+str(final-inicio))