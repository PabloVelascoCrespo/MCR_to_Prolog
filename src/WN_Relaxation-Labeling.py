import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import MinMaxScaler

def normalizarFilas(df):
    scaler = MinMaxScaler()
    return pd.DataFrame(scaler.fit_transform(df.T).T, columns=df.columns, index=df.index).round(2)

def analizarDF(df):
    for index, row in df.iterrows():
        columnsDist0 = row[row != 0].index.tolist()
        if columnsDist0 != 0:
            for columnDist0 in columnsDist0:
                analizarGlosas(index, columnDist0)
                df.at[index, columnDist0] += analizarRelaciones(index, columnDist0)
    return df

def analizarGlosas(fila,columna):
    gloss16 = re.sub(r'[^\w\s]', '', wn_16_DF.loc[wn_16_DF['Synset'] == fila, 'Gloss'].values[0].split(";")[0]).split(" ")
    gloss30 = re.sub(r'[^\w\s]', '', wn_30_DF.loc[wn_30_DF['Synset'] == columna, 'Gloss'].values[0]).split(" ")
    df.at[fila, columna] += calcular_jaccard(gloss16, gloss30)
    return 0

def calcular_jaccard(words_16, words_30):
    return round(2*palabras_comunes(words_16,words_30) / (len(words_16) + len(words_30)), 2)

def palabras_comunes(list1,list2):
    return len(set(list1).intersection(set(list2)))

def analizarHiperonimos(df):
    return 0

def analizarRelaciones(fila,columna):
    if wn_16_DF.loc[wn_16_DF['Synset'] == fila, 'antonyms'].values[0] != wn_30_DF.loc[wn_30_DF['Synset'] == columna, 'antonyms'].values[0]:
        return -0.5
    if wn_16_DF.loc[wn_16_DF['Synset'] == fila, 'hypernyms'].values[0] != wn_30_DF.loc[wn_30_DF['Synset'] == columna, 'hypernyms'].values[0]:
        return -0.5
    if wn_16_DF.loc[wn_16_DF['Synset'] == fila, 'i_hypernyms'].values[0] != wn_30_DF.loc[wn_30_DF['Synset'] == columna, 'i_hypernyms'].values[0]:
        return -0.5
    if wn_16_DF.loc[wn_16_DF['Synset'] == fila, 'hyponym'].values[0] != wn_30_DF.loc[wn_30_DF['Synset'] == columna, 'hyponym'].values[0]:
        return -0.5
    if wn_16_DF.loc[wn_16_DF['Synset'] == fila, 'i_hyponym'].values[0] != wn_30_DF.loc[wn_30_DF['Synset'] == columna, 'i_hyponym'].values[0]:
        return -0.5
    if wn_16_DF.loc[wn_16_DF['Synset'] == fila, 'm_holonym'].values[0] != wn_30_DF.loc[wn_30_DF['Synset'] == columna, 'm_holonym'].values[0]:
        return -0.5
    if wn_16_DF.loc[wn_16_DF['Synset'] == fila, 's_holonym'].values[0] != wn_30_DF.loc[wn_30_DF['Synset'] == columna, 's_holonym'].values[0]:
        return -0.5
    if wn_16_DF.loc[wn_16_DF['Synset'] == fila, 'p_holonym'].values[0] != wn_30_DF.loc[wn_30_DF['Synset'] == columna, 'p_holonym'].values[0]:
        return -0.5
    if wn_16_DF.loc[wn_16_DF['Synset'] == fila, 'm_meronym'].values[0] != wn_30_DF.loc[wn_30_DF['Synset'] == columna, 'm_meronym'].values[0]:
        return -0.5
    if wn_16_DF.loc[wn_16_DF['Synset'] == fila, 's_meronym'].values[0] != wn_30_DF.loc[wn_30_DF['Synset'] == columna, 's_meronym'].values[0]:
        return -0.5
    if wn_16_DF.loc[wn_16_DF['Synset'] == fila, 'p_meronym'].values[0] != wn_30_DF.loc[wn_30_DF['Synset'] == columna, 'p_meronym'].values[0]:
        return -0.5
    if wn_16_DF.loc[wn_16_DF['Synset'] == fila, 'attribute'].values[0] != wn_30_DF.loc[wn_30_DF['Synset'] == columna, 'attribute'].values[0]:
        return -0.5
    if wn_16_DF.loc[wn_16_DF['Synset'] == fila, 'd_r_t'].values[0] != wn_30_DF.loc[wn_30_DF['Synset'] == columna, 'd_r_t'].values[0]:
        return -0.5
    return 0.5

def split_dataframe(df, chunk_size):
    for start in range(0, len(df), chunk_size):
        yield df[start:start + chunk_size]

# Crear una función para calcular la media ignorando los ceros
def media_sin_ceros(row):
    valores_no_cero = row[row != 0]
    if len(valores_no_cero) == 0:
        return 0  # Evitar la división por cero
    return valores_no_cero.mean()

def eliminar_inferiores_a_media_sin_ceros(row):
    mean = media_sin_ceros(row)
    return row.apply(lambda x: x if x >= mean else 0)

def reemplazar_negativos(valor):
    return 0 if valor < 0 else valor

print("Cargando los Dataframes...")
wn_16_DF = pd.read_csv("Words&Gloss16.csv", dtype={'Synset': str, 'Gloss': str}, index_col=[0])
wn_30_DF = pd.read_csv("Words&Gloss30.csv", dtype={'Synset': str, 'Gloss': str}, index_col=[0])
df = pd.read_csv('sim_matrix\sim_matrix[00001740-00059344].csv', dtype={'Synset16': str}, index_col='Synset16')
print("Dataframes cargados.")

print("Analizando el Dataframe...")
df = analizarDF(df)
print("Dataframe analizado.")

df = df.apply(lambda col: col.map(reemplazar_negativos))

print("Normalizando el Dataframe...")
df = normalizarFilas(df)
print("Dataframe normalizado.")

print("Eliminando valores inferiores a la media...")
df = df.apply(eliminar_inferiores_a_media_sin_ceros, axis=1)
print("Valores inferiores a la media eliminados.")

chunk_size = 150

for chunk in split_dataframe(df, chunk_size):
    start_idx = chunk.index[0]
    end_idx = chunk.index[-1]
    filename = f'sim_matrix/AAAA2.csv'
    print("Saving " + filename)
    chunk.to_csv(filename, index=True)