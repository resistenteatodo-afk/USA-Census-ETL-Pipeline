import pandas as pd
from Data_Refinery_Core import DataRefinery
from Smart_Memory_Optimizer import MemoryOptimizer


def run_cleaning_pipeline(input_csv, output_name="datos_limpios_pro.csv"):
    print(f"🚀 Iniciando proceso para: {input_csv}")

    # Intentamos las 3 codificaciones más comunes en el mundo real
    # Intentamos las codificaciones en este orden específico para Windows
    encodings = ["utf-16", "utf-8", "latin1"]
    df_raw = None

    for enc in encodings:
        try:
            # Añadimos 'sep=None' para que Pandas detecte si es coma o punto y coma solo
            df_raw = pd.read_csv(input_csv, encoding=enc, sep=None, engine="python")
            print(f"✅ Archivo leído correctamente con: {enc}")
            break
        except:
            continue

    if df_raw is None:
        print("❌ Error: No se pudo leer el archivo. Revisa el formato.")
        return

    # Fase 1: Limpieza profunda
    refinery = DataRefinery(df_raw)
    df_clean = refinery.basic_clean().handle_missing().get_result()

    # Fase 2: Optimización (Ahora blindada contra strings)
    df_final = MemoryOptimizer.optimize(df_clean)

    # Fase 3: Guardado
    df_final.to_csv(output_name, index=False, encoding="utf-8")
    print(f"✅ ¡Éxito! Resultado en: {output_name}")


if __name__ == "__main__":
    run_cleaning_pipeline("ejemplo.csv")
