"""Renombra archivos de música usando sus tags (metadata) del propio archivo."""

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.directorios import pedir_directorio

from mutagen.easyid3 import EasyID3


MUSIC_EXTENSIONS = (".mp3",)


def extrae_metadata_con_tags(ruta_archivo):
    """Lee la metadata del archivo usando mutagen."""

    try:
        tags = EasyID3(ruta_archivo)
    except Exception:
        tags = None

    def obtener(clave):
        if tags and clave in tags:
            valores = tags[clave]
            if isinstance(valores, list) and valores:
                return str(valores[0])
            return str(valores)
        return ""

    cancion = obtener("title")
    artista = obtener("artist")
    anio = obtener("date")[:4]
    genero = obtener("genre")

    return {
        "cancion": cancion or Path(ruta_archivo).stem,
        "artista": artista or "Artista Desconocido",
        "artistas_adicionales": "",
        "año": anio,
        "genero": genero or "Desconocido",
    }


def limpiar_nombre_archivo(nombre):
    """Elimina caracteres no válidos para nombres de archivo."""

    nombre = re.sub(r'[<>:"/\\|?*]', "", nombre)
    nombre = re.sub(r"\s+", " ", nombre)
    return nombre.strip()


def generar_nombre_archivo(nombre_original, metadata, extension):
    """Genera el nuevo nombre adjuntando la metadata encontrada al nombre original."""

    nombre_base = Path(nombre_original).stem

    campos = [
        metadata.get("cancion", ""),
        metadata.get("artista", ""),
        metadata.get("artistas_adicionales", ""),
        metadata.get("año", ""),
        metadata.get("genero", ""),
    ]

    partes = [nombre_base] + [
        str(campo).strip() for campo in campos if str(campo).strip()
    ]

    nuevo_nombre = limpiar_nombre_archivo(" ".join(partes))
    return f"{nuevo_nombre}{extension.lower()}"


def obtener_nombre_unico(ruta_carpeta, nombre):
    """Devuelve un nombre de archivo que no exista en la carpeta."""

    nombre_path = Path(nombre)
    base = nombre_path.stem
    ext = nombre_path.suffix
    contador = 1

    while (ruta_carpeta / nombre).exists():
        nombre = f"{base}_{contador}{ext}"
        contador += 1

    return nombre


def procesar_archivo(file_path: Path):
    """Procesa un archivo: obtiene metadata, genera el nuevo nombre y renombra."""

    original_name = file_path.name
    print(f"\nProcesando: {original_name}")

    try:
        metadata = extrae_metadata_con_tags(file_path)
        extension = file_path.suffix
        nuevo_nombre = generar_nombre_archivo(original_name, metadata, extension)
        nuevo_nombre = obtener_nombre_unico(file_path.parent, nuevo_nombre)

        nuevo_path = file_path.parent / nuevo_nombre

        os.rename(file_path, nuevo_path)
        print(f"[OK] {original_name} -> {nuevo_nombre}")

    except Exception as e:
        print(f"[ERROR] {original_name}: {e}")


def renombra_musica_metadata(rutadirectorio):
    """Renombra todos los archivos de música del directorio."""

    ruta = Path(rutadirectorio)
    archivos = [f for f in ruta.iterdir() if f.is_file()]

    for archivo in archivos:
        if archivo.suffix.lower() not in MUSIC_EXTENSIONS:
            continue

        procesar_archivo(archivo)

    print("\nProceso finalizado.")


def ejecutar(rutadirectorio):
    """Ejecuta la funcion principal."""

    renombra_musica_metadata(rutadirectorio)


if __name__ == "__main__":
    directorio = pedir_directorio()
    ejecutar(directorio)
