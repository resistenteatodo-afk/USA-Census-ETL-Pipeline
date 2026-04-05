import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:Thedria31@localhost/limpieza_datos")
df = pd.read_sql("SELECT * FROM poblacion_usa LIMIT 1", engine)
print("🔍 Tus columnas se llaman exactamente así:")
print(df.columns.tolist())
