import pandas as pd
import time

idiomas = ['cat', 'eng', 'eus', 'glg', 'por', 'spa']

relaciones = {
    '12':['hyp',1],'33':['ant',2],'31':['der',2],'52':['vgp',4],'47':['per',4],'34':['sim',3],'19':['sub',1],'21':['xphyp',1],'64':['rel',3],
    '63':['cat',1],'61':['rgloss',3],'66':['rterm',3],'68':['uterm',3],'7':['mm',3],'8':['mp',3],'49':['sa',4],'1':['bis',3],
    '2':['cau',3],'3':['fuz',3],'5':['ml',1],'6':['ms',3],'9':['hp',3],'10':['m',1],'35':['in',1],'36':['ina',1],
    '37':['ind',1],'38':['ini',1],'39':['inl',1],'40':['inp',1],'41':['isd',1],'42':['itd',1],'44':['xpfuz',3],'45':['xpant',3],
    '46':['xpsim',3],'60':['near',3]
    }

def codificacionCategoria(c):
    categorias = {
        'n':'1',
        'v':'2',
        'a':'3',
        'r':'4'
        }
    return categorias[c]

def crearSynsetID(synset):
    synset = codificacionCategoria(synset[-1])+synset[7:15]
    return int(synset)

def crearDF(key, df):
    dfAux = df[df['Rel_ID'] == int(key)]
    if not(dfAux.empty):
        if relaciones[key][1] == 1:
            dfAux = dfAux.drop(columns = ['Rel_ID'])
            dfAux = dfAux[['Synset_Target', 'Synset_Source']]
            dfAux.rename(columns = { 'Synset_Target': 'Synset Source', 'Synset_Source': 'Synset Target'}, inplace = True)

            dfAux = dfAux.sort_values(by=['Synset Source', 'Synset Target'])
            dfAux = dfAux.reset_index(drop = True)

            dfAux.to_csv(i+"\PrologCSV\wn_"+relaciones[key][0]+".csv")

            ficheroEscritura = open(i+"\Prolog\wn_"+relaciones[key][0]+".pl", "w", encoding='utf-8')
            for index in dfAux.index:
                ficheroEscritura.write(relaciones[key][0]+"("+str(dfAux["Synset Source"][index])+","+str(dfAux["Synset Target"][index])+").\n")
            ficheroEscritura.close()

        if relaciones[key][1] == 2:
            dfAux = dfAux.drop(columns = ['Rel_ID'])

            W_Num = [0] * len(dfAux['Synset_Target'])
            dfAux['W_Num Source'] = W_Num
            dfAux['W_Num Target'] = W_Num

            dfAux.rename(columns = { 'Synset_Target': 'Synset Source', 'Synset_Source': 'Synset Target'}, inplace = True)
            dfAux = dfAux[['Synset Source', 'W_Num Source', 'Synset Target', 'W_Num Target']]

            dfAux = dfAux.sort_values(by=['Synset Source', 'Synset Target'])
            dfAux = dfAux.reset_index(drop = True)

            dfAux.to_csv(i+"\PrologCSV\wn_"+relaciones[key][0]+".csv")

            ficheroEscritura = open(i+"\Prolog\wn_"+relaciones[key][0]+".pl", "w", encoding='utf-8')
            for index in dfAux.index:
                ficheroEscritura.write(relaciones[key][0]+"("+str(dfAux["Synset Source"][index])+",0,"+str(dfAux["Synset Target"][index])+",0).\n")
            ficheroEscritura.close()
            
        if relaciones[key][1] == 3:
            dfAux = dfAux.drop(columns = ['Rel_ID'])
            dfAux.rename(columns = { 'Synset_Source': 'Synset Source', 'Synset_Target': 'Synset Target'}, inplace = True)

            dfAux = dfAux.sort_values(by=['Synset Source', 'Synset Target'])
            dfAux = dfAux.reset_index(drop = True)

            dfAux.to_csv(i+"\PrologCSV\wn_"+relaciones[key][0]+".csv")
            
            ficheroEscritura = open(i+"\Prolog\wn_"+relaciones[key][0]+".pl", "w", encoding='utf-8')
            for index in dfAux.index:
                ficheroEscritura.write(relaciones[key][0]+"("+str(dfAux["Synset Source"][index])+","+str(dfAux["Synset Target"][index])+").\n")
            ficheroEscritura.close()

        if relaciones[key][1] == 4:
            dfAux = dfAux.drop(columns = ['Rel_ID'])

            W_Num = [0] * len(dfAux['Synset_Target'])
            dfAux['W_Num Source'] = W_Num
            dfAux['W_Num Target'] = W_Num

            dfAux.rename(columns = { 'Synset_Source': 'Synset Source', 'Synset_Target': 'Synset Target'}, inplace = True)
            dfAux = dfAux[['Synset Source', 'W_Num Source', 'Synset Target', 'W_Num Target']]

            dfAux = dfAux.sort_values(by=['Synset Source', 'Synset Target'])
            dfAux = dfAux.reset_index(drop = True)

            dfAux.to_csv(i+"\PrologCSV\wn_"+relaciones[key][0]+".csv")

            ficheroEscritura = open(i+"\Prolog\wn_"+relaciones[key][0]+".pl", "w", encoding='utf-8')
            for index in dfAux.index:
                ficheroEscritura.write(relaciones[key][0]+"("+str(dfAux["Synset Source"][index])+",0,"+str(dfAux["Synset Target"][index])+",0).\n")
            ficheroEscritura.close()

# 1: 2 datos del revés

# 2: 4 datos del revés

# 3: 2 datos del derecho

# 4: 4 datos del derecho

for i in idiomas:
    inicio = time.time()
   
    ruta = "mcrCSV//"+i+"WN\wei_"+i+"-30_relation.csv"
    print("Leyendo dataframe "+ ruta)
    
    df = pd.read_csv(ruta, index_col=[0])
    df = df.drop(columns=['S_PoS', 'T_PoS', 'Conf', 'Info'])

    df.columns = ['Rel_ID', 'Synset_Source', 'Synset_Target']

    df['Synset_Source'] = df['Synset_Source'].apply(crearSynsetID)
    df['Synset_Target'] = df['Synset_Target'].apply(crearSynsetID)

    keys = relaciones.keys()

    for key in keys:
        print('Se está traduciendo la relación: '+relaciones[key][0])
        crearDF(key, df)

    final = time.time()
    print('Proceso en ruta: ' + ruta + ' finalizado. Ha tardado '+str(final-inicio)+'.\n')
    