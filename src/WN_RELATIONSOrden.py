import pandas as pd

Relations = ["hyp","der","vgp","per","sim","sub","xphyp","rel","cat","rgloss","rterm","uterm","mm","mp","sa","bis","cau","fuz","ml","mmof","hp","m","in","ina","ind","ini","inl","inp","isd","itd","xpfuz","xpant","xpsim","near"]

for rel in Relations:

    fichero = open('spa\Prolog\wn_'+rel+'.pl','r', encoding='utf-8')
    lineas = fichero.readlines()

    df = pd.DataFrame()
    SynsetSource = []
    SynsetTarget = []
    W_NumSource = []
    W_NumTarget = []

    for linea in lineas:
        linea = linea[linea.find('('):linea.find(')')]
        linea = linea.split(',')
        if len(linea) == 2:
            SynsetSource.append(linea[0])
            SynsetTarget.append(linea[1])
        else:
            SynsetSource.append(linea[0])
            W_NumSource.append(linea[1])
            SynsetTarget.append(linea[2])
            W_NumTarget.append(linea[3])

    if W_NumSource == []:
        df = pd.DataFrame({"Synset Source":SynsetSource, "Synset Target":SynsetTarget})
        df = df.sort_values(by=["Synset Source", "Synset Target"])
        df = df.reset_index(drop = True)
        
        fichero.close()

        f = open("spa\Prolog\wn_"+rel+".pl", "w", encoding='utf-8')

        for i in df.index:
            f.write(rel+"("+str(df["Synset Source"][i])+","+str(df["Synset Target"][i])+").\n")

        f.close()
    else:
        df = pd.DataFrame({"Synset Source":SynsetSource, "W_Num Source": W_NumSource,"Synset Target":SynsetTarget, "W_Num Target": W_NumTarget})
        df = df.sort_values(by=["Synset Source", "Synset Target"])
        df = df.reset_index(drop = True)
        
        fichero.close()

        f = open("spa\Prolog\wn_"+rel+".pl", "w", encoding='utf-8')

        for i in df.index:
            f.write(rel+"("+str(df["Synset Source"][i])+","+str(df["W_Num Source"][i])+","+str(df["Synset Target"][i])+","+str(df["W_Num Target"][i])+").\n")
        f.close();

