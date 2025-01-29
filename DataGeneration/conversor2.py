import json
import csv
import tkinter as tk
from tkinter import filedialog
from collections.abc import Mapping
import os

def flatten_dict(d, parent_key='', sep='.'):
    """Aplanar un diccionario, uniendo claves con un separador."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, Mapping):  # Si es un diccionario, se aplana recursivamente
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def convertir_json_a_csv(json_file_path, csv_file_path):
    """Leer un archivo JSON (posiblemente con múltiples objetos) y escribirlo como un archivo CSV."""
    rows = []
    
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        for line in json_file:
            try:
                # Intentar cargar cada línea como un objeto JSON
                datos_json = json.loads(line)
                
                # Aplanar las claves y agregarla a la lista de filas
                fila = flatten_dict(datos_json)
                rows.append(fila)
            except json.JSONDecodeError:
                print(f"Error al procesar la línea: {line}")
                continue

    # Si no se encontraron filas, salir
    if not rows:
        print("No se encontraron datos válidos en el archivo JSON.")
        return

    # Obtener todos los nombres de las columnas (un conjunto único de claves)
    columnas = set()
    for fila in rows:
        columnas.update(fila.keys())

    # Escribir el archivo CSV
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=columnas)
        writer.writeheader()  # Escribir las cabeceras de las columnas
        writer.writerows(rows)  # Escribir las filas de datos

def seleccionar_archivo_json():
    """Abrir una ventana de diálogo para seleccionar un archivo JSON."""
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter
    archivo_json = filedialog.askopenfilename(
        title="Selecciona un archivo JSON",
        filetypes=[("Archivos JSON", "*.json")]
    )
    return archivo_json

def guardar_archivo_csv(ruta_json):
    """Generar la ruta para guardar el archivo CSV con el mismo nombre en la misma ubicación."""
    nombre_csv = os.path.splitext(os.path.basename(ruta_json))[0] + '.csv'
    ruta_csv = os.path.join(os.path.dirname(ruta_json), nombre_csv)
    return ruta_csv

if __name__ == '__main__':
    # Seleccionar el archivo JSON
    archivo_json = seleccionar_archivo_json()

    if archivo_json:
        # Obtener la ruta para guardar el archivo CSV
        archivo_csv = guardar_archivo_csv(archivo_json)

        # Convertir el archivo JSON a CSV
        convertir_json_a_csv(archivo_json, archivo_csv)
        print(f"Archivo CSV guardado en: {archivo_csv}")
    else:
        print("No se seleccionó ningún archivo.")
