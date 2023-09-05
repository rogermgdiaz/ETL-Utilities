import os
import re

# Nombre del archivo SQL original
archivo_sql_original = "postgres_public_trades.sql"

# Prefijo para los archivos divididos
prefijo_archivos_divididos = "fragmento_sql_"

# Número máximo de sentencias INSERT por fragmento
max_sentencias_por_fragmento = 10000

# Leer el contenido del archivo SQL original
with open(archivo_sql_original, "r") as archivo_original:
    contenido = archivo_original.read()

# Separar la estructura de la inserción de los valores
estructura, valores = re.split(r"\);\s*", contenido, maxsplit=1)
estructura += ");"  # Agregar el cierre de paréntesis que se perdió al dividir

# Dividir los valores en líneas individuales
lineas_de_valores = valores.split("\n")
lineas_de_valores = [linea.strip() for linea in lineas_de_valores if linea.strip()]  # Eliminar líneas vacías

# Dividir el contenido en fragmentos basados en el número máximo de sentencias
fragmentos = [lineas_de_valores[i:i + max_sentencias_por_fragmento] for i in range(0, len(lineas_de_valores), max_sentencias_por_fragmento)]

# Reemplazar la última coma (,) con un punto y coma (;) en cada fragmento
for fragmento in fragmentos:
    fragmento[-1] = fragmento[-1].rstrip(",") + ";"

# Directorio donde se guardarán los archivos fragmentados
directorio_destino = "archivos_fragmentados"

# Crear el directorio si no existe
os.makedirs(directorio_destino, exist_ok=True)

# Crear archivos de fragmentos SQL con la estructura INSERT
for i, fragmento in enumerate(fragmentos):
    nombre_archivo_fragmento = os.path.join(directorio_destino, f"{prefijo_archivos_divididos}{i + 1}.sql")
    
    # Si no es el primer fragmento, agregar la sentencia INSERT
    if i != 0:
        with open(nombre_archivo_fragmento, "w") as archivo_fragmento:
            archivo_fragmento.write(f"INSERT INTO public.trades (country_code, year, comm_code, flow, trade_usd, kg, quantity, quantity_name) VALUES\n")
            archivo_fragmento.write("\n".join(fragmento))
            archivo_fragmento.write("\n")  # Agregar una nueva línea
    else:
        # El primer fragmento contiene la estructura de la tabla y no necesita la sentencia INSERT
        with open(nombre_archivo_fragmento, "w") as archivo_fragmento:
            archivo_fragmento.write(estructura + "\n")
            archivo_fragmento.write("\n".join(fragmento))
            archivo_fragmento.write("\n")  # Agregar una nueva línea

print("Archivos divididos creados correctamente.")
