import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype


class DataRefinery:
    """Motor de limpieza profunda: elimina ruido, duplicados y outliers."""

    def __init__(self, df):
        self.df = df

    def basic_clean(self):
        """Limpia espacios en blanco en textos y luego elimina duplicados."""
        # 1. Quitamos espacios al inicio y final de cada celda de texto
        for col in self.df.columns:
            if self.df[col].dtype == "object":
                self.df[col] = self.df[col].str.strip()

        # 2. Ahora que el texto está limpio, borramos las filas repetidas
        self.df = self.df.drop_duplicates()
        return self

    def handle_missing(self):
        """Rellena valores vacíos (NaN) de forma inteligente según el tipo de dato."""
        for col in self.df.columns:
            if is_numeric_dtype(self.df[col]):
                # Si es número, ponemos 0 para no romper cálculos estadísticos
                self.df[col] = self.df[col].fillna(0)
            else:
                # Si es texto, ponemos 'N/A' (Not Available)
                self.df[col] = self.df[col].fillna("N/A")
        return self

    def remove_outliers(self):
        """Identifica y ELIMINA las filas que tengan valores estadísticamente imposibles."""
        # Solo analizamos columnas con números
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            # Calculamos los cuartiles y el rango intercuartílico (IQR)
            q1 = self.df[col].quantile(0.25)
            q3 = self.df[col].quantile(0.75)
            iqr = q3 - q1

            # Definimos los límites de 'normalidad'
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            # FILTRADO: Mantenemos solo las filas que están DENTRO de los límites
            # Usamos .copy() para que Pandas trabaje de forma más rápida y segura
            self.df = self.df[
                (self.df[col] >= lower_bound) & (self.df[col] <= upper_bound)
            ].copy()

        return self

    def get_result(self):
        """Devuelve el DataFrame final totalmente purificado."""
        return self.df
