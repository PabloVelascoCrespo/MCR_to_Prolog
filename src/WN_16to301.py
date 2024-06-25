import concurrent.futures
import pandas as pd

print("Opening WN files...")
wn_16 = open('WN16/data.noun', 'r', encoding = 'utf-8').readlines()[29:]
wn_30 = open('WN30/data.noun', 'r', encoding = 'utf-8').readlines()[29:]
print("WN files opened.")
print("Opening DataFrames...")
dfSynsets16AnCora = pd.read_csv('spa/PrologCSV/Tag_Count_AnCora.csv', encoding = 'utf-8', index_col=[0], dtype={'Synset16':'string'})
dfSynsets16WikiCorpus = pd.read_csv('spa/PrologCSV/Tag_Count_WikiCorpus.csv', encoding = 'utf-8', index_col=[0], dtype={'Synset16':'string'})
wn_16_DF = pd.read_csv("Words&Gloss16.csv", dtype={'Synset': str, 'Gloss': str}, index_col=[0])
wn_30_DF = pd.read_csv("Words&Gloss30.csv", dtype={'Synset': str, 'Gloss': str}, index_col=[0])
df = pd.read_csv('similarities_matrix.csv', dtype={'Synset16': str}, index_col='Synset16')
print("DataFrames opened.")

def codificacionNumero(c):
    numeros = {
        '0a':10,
        '0b':11,
        '0c':12,
        '0d':13,
        '0e':14,
        '0f':15,
        '0g':16,
        '0h':17,
        '0i':18,
        '0j':19,
        '0k':20,
        '0l':21,
        '0m':22,
        '0n':23,
        '0o':24,
        '0p':25,
        '1a':26,
        '1b':27,
        '1c':28,
        '1d':29,
        '1e':30
        }
    return numeros[c]

def calcular_similitud(row_label):
    if row_label not in df.index.tolist():
        print(f"Computing {row_label} synset.")
        words_16 = get_words(row_label, wn_16_DF)
        resultados = {}
        for col_label in df.columns:
            words_30 = get_words(col_label, wn_30_DF)
            resultados[col_label] = words_similarities(words_16, words_30)
        print(f"Synset {row_label} done.")
        return row_label, resultados
    return None

def get_sim_matrix(df, wn_16_synsets):
    try:
        # Crear un ThreadPoolExecutor con un número específico de hilos
        numero_hilos = 64

        # Diccionario para almacenar resultados
        resultados_completos = {}

        with concurrent.futures.ThreadPoolExecutor(max_workers=numero_hilos) as executor:
            # Ejecutar la función calcular_similitud en varios hilos
            futuros = {executor.submit(calcular_similitud, label): label for label in wn_16_synsets}

            # Obtener los resultados conforme se vayan completando
            for futuro in concurrent.futures.as_completed(futuros):
                label = futuros[futuro]
                try:
                    resultado = futuro.result()
                    if resultado is not None:
                        row_label, resultados = resultado
                        resultados_completos[row_label] = resultados
                except Exception as exc:
                    print(f'El hilo para {label} generó una excepción: {exc}')

    except KeyboardInterrupt:
        print("Exiting...")
    # Actualizar el DataFrame con los resultados
    for row_label, resultados in resultados_completos.items():
        for col_label, value in resultados.items():
            df.at[row_label, col_label] = value
    return df

def words_similarities(words_16, words_30):
    return round(2*common_words(words_16,words_30) / (len(words_16) + len(words_30)), 2)

def common_words(list1,list2):
    return len(set(list1).intersection(set(list2)))

def get_words(synset, wn):
    words = []
    row = wn[wn['Synset'] == synset]
    if not row.empty:
        return str(row['Words'].item()).split(" ")
    else:
        return None

def get_synset(wn30_line):
    return wn30_line.split(' ')[0]

wn_16_synsets_AnCora = dfSynsets16AnCora['Synset16'].to_list()
wn_16_synsets_WikiCorpus = dfSynsets16WikiCorpus['Synset16'].to_list()
wn_16_synsets_original = wn_16_synsets_AnCora + wn_16_synsets_WikiCorpus
wn_16_synsets = []
[wn_16_synsets.append(x) for x in wn_16_synsets_original if x not in wn_16_synsets]
wn_16_synsets = sorted(wn_16_synsets)
print("list created")

'''
wn_30_synsets = list(map(get_synset, wn_30))

df = pd.DataFrame(columns=wn_30_synsets)
print("dataframe creado")
print(df)
'''

print(df)

df = get_sim_matrix(df,wn_16_synsets)
print("matrix done")

df.to_csv("similarities_matrix.csv")
print("csv done")