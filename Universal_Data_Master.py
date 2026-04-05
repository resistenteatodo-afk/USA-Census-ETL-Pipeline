import os
import pandas as pd
from Document_Table_Parser import PDFTableExtractor
from Data_Refinery_Core import DataRefinery
from Smart_Memory_Optimizer import MemoryOptimizer
from Quality_Inspector import QualityInspector
from Database_Manager import DatabaseManager  # <-- El nuevo módulo SQL


def process_data(file_path):
    # 0. Verificación de seguridad
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        print(f"❌ Error: El archivo '{file_path}' no existe o está vacío.")
        return

    ext = os.path.splitext(file_path)[1].lower()
    print(f"🚀 INICIANDO PIPELINE ETL PROFESIONAL: {file_path}")

    # --- FASE 1: Extracción (Extraer) ---
    try:
        if ext == ".csv":
            df = pd.read_csv(
                file_path, sep=",", encoding="utf-8-sig", skipinitialspace=True
            )
            if len(df.columns) <= 1:
                # Modo rescate si las columnas vienen pegadas
                df_raw = pd.read_csv(file_path, header=None, encoding="utf-8-sig")
                df = df_raw[0].str.split(",", expand=True)
                df.columns = [str(c).strip() for c in df.iloc[0]]
                df = df[1:].reset_index(drop=True)
        elif ext == ".pdf":
            df = PDFTableExtractor.extract(file_path)
        else:
            print("❌ Formato no soportado.")
            return
    except Exception as e:
        print(f"⚠️ Error en lectura: {e}")
        return

    # --- FASE 2: Refinería y Purga (Transformar) ---
    cleaner = DataRefinery(df)
    df_clean = (
        cleaner.basic_clean()  # Espacios y duplicados
        .handle_missing()  # Rellenar nulos
        .remove_outliers()  # Purga estadística (los 216 osos)
        .get_result()
    )

    # --- FASE 3: Optimización y Calidad ---
    inspector = QualityInspector()
    outliers_restantes = inspector.detect_outliers(df_clean)
    df_final = MemoryOptimizer.optimize(df_clean)

    # --- FASE 4: Reporte Local (Excel) ---
    inspector.print_summary(df, df_final, outliers_restantes)

    nombre_excel = "REPORTE_FINAL_PURGADO.xlsx"
    df_final.to_excel(nombre_excel, index=False)
    print(f"📂 Reporte Excel generado: {nombre_excel}")

    # --- FASE 5: Carga en MySQL (Cargar) ---
    try:
        # CONFIGURACIÓN: Cambia 'tu_password' por tu clave real de MySQL
        db = DatabaseManager(
            user="root",
            password="thedria31",
            host="localhost",
            db_name="limpieza_datos",
        )
        # Subimos los datos a la tabla 'poblacion_usa'
        db.upload_data(df_final, "poblacion_usa")
    except Exception as e:
        print(f"⚠️ No se pudo cargar en MySQL. ¿Está el servidor encendido? Error: {e}")

    print(f"\n🔥 ¡PROCESO ETL FINALIZADO CON ÉXITO! 🔥")


if __name__ == "__main__":
    # Ejecutamos con el dataset pesado
    process_data("DATASET_EMERGENCIA.csv")
