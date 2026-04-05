import pandas as pd


def clean_census_2024():
    print("🧹 Modo Supervivencia: Extrayendo TODO...")

    # Leemos el archivo saltando la fila de basura
    df = pd.read_csv(
        "PEPCHARV2023.PEP_ALLDATA-Data.csv", skiprows=[1], low_memory=False
    )

    # Limpiamos el nombre: "Autauga County, Alabama" -> "Alabama"
    df["state_clean"] = df["NAME"].astype(str).apply(lambda x: x.split(",")[-1].strip())

    # Creamos el dataset sin filtrar nada más
    df_resultado = df[["state_clean", "YEAR", "POP"]].copy()
    df_resultado.columns = ["state/region", "year", "population"]

    # Guardamos
    df_resultado.to_csv("DATASET_2024_READY.csv", index=False)

    estados = df_resultado["state/region"].nunique()
    print(f"✅ ¡POR FIN! Se han encontrado {estados} entidades diferentes.")


if __name__ == "__main__":
    clean_census_2024()
