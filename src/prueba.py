import pandas as pd

idiomas = ['cat', 'eng', 'eus', 'glg', 'por', 'spa']
relacionesLexicas = ['ant', 'der', 'vgp', 'per', 'sa']

def metodo(synset):
    if synset in List:
        return 1
    else:
        return 0

for i in idiomas:
    dfS = pd.read_csv(i+'//PrologCSV//wn_s.csv', index_col=[0])
    for rel in relacionesLexicas:
        dfRel = pd.read_csv(i+'//PrologCSV//wn_'+rel+'.csv', index_col=[0])

        Synsets_count = dfS.Synset.value_counts()
        Synsets_count_1 = Synsets_count[(Synsets_count == 1)]
        List = list(Synsets_count_1.index)

        dfRel['W_Num Source'] = dfRel['Synset Source'].apply(metodo)
        dfRel['W_Num Target'] = dfRel['Synset Target'].apply(metodo)

        dfRel.to_csv(i+'//PrologCSV//wn_'+rel+'.csv')
        ficheroEscritura = open(i+"\Prolog\wn_"+rel+".pl", "w", encoding='utf-8')

        for index in dfRel.index:
                ficheroEscritura.write(rel+"("+str(dfRel["Synset Source"][index])+","+str(dfRel["W_Num Source"][index])+","+str(dfRel["Synset Target"][index])+","+str(dfRel["W_Num Target"][index])+").\n")
        ficheroEscritura.close()

        print("Se ha terminado de ejecutar el fichero: wn_"+rel+" del idioma "+i)
    print("Se ha terminado de ejecutar el idioma: "+i+"\n")
    