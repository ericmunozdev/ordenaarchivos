"""Obtiene el texto de los archivos de un directorio."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.directorios import pedir_directorio


def leer_archivo(ruta):
    """Lee un archivo como texto probando varias codificaciones."""

    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return [linea.rstrip("\r\n") for linea in f]
    except UnicodeDecodeError:
        with open(ruta, "r", encoding="latin-1") as f:
            return [linea.rstrip("\r\n") for linea in f]


def es_archivo_binario(lineas):
    """Detecta archivos binarios por la presencia de bytes nulos."""

    return any("\x00" in linea for linea in lineas)


def crea_archivo_salida(rutasalida, lineas):
    """Escribe las lineas en un archivo de salida."""

    ruta_salida = Path(rutasalida) / "output.txt"
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)

    with open(ruta_salida, "w", encoding="utf-8") as salida:
        for linea in lineas:
            salida.write(linea + "\n")

    print(f"Archivo generado: {ruta_salida}")


def obtiene_texto_archivos(rutadirectorio, rutasalida):
    """Obtiene el texto de todos los archivos del directorio."""

    ruta = Path(rutadirectorio)
    archivos = [f for f in ruta.iterdir() if f.is_file()]

    salida_path = (Path(rutasalida) / "output.txt").resolve()

    lineas = []

    for archivo in archivos:
        if archivo.resolve() == salida_path:
            continue

        try:
            contenido = leer_archivo(archivo)

            if es_archivo_binario(contenido):
                continue

            lineas.append(f"# {archivo.name}")
            lineas.extend(contenido)
        except Exception as e:
            print(f"Error leyendo '{archivo.name}': {e}")

    crea_archivo_salida(rutasalida, lineas)


def ejecutar(rutadirectorio):
    """Ejecuta la funcion principal."""

    rutasalida = input("Ingrese el directorio archivo salida: ").strip()

    if not rutasalida:
        print("Debe indicar un directorio de salida.")
        return

    obtiene_texto_archivos(rutadirectorio, rutasalida)


if __name__ == "__main__":
    directorio = pedir_directorio()
    ejecutar(directorio)
