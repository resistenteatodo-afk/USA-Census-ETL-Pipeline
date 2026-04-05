import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

# Diccionario de traducción (Sigla -> Nombre Completo)
mapeo_estados = {
    "AK": "Alaska",
    "AL": "Alabama",
    "AR": "Arkansas",
    "AZ": "Arizona",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DC": "District of Columbia",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "IA": "Iowa",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "MA": "Massachusetts",
    "MD": "Maryland",
    "ME": "Maine",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MO": "Missouri",
    "MS": "Mississippi",
    "MT": "Montana",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "NE": "Nebraska",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NV": "Nevada",
    "NY": "New York",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VA": "Virginia",
    "VT": "Vermont",
    "WA": "Washington",
    "WI": "Wisconsin",
    "WV": "West Virginia",
    "WY": "Wyoming",
}

USER = "root"
PASSWORD = "thedria31"
HOST = "localhost"
DB_NAME = "limpieza_datos"

engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DB_NAME}")


import matplotlib.ticker as ticker  # <--- Asegúrate de que esta línea esté arriba


def generate_chart():
    print("📊 Generando gráfico con etiquetas detalladas...")

    query = """
    SELECT `state/region` AS estado, SUM(population) as poblacion
    FROM poblacion_usa 
    WHERE year = 2023 
    GROUP BY `state/region`
    ORDER BY poblacion DESC 
    LIMIT 10;
    """

    try:
        df = pd.read_sql(query, engine)

        plt.figure(figsize=(12, 8))
        sns.set_theme(style="whitegrid")

        # Guardamos el gráfico en una variable 'ax' para poder tunearlo
        ax = sns.barplot(
            data=df,
            x="poblacion",
            y="estado",
            palette="magma",
            hue="estado",
            legend=False,
        )

        # 🎯 EL SECRETO PARA LOS NÚMEROS ESPECÍFICOS:
        # Esto pone separadores de miles y quita la notación científica (1e7)
        ax.xaxis.set_major_formatter(
            ticker.FuncFormatter(lambda x, p: format(int(x), ","))
        )

        plt.title(
            "Top 10 Estados más Poblados (Datos Reales 2023)",
            fontsize=18,
            fontweight="bold",
            pad=20,
        )
        plt.xlabel("Población Total (Número de personas)", fontsize=13)
        plt.ylabel("Estado", fontsize=13)

        # Añadir el número exacto al final de cada barra (opcional pero muy útil)
        for i, v in enumerate(df["poblacion"]):
            ax.text(
                v + 300000,
                i,
                format(int(v), ","),
                color="black",
                va="center",
                fontweight="bold",
            )

        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    generate_chart()
