import pymysql

# CONFIGURACIÓN: Pon tu contraseña real aquí
USER = "root"
PASSWORD = "thedria31"  # Si no tienes, déjalo vacío ''
HOST = "localhost"

try:
    # 1. Conectamos al servidor de MySQL (sin especificar base de datos)
    conexion = pymysql.connect(host=HOST, user=USER, password=PASSWORD)
    cursor = conexion.cursor()

    # 2. Creamos la base de datos si no existe
    cursor.execute("CREATE DATABASE IF NOT EXISTS limpieza_datos")

    print("✅ ¡Base de datos 'limpieza_datos' lista para recibir datos!")

    conexion.close()
except Exception as e:
    print(f"❌ Error al conectar: {e}")
    print("💡 Tip: Asegúrate de que XAMPP o MySQL Server estén ENCENDIDOS.")
