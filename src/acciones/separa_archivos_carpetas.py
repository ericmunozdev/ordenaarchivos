"""Separa los archivos en carpetas."""

import shutil
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.directorios import pedir_directorio


def generar_nombre_carpeta():
    """Retorna un nombre con formato YYYYMMDDHHMMSS.mmm"""

    now = datetime.now()
    return now.strftime("%Y%m%d%H%M%S") + f".{int(now.microsecond / 1000):03d}"


def obtener_nombre_carpeta_unico(ruta, nombre):
    """Devuelve un nombre de carpeta que no exista."""

    contador = 1

    while (ruta / nombre).exists():
        nombre = f"{nombre}_{contador}"
        contador += 1

    return nombre


def separa_archivos_carpetas(rutadirectorio, cantidad):
    """Separa los archivos del directorio en carpetas de N archivos."""

    ruta = Path(rutadirectorio)
    archivos = [f for f in ruta.iterdir() if f.is_file()]

    for i in range(0, len(archivos), cantidad):
        lote = archivos[i : i + cantidad]

        nombre_carpeta = obtener_nombre_carpeta_unico(
            ruta, generar_nombre_carpeta()
        )
        ruta_carpeta = ruta / nombre_carpeta

        ruta_carpeta.mkdir()
        print(f"Creando carpeta: {ruta_carpeta}")

        for archivo in lote:
            try:
                shutil.move(archivo, ruta_carpeta / archivo.name)
                print(f"Moviendo '{archivo.name}' a '{ruta_carpeta}'")
            except Exception as e:
                print(f"Error al mover '{archivo.name}': {e}")


def ejecutar(rutadirectorio):
    """Ejecuta la funcion principal."""

    print("\nIngrese la cantidad de archivos por carpeta:")
    cantidad = input("\nCantidad: ").strip()

    try:
        cantidad = int(cantidad)
    except ValueError:
        print("La cantidad debe ser un número.")
        return

    if cantidad <= 0:
        print("La cantidad debe ser un número positivo.")
        return

    separa_archivos_carpetas(rutadirectorio, cantidad)


if __name__ == "__main__":
    directorio = pedir_directorio()
    ejecutar(directorio)
