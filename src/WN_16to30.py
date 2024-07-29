import pandas as pd
import os
import re

print("Opening WN files...")
wn_16 = open('WN16/data.noun', 'r', encoding = 'utf-8').readlines()[29:]
wn_30 = open('WN30/data.noun', 'r', encoding = 'utf-8').readlines()[29:]
folder = "sim_matrix"
files = os.listdir(folder)
pattern = re.compile(r'sim_matrix\[(\d+)-(\d+)\].csv')
end_indices = []
last_index = ""
for file in files:
    match = pattern.match(file)
    if match:
        end_index = match.group(2)
        end_indices.append(end_index)

if end_indices:
    last_index = max(end_indices)
    print(f"El último índice procesado es: {last_index}")
else:
    print("No se encontraron ficheros con el formato esperado.")

print("WN files opened.")

print("Opening DataFrames...")
dfSynsets16AnCora = pd.read_csv('spa/PrologCSV/Tag_Count_AnCora.csv', encoding = 'utf-8', index_col=[0], dtype={'Synset16':'string'})
dfSynsets16WikiCorpus = pd.read_csv('spa/PrologCSV/Tag_Count_WikiCorpus.csv', encoding = 'utf-8', index_col=[0], dtype={'Synset16':'string'})
wn_16_DF = pd.read_csv("Words&Gloss16.csv", dtype={'Synset': str, 'Gloss': str}, index_col=[0])
wn_30_DF = pd.read_csv("Words&Gloss30.csv", dtype={'Synset': str, 'Gloss': str}, index_col=[0]) 
df = pd.read_csv('Collab Files/DataFrame.csv', dtype={'Synset16': str}, index_col='Synset16')
df.drop(df.index[0], inplace=True)
print("DataFrames opened.")

def split_dataframe(df, chunk_size):
    for start in range(0, len(df), chunk_size):
        yield df[start:start + chunk_size]

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

def get_sim_matrix(df, wn_16_synsets):
    wn_16_DF = pd.read_csv("Words&Gloss16.csv", dtype={'Synset': str, 'Gloss': str}, index_col=[0])
    wn_30_DF = pd.read_csv("Words&Gloss30.csv", dtype={'Synset': str, 'Gloss': str}, index_col=[0])
    try:
        for row_label in wn_16_synsets:
            if row_label not in df.index.tolist():
                print("Computing " + row_label + " synset.")
                words_16 = get_words(row_label,wn_16_DF)
                for col_label in df.columns:
                    words_30 = get_words(col_label,wn_30_DF)
                    df.at[row_label, col_label] = calcular_jaccard(words_16, words_30)
                print("Synset " + row_label + " done.")
    except KeyboardInterrupt:
        print("Exiting...")
    return df

def calcular_jaccard(words_16, words_30):
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

print("Starting from " + str(wn_16_synsets.index(last_index))+ " position.")

df = get_sim_matrix(df,wn_16_synsets[wn_16_synsets.index(last_index):])
print("matrix done")

chunk_size = 150

for chunk in split_dataframe(df, chunk_size):
    start_idx = chunk.index[0]
    end_idx = chunk.index[-1]
    filename = f'sim_matrix/sim_matrix[{start_idx}-{end_idx}].csv'
    print("Saving " + filename)
    chunk.to_csv(filename, index=True)

print("csv done")
