from sqlalchemy import create_engine
import pandas as pd


class DatabaseManager:
    def __init__(self, user, password, host, db_name):
        # Creamos la conexión (reemplaza con tus datos reales)
        self.connection_str = f"mysql+pymysql://{user}:{password}@{host}/{db_name}"
        self.engine = create_engine(self.connection_str)

    def upload_data(self, df, table_name):
        """Sube el DataFrame limpio a MySQL. Si la tabla existe, la reemplaza."""
        try:
            print(f"🗄️ Subiendo {len(df)} filas a la tabla '{table_name}'...")
            df.to_sql(
                name=table_name, con=self.engine, if_exists="replace", index=False
            )
            print("✅ ¡Datos cargados en MySQL con éxito!")
        except Exception as e:
            print(f"❌ Error al subir a la base de datos: {e}")
