import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype


class MemoryOptimizer:
    @staticmethod
    def optimize(df):
        initial_mem = df.memory_usage().sum() / 1024**2
        for col in df.columns:
            if is_numeric_dtype(df[col]):
                c_min, c_max = df[col].min(), df[col].max()
                if np.issubdtype(df[col].dtype, np.integer):
                    if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                        df[col] = df[col].astype(np.int8)
                    elif (
                        c_min > np.iinfo(np.int16).min
                        and c_max < np.iinfo(np.int16).max
                    ):
                        df[col] = df[col].astype(np.int16)
                else:
                    df[col] = df[col].astype(np.float32)
            else:
                if df[col].nunique() / len(df[col]) < 0.5:
                    df[col] = df[col].astype("category")
        final_mem = df.memory_usage().sum() / 1024**2
        print(f"📉 Memoria: {initial_mem:.2f}MB -> {final_mem:.2f}MB")
        return df
