"""Renombra archivos agregando el nombre de su carpeta como prefijo."""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.directorios import pedir_directorio


def limpiar_nombre_carpeta(nombre):
    """Limpia el nombre de la carpeta para usarlo como prefijo.

    Convierte a minúsculas, elimina caracteres no válidos para nombres de
    archivo, reemplaza espacios por guiones bajos y colapsa separadores.
    Si el resultado queda vacío, retorna "sin_nombre".
    """

    nombre = nombre.lower()
    nombre = re.sub(r'[<>:"/\\|?*]', "", nombre)
    nombre = re.sub(r"[^\w\s-]", "", nombre, flags=re.UNICODE)
    nombre = re.sub(r"[\s-]+", "_", nombre)
    nombre = re.sub(r"_+", "_", nombre)
    nombre = nombre.strip("_ ")

    return nombre or "sin_nombre"


def ya_tiene_prefijo(nombre_archivo, prefijo):
    """Verifica si el archivo ya comienza con el prefijo de la carpeta."""

    return nombre_archivo.lower().startswith(f"{prefijo.lower()}_")


def obtener_nombre_unico(ruta_carpeta, nombre, ocupados, archivo=None):
    """Devuelve un nombre de archivo que no exista en la carpeta."""

    nombre_path = Path(nombre)
    base = nombre_path.stem
    extension = nombre_path.suffix
    contador = 1

    while nombre in ocupados:
        if archivo is not None and (ruta_carpeta / nombre).resolve() == archivo.resolve():
            break

        nombre = f"{base}_{contador}{extension}"
        contador += 1

    return nombre


def renombra_archivos_carpeta(rutadirectorio):
    """Renombra todos los archivos del directorio agregando el prefijo de carpeta."""

    ruta = Path(rutadirectorio)
    archivos = [f for f in ruta.rglob("*") if f.is_file()]

    ocupados_por_carpeta = {}

    for archivo in archivos:
        carpeta = archivo.parent
        ocupados = ocupados_por_carpeta.setdefault(
            carpeta, {f.name for f in carpeta.iterdir() if f.is_file()}
        )

        prefijo = limpiar_nombre_carpeta(carpeta.name)

        if ya_tiene_prefijo(archivo.name, prefijo):
            continue

        nuevo_nombre = obtener_nombre_unico(
            carpeta, f"{prefijo}_{archivo.name}", ocupados, archivo
        )

        if nuevo_nombre == archivo.name:
            continue

        try:
            archivo.rename(carpeta / nuevo_nombre)
            ocupados.discard(archivo.name)
            ocupados.add(nuevo_nombre)
            print(f"{archivo}  --->  {carpeta / nuevo_nombre}")
        except Exception as e:
            print(f"Error al renombrar '{archivo.name}': {e}")


def ejecutar(rutadirectorio):
    """Ejecuta la funcion principal."""

    renombra_archivos_carpeta(rutadirectorio)


if __name__ == "__main__":
    directorio = pedir_directorio()
    ejecutar(directorio)
