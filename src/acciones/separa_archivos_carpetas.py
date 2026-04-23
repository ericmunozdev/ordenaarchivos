"""Separa los archivos en carpetas."""

import os
import time
import shutil
from datetime import datetime


def generar_nombre_carpeta():
    """Retorna un nombre con formato YYYYMMDDHHMMSS.mmm"""

    now = datetime.now()
    return now.strftime("%Y%m%d%H%M%S") + f".{int(now.microsecond / 1000):03d}"


def separa_archivos_carpetas(rutadirectorio, cantidad):
    os.chdir(rutadirectorio)
    archivos = [f for f in os.listdir() if os.path.isfile(f)]

    for i in range(0, len(archivos), cantidad):
        lote = archivos[i : i + cantidad]

        nombre_carpeta = generar_nombre_carpeta()
        ruta_carpeta = os.path.join(rutadirectorio, nombre_carpeta)

        os.makedirs(ruta_carpeta, exist_ok=True)
        print(f"Creando carpeta: {ruta_carpeta}")

        for archivo in lote:
            try:
                origen = os.path.join(rutadirectorio, archivo)
                destino = os.path.join(ruta_carpeta, archivo)
                shutil.move(origen, destino)
                print(f"Moviendo '{archivo}' a '{ruta_carpeta}'")
            except Exception as e:
                print(f"Error al mover '{archivo}': {e}")

        # Pequeña pausa para evitar colisiones de timestamp
        time.sleep(0.01)


def ejecutar(rutadirectorio):
    """Ejecuta la funcion principal."""

    print("\nIngrese la cantidad de archivos por carpeta:")
    cantidad = input("\nCantidad: ")

    cantidad = int(cantidad)

    if cantidad <= 0:
        print("La cantidad debe ser un número positivo.")
        return

    separa_archivos_carpetas(rutadirectorio, cantidad)


if __name__ == "__main__":
    directorio = input("Ingrese el directorio: ").strip()
    ejecutar(directorio)
