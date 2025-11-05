import pandas as pd

# 1️⃣ Archivos de entrada y salida
input_file = "spa/PrologCSV/wn_s.csv"
output_file = "spa/Prolog/wn_s.pl"

# 2️⃣ Cargar el CSV
df = pd.read_csv(input_file, dtype={'Synset': str})

# 3️⃣ Generar los hechos Prolog
with open(output_file, "w", encoding="utf-8") as f:
    for _, row in df.iterrows():
        synset = row["Synset"]
        wnum = row["W Num"]
        tipo = row["Type"]
        sense = row["Sense"]
        tagcount = row["Tag Count"]

        # Convertir 'Word' a cadena (por si contiene NaN o número)
        word = str(row["Word"]).strip()

        # Escapar comillas simples en la palabra
        word_safe = word.replace("'", "")

        # Escribir el hecho Prolog
        f.write(f"s({synset},{wnum},'{word_safe}',{tipo},{sense},{tagcount}).\n")

print(f"✅ Fichero '{output_file}' generado correctamente con hechos Prolog y comentario inicial.")
