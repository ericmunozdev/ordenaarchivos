"""Renombra imágenes según la fecha más antigua del archivo."""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.directorios import pedir_directorio

IMAGE_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".webp",
    ".tiff",
    ".tif",
    ".heic",
)


def obtener_fecha_minima(archivo):
    """Retorna la fecha más antigua del archivo (creación o modificación)."""

    stat = archivo.stat()
    return min(stat.st_ctime, stat.st_mtime)


def obtener_nombre_unico(ruta_carpeta, nombre, archivo=None):
    """Devuelve un nombre de archivo que no exista en la carpeta."""

    nombre_path = Path(nombre)
    base = nombre_path.stem
    extension = nombre_path.suffix
    contador = 1

    while (ruta_carpeta / nombre).exists():
        if archivo is not None and (ruta_carpeta / nombre).resolve() == archivo.resolve():
            break

        nombre = f"{base}_{contador}{extension}"
        contador += 1

    return nombre


def renombra_imagenes_fecha(rutadirectorio):
    """Renombra las imágenes del directorio según su fecha más antigua."""

    ruta = Path(rutadirectorio)
    archivos = [f for f in ruta.iterdir() if f.is_file()]

    for archivo in archivos:
        if archivo.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        fecha = datetime.fromtimestamp(obtener_fecha_minima(archivo))
        nombre_base = fecha.strftime("%Y%m%d_%H%M%S")
        extension = archivo.suffix.lower()

        nuevo_nombre = obtener_nombre_unico(ruta, f"{nombre_base}{extension}", archivo)

        if nuevo_nombre == archivo.name:
            continue

        try:
            archivo.rename(ruta / nuevo_nombre)
            print(f"{archivo.name}  --->  {nuevo_nombre}")
        except Exception as e:
            print(f"Error al renombrar '{archivo.name}': {e}")


def ejecutar(rutadirectorio):
    """Ejecuta la funcion principal."""

    renombra_imagenes_fecha(rutadirectorio)


if __name__ == "__main__":
    directorio = pedir_directorio()
    ejecutar(directorio)
