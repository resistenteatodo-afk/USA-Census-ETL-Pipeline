import requests
import os


def download_heavy_data():
    # Dataset real: Registros de crímenes (pesado y con datos vacíos)
    url = "https://raw.githubusercontent.com/jakevdp/data-USstates/master/state-population.csv"
    filename = "DATASET_CHUNGO.csv"

    print(f"📡 Conectando con el servidor...")

    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"✅ ¡Descarga terminada! Archivo listo: {filename}")
        else:
            print(f"❌ Error de servidor: {response.status_code}")
    except Exception as e:
        print(f"❌ Error crítico: {e}")


if __name__ == "__main__":
    download_heavy_data()
