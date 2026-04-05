import pandas as pd
import numpy as np


class QualityInspector:
    @staticmethod
    def detect_outliers(df):
        outliers_report = {}
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
            iqr = q3 - q1
            outliers = df[(df[col] < (q1 - 1.5 * iqr)) | (df[col] > (q3 + 1.5 * iqr))]
            if len(outliers) > 0:
                outliers_report[col] = len(outliers)
        return outliers_report

    @staticmethod
    def print_summary(df_ini, df_fin, outliers):
        print("\n" + "=" * 40)
        print("📊 REPORTE DE CALIDAD UNIVERSAL")
        print("=" * 40)
        print(f"✅ Filas procesadas: {len(df_ini)}")
        print(f"🧹 Filas finales:    {len(df_fin)}")
        print(f"🗑️  Filas eliminadas (Purga): {len(df_ini) - len(df_fin)}")
        print(f"🚨 Outliers restantes: {outliers if outliers else '0'}")
        print("=" * 40 + "\n")
