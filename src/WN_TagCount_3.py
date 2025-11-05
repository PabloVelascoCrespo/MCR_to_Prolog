import pandas as pd
from collections import defaultdict

def normalize_word(s):
    if pd.isna(s):
        return s
    s = str(s).strip()
    quote_pairs = [("'", "'"), ('"', '"'), ("‘", "’"), ("“", "”"), ("`", "`")]
    if len(s) >= 2:
        for left, right in quote_pairs:
            if s.startswith(left) and s.endswith(right):
                return s[1:-1].strip()
        if (s[0] in "\"'`“”‘’") and (s[-1] in "\"'`“”‘’"):
            return s[1:-1].strip()
    return s

def add_quotes(s):
    if pd.isna(s):
        return s
    s = str(s).strip()
    if not (s.startswith("'") and s.endswith("'")):
        return f"'{s}'"
    return s

def normalize_synset(x):
    return None if pd.isna(x) else str(x).strip()


# ======================
# CARGA CSVs
# ======================

path_main = "spa/PrologCSV/wn_s.csv"
paths_other = [
    "spa/PrologCSV/Tag_Count_AnCora30.csv",   # CSV1
    "spa/PrologCSV/Tag_Count_SenSem.csv",     # CSV2 ✅ especial para Type!=n
    "spa/PrologCSV/Tag_Count_WikiCorpus30.csv" # CSV3
]

df_main = pd.read_csv(path_main)
dfs_other = [pd.read_csv(p) for p in paths_other]

df1, df2, df3 = dfs_other   # nombres claros


# ======================
# Normalizar
# ======================

df_main["Synset"] = df_main["Synset"].apply(normalize_synset)
df_main["Word"]   = df_main["Word"].apply(normalize_word)
df_main["Tag Count"] = pd.to_numeric(df_main["Tag Count"], errors="coerce").fillna(0)

for df in (df1, df2, df3):
    df["Synset"] = df["Synset"].apply(normalize_synset)
    df["Word"]   = df["Word"].apply(normalize_word)
    df["Tag Count"] = pd.to_numeric(df["Tag Count"], errors="coerce").fillna(0)


# ======================
# ✅ PESOS PARA type=="n" (SenSem solo sustantivos)
# ======================

# ✅ Solo filas donde SenSem.PoS == 'n'
sen_sem_nouns = df2[df2["PoS"] == "n"]

weights = [
    len(df1),            # AnCora30 completo
    len(sen_sem_nouns),  # ✅ SenSem: SOLO sustantivos
    len(df3)             # WikiCorpus completo
]

total_weight = sum(weights)
w1, w2, w3 = [w / total_weight for w in weights]


# ======================
# CALCULO DE TAG COUNT
# ======================

new_tagcounts = {}

for idx, row in df_main.iterrows():
    synset = row["Synset"]
    word   = row["Word"]
    tipo   = row["Type"]

    # ✅ REGLA: Si no es 'n', usar SOLO SenSem (sin ponderar)
    if tipo != "n":
        match = df2[(df2["Synset"] == synset) & (df2["Word"] == word)]
        if not match.empty:
            new_tagcounts[idx] = int(match["Tag Count"].iloc[0])
        else:
            new_tagcounts[idx] = 0
        continue

    # ✅ Si sí es 'n', usar ponderación normal
    weighted_sum = 0
    any_found = False

    # CSV1 (AnCora)
    match1 = df1[(df1["Synset"] == synset) & (df1["Word"] == word)]
    if not match1.empty:
        weighted_sum += match1["Tag Count"].iloc[0] * w1
        any_found = True

    # CSV2 (SenSem)
    match2 = sen_sem_nouns[(sen_sem_nouns["Synset"] == synset) & (sen_sem_nouns["Word"] == word)]
    if not match2.empty:
        weighted_sum += match2["Tag Count"].iloc[0] * w2
        any_found = True

    # CSV3 (WikiCorpus)
    match3 = df3[(df3["Synset"] == synset) & (df3["Word"] == word)]
    if not match3.empty:
        weighted_sum += match3["Tag Count"].iloc[0] * w3
        any_found = True

    new_tagcounts[idx] = int(round(weighted_sum)) if any_found else 0


# ======================
# Guardar resultados en columnas
# ======================

df_main["Tag Count"] = df_main.index.map(lambda i: new_tagcounts[i])
df_main["Word"] = df_main["Word"].apply(add_quotes)


# ======================
# REORDENAR Y REGENERAR W Num
# ======================

df_main = df_main.sort_values(
    by=["Synset", "Tag Count"],
    ascending=[True, False]
)

df_main["W Num"] = df_main.groupby("Synset").cumcount() + 1


# ======================
# Guardar archivo
# ======================

df_main.to_csv(path_main, index=False)
print("\n✅ CSV actualizado ✅ Pesos corregidos (SenSem solo sustantivos) ✅\n")
