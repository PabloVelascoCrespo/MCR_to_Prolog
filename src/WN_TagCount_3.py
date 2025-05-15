import pandas as pd
import re

# Rutas de los CSVs y del fichero wn_s.pl
csv_files = ['csv1.csv', 'csv2.csv', 'csv3.csv']
wn_s_path = 'wn_s.pl'

# Leer CSVs con pandas
dfs = [pd.read_csv(f) for f in csv_files]

# Unificar columnas relevantes y normalizar
for df in dfs:
    df.columns = df.columns.str.strip().str.lower()
    df.rename(columns={
        'índice': 'index',
        'synset': 'synset',
        'categoría gramatical': 'pos',
        'palabra': 'lemma',
        'tagcount': 'tag_count'
    }, inplace=True)

# Combinar los tres CSVs haciendo un merge múltiple
df_merged = dfs[0].merge(dfs[1], on=['synset', 'pos', 'lemma'], suffixes=('_1', '_2')) \
                 .merge(dfs[2], on=['synset', 'pos', 'lemma'])
df_merged.rename(columns={'tag_count': 'tag_count_3'}, inplace=True)

# Calcular media aritmética del tag_count
df_merged['avg_tag_count'] = df_merged[['tag_count_1', 'tag_count_2', 'tag_count_3']].mean(axis=1).round().astype(int)

# Leer wn_s.pl
pattern = re.compile(r"s\((\d+),(\d+),'(.+?)',([a-z]),(\d+),(\d+)\)\.")
with open(wn_s_path, 'r', encoding='utf-8') as f:
    wn_lines = f.readlines()

# Extraer datos del wn_s.pl en un diccionario
wn_data = {}
for line in wn_lines:
    m = pattern.match(line.strip())
    if m:
        synset = int(m.group(1))
        lemma = m.group(3)
        pos = m.group(4)
        tag = int(m.group(6))
        key = (synset, pos, lemma)
        wn_data[key] = tag

# Comparar y mostrar
for _, row in df_merged.iterrows():
    key = (int(row['synset']), row['pos'], row['lemma'])
    if key in wn_data:
        original = wn_data[key]
        promedio = row['avg_tag_count']
        print(f"{key}: wn_s.pl = {original}, promedio = {promedio}")
