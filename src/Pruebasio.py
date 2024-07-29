import pandas as pd

# Función para dividir el dataframe en partes más pequeñas
def split_dataframe(df, chunk_size):
    for start in range(0, len(df), chunk_size):
        yield df[start:start + chunk_size]

# Cargar el fichero CSV grande
print("Startig with chunks")
chunksize = 500
chunks = []
a = 1
for chunk in pd.read_csv('../sim_matrix/similarities_matrix - copia (3).csv', dtype={'Synset16': str}, index_col='Synset16', chunksize=chunksize):
    print("llevamos "+str(chunksize * a) +" líneas cargadas.")
    a = a+1
    chunks.append(chunk)

df = pd.concat(chunks, axis=0)
print("Chunks done.")

# Definir el tamaño de cada parte
chunk_size = 150

# Generar los dataframes pequeños y guardarlos en nuevos ficheros CSV
for chunk in split_dataframe(df, chunk_size):
    start_idx = chunk.index[0]
    end_idx = chunk.index[-1]
    filename = f'sim_matrix/sim_matrix[{start_idx}-{end_idx}].csv'
    print("Saving " + filename)
    chunk.to_csv(filename, index=True)

print("El fichero CSV ha sido dividido en partes más pequeñas.")