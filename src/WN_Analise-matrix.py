import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def normalizarFilas(df):
    scaler = MinMaxScaler()
    return pd.DataFrame(scaler.fit_transform(df.T).T, columns=df.columns, index=df.index)

def analizarFilas(df):
    list1to1 = []
    list1toN = []
    listNto1 = []
    listNtoM = []
    list1to0 = []
    
    df_nonzero = df.astype(bool)
    non_zero_counts = df_nonzero.sum(axis=1)
    
    print("Analizando las filas...")
    for index, row in df.iterrows():
        columnsDist0 = row[row != 0].index.tolist()
        if len(columnsDist0) == 0:
            list1to0.append([index, ""])
        elif len(columnsDist0) == 1:
            column = columnsDist0[0]
            valoresDist0Columna = df[df[column] != 0][column].index.tolist()
            if len(valoresDist0Columna) == 1:        # CASO 1:1 PURO
                list1to1.append([index, column])
            else:                                    # CASO N:1 PURO
                listAux3 = [[val, df.at[val, column]] for val in valoresDist0Columna]
                listNto1.append([listAux3, column])
        else:
            is1toN = all(df_nonzero[column].sum() == 1 for column in columnsDist0)
            listAux = [[column, df.at[index, column]] for column in columnsDist0]
            listAux2 = list(set(elem for column in columnsDist0 for elem in df[df[column] != 0][column].index.tolist()))
            if is1toN:                          # CASO 1:N PURO
                list1toN.append([index, listAux])
            else:                               # CASO N:M
                listNtoM.append([listAux2, listAux])
    
    return list1to1, list1toN, listNto1, listNtoM, list1to0

print("Cargando el DataFrame...")
df = pd.read_csv('similarities_matrix_normalized - pequeña.csv', dtype={'Synset16': str}, index_col='Synset16')
print("DataFrame cargado.")
print(df)

list1to1, list1toN, listNto1, listNtoM, list1to0 = analizarFilas(df)

print("Imprimiendo ficheros...")

output_dir = "lists/"
output_files = {
    "list1to1.txt": list1to1,
    "list1toN.txt": list1toN,
    "listNto1.txt": listNto1,
    "listNtoM.txt": listNtoM,
    "list1to0.txt": list1to0
}

for filename, data in output_files.items():
    with open(output_dir + filename, 'w') as archivo:
        for elemento in data:
            archivo.write("%s\n" % str(elemento))

print("Ficheros impresos.")
print("Proceso finalizado!")
