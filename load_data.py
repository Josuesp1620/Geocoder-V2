import subprocess


data_distritos = []
data_centros_poblados = []
data_urbanizaciones = []
data_calles = []
dat_manzanas_lotes = []

import os

def obtener_archivos_en_carpeta(carpeta):
    archivos = []
    for carpeta_actual, subcarpetas, archivos_actual in os.walk(carpeta):
        for archivo in archivos_actual:
            ruta_completa = os.path.join(carpeta_actual, archivo)
            archivos.append(ruta_completa)
    return archivos

carpeta_a_explorar = '/srv/geocoder/geocoder/data'

archivos_en_carpeta = obtener_archivos_en_carpeta(carpeta_a_explorar)

for file in archivos_en_carpeta:
    try:
        print(f"Cargando data del archivo => {file}")

        bash_command = f"./env/bin/python app.py batch {file}"

        result = subprocess.run(bash_command, shell=True, check=True, text=True)
    except:
        print(f"Error al ejecutar carga de datos en el archivo => {file}")

print(f"Ejecutando ngrams")
bash_command = f"./env/bin/python app.py ngrams"
result = subprocess.run(bash_command, shell=True, check=True, text=True)
print(f"___CARGA DE DATOS REALIZADA CORRECTAMENTE___")
