import sys
import pandas as pd
import unicodedata
import os

def normalizar(palabra):
    """
    - Elimina comillas exteriores (', ", ‘ ’, “ ”, ` `)
    - Quita tildes
    - Pone en minúsculas
    """
    if pd.isna(palabra):
        return ""

    s = str(palabra).strip()

    # --- 1. Eliminar comillas exteriores ---
    quote_pairs = [
        ("'", "'"),
        ('"', '"'),
        ("‘", "’"),
        ("“", "”"),
        ("`", "`")
    ]

    if len(s) >= 2:
        for q1, q2 in quote_pairs:
            if s.startswith(q1) and s.endswith(q2):
                s = s[1:-1].strip()
                break

        # Caso genérico: empieza y acaba con algún tipo de comilla
        if (s[0] in "\"'`“”‘’") and (s[-1] in "\"'`“”‘’"):
            s = s[1:-1].strip()

    # --- 2. Quitar tildes y pasar a minúsculas ---
    s = ''.join(
        c for c in unicodedata.normalize('NFD', s.lower())
        if unicodedata.category(c) != 'Mn'
    )

    return s

def main():
    # --- 0. Comprobar argumentos ---
    if len(sys.argv) < 2:
        print("Uso: python asignar_synsets.py <fichero_Tag_Count.csv>")
        sys.exit(1)

    fichero_entrada = sys.argv[1]

    if not os.path.exists(fichero_entrada):
        print(f"❌ Error: no se encuentra el fichero '{fichero_entrada}'")
        sys.exit(1)

    # Nombres de salida derivados del nombre base
    base = os.path.splitext(os.path.basename(fichero_entrada))[0]
    fichero_salida = f"{base}_new.csv"
    fichero_reporte = f"Reporte_{base}.csv"

    # --- 1. Cargar ficheros ---
    corpus = pd.read_csv(fichero_entrada)
    wn = pd.read_csv("spa/PrologCSV/wn_s.csv")

    # --- 2. Normalizar ---
    wn["Word_norm"] = wn["Word"].apply(normalizar)
    corpus["Word_norm"] = corpus["Word"].apply(normalizar)

    # --- 3. Crear diccionario palabra → lista de synsets ---
    dic_synsets = (
        wn.groupby("Word_norm")["Synset"]
          .apply(lambda x: sorted(set(x)))
          .to_dict()
    )

    # --- 4. Procesar bloques consecutivos ---
    reporte = []
    corpus_new = corpus.copy()

    i = 0
    n = len(corpus)
    total_notfound = (corpus["Synset"] == "1Synset Not Found").sum()
    actualizados = 0

    while i < n:
        fila = corpus.iloc[i]
        if fila["Synset"] == "1Synset Not Found":
            # inicio del bloque
            inicio = i
            while i + 1 < n and corpus.iloc[i + 1]["Synset"] == "1Synset Not Found":
                i += 1
            fin = i

            # Palabras del bloque
            bloque = corpus.iloc[inicio:fin + 1]
            palabras = bloque["Word_norm"].tolist()

            # Synsets posibles por palabra
            sets_por_palabra = [set(dic_synsets.get(p, [])) for p in palabras if p in dic_synsets]

            if not sets_por_palabra:
                # Ninguna palabra encontrada
                for j, palabra in zip(bloque.index, bloque["Word"]):
                    reporte.append({
                        "Índice": j,
                        "Word": palabra,
                        "Num_Synsets": 0,
                        "Posibles_Synsets": "[]"
                    })
            else:
                # Synset(s) comunes entre todas las palabras encontradas
                synsets_comunes = set.intersection(*sets_por_palabra) if len(sets_por_palabra) > 1 else sets_por_palabra[0]

                if len(synsets_comunes) == 1:
                    # Caso ideal → asignar el synset común
                    synset_val = list(synsets_comunes)[0]
                    corpus_new.loc[inicio:fin, "Synset"] = synset_val
                    actualizados += (fin - inicio + 1)
                else:
                    # Ambigüedad o sin intersección → se reporta
                    for j, palabra in zip(bloque.index, bloque["Word"]):
                        posibles = sorted(dic_synsets.get(normalizar(palabra), []))
                        reporte.append({
                            "Índice": j,
                            "Word": palabra,
                            "Num_Synsets": len(posibles),
                            "Posibles_Synsets": posibles
                        })
        i += 1

    # --- 5. Eliminar columna auxiliar antes de guardar ---
    corpus_new = corpus_new.drop(columns=["Word_norm"])

    # --- 6. Guardar resultados ---
    corpus_new.to_csv(fichero_salida, index=False)
    pd.DataFrame(reporte).to_csv(fichero_reporte, index=False)

    # --- 7. Mostrar resumen final ---
    reportados = len(reporte)
    print("\n✅ PROCESO FINALIZADO\n")
    print(f"• Fichero de entrada: {fichero_entrada}")
    print(f"• Total de registros: {n}")
    print(f"• Registros con '1Synset Not Found': {total_notfound}")
    print(f"• Registros actualizados con un synset válido: {actualizados}")
    print(f"• Registros sin resolver (reporte): {reportados}")
    print("\nArchivos generados:")
    print(f"  - {fichero_salida}")
    print(f"  - {fichero_reporte}")

if __name__ == "__main__":
    main()
