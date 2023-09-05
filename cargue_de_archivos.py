import psycopg2
import os
from tqdm import tqdm  # Importar tqdm

# Configuración de la base de datos (ajústala según tu entorno)
db_config = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "0412"
}

# Ruta completa al directorio donde se encuentran los archivos SQL divididos
directorio_archivos_divididos = "C:\\Users\\roger\\OneDrive\\Escritorio\\GATITO\\Programacion\\cursos_platzi\\Curso de Fundamentos de ETL con Python y Pentaho\\archivos_fragmentados"

# Obtener la lista de archivos SQL en el directorio
archivos_sql = [archivo for archivo in os.listdir(directorio_archivos_divididos) if archivo.endswith(".sql")]

# Ordenar los archivos por nombre
archivos_sql.sort()

# Conectar a la base de datos
try:
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("BEGIN;")

    # Iterar sobre los archivos y ejecutar las consultas SQL con barra de carga
    for archivo_sql in tqdm(archivos_sql, desc="Insertando datos"):
        ruta_archivo = os.path.join(directorio_archivos_divididos, archivo_sql)
        with open(ruta_archivo, "r") as archivo:
            consulta_sql = archivo.read()
            cursor.execute(consulta_sql)

    cursor.execute("COMMIT;")
    conn.commit()
    print("Inserción exitosa en la base de datos.")

except psycopg2.Error as e:
    print(f"Error al insertar datos en la base de datos: {e}")

finally:
    cursor.close()
    conn.close()

print("Proceso completado.")
