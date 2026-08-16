"""Renombra archivos de música usando sus tags (metadata) del propio archivo."""

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.directorios import pedir_directorio

from mutagen.easyid3 import EasyID3


MUSIC_EXTENSIONS = (".mp3",)
ERROR_PREFIX = "_error_"


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
        str(campo).strip()
        for campo in campos
        if str(campo).strip() and "desconocido" not in str(campo).lower()
    ]

    nuevo_nombre = limpiar_nombre_archivo(" ".join(partes))
    return f"{nuevo_nombre}{extension.lower()}"


def obtener_nombre_unico(ruta_carpeta, nombre, archivo=None):
    """Devuelve un nombre de archivo que no exista en la carpeta."""

    nombre_path = Path(nombre)
    base = nombre_path.stem
    ext = nombre_path.suffix
    contador = 1

    while (ruta_carpeta / nombre).exists():
        if (
            archivo is not None
            and (ruta_carpeta / nombre).resolve() == archivo.resolve()
        ):
            break

        nombre = f"{base}_{contador}{ext}"
        contador += 1

    return nombre


def marcar_archivo_error(ruta_carpeta, archivo):
    """Antepone '_error_' al nombre del archivo para detectarlo visualmente."""

    nombre_error = obtener_nombre_unico(
        ruta_carpeta, f"{ERROR_PREFIX}{archivo.name}", archivo
    )

    try:
        archivo.rename(ruta_carpeta / nombre_error)
        print(f"[ERROR MARK] {archivo.name} -> {nombre_error}")
        return nombre_error
    except Exception as e:
        print(f"No se pudo marcar como error '{archivo.name}': {e}")
        return None


def procesar_archivo(file_path: Path):
    """Procesa un archivo: obtiene metadata, genera el nuevo nombre y renombra.

    Retorna ("ok", nombre_original, nuevo_nombre) en éxito o
    ("error", nombre_original, mensaje) si el renombrado falla.
    """

    original_name = file_path.name
    print(f"\nProcesando: {original_name}")

    try:
        metadata = extrae_metadata_con_tags(file_path)
        extension = file_path.suffix
        nuevo_nombre = generar_nombre_archivo(original_name, metadata, extension)
        nuevo_nombre = obtener_nombre_unico(file_path.parent, nuevo_nombre, file_path)

        nuevo_path = file_path.parent / nuevo_nombre

        if nuevo_nombre != original_name:
            os.rename(file_path, nuevo_path)

        print(f"[OK] {original_name} -> {nuevo_nombre}")
        return ("ok", original_name, nuevo_nombre)

    except Exception as e:
        marcar_archivo_error(file_path.parent, file_path)
        print(f"[ERROR] {original_name}: {e}")
        return ("error", original_name, str(e))


def escribir_log_errores(ruta, errores):
    """Escribe el archivo de errores en el directorio."""

    ruta_log = ruta / "errores.txt"

    try:
        with open(ruta_log, "w", encoding="utf-8") as log:
            for original, mensaje in errores:
                log.write(f"{original}: {mensaje}\n")

        print(f"Log de errores: {ruta_log}")
    except Exception as e:
        print(f"No se pudo escribir el log de errores: {e}")


def renombra_musica_metadata(rutadirectorio):
    """Renombra todos los archivos de música del directorio."""

    ruta = Path(rutadirectorio)
    archivos = [f for f in ruta.iterdir() if f.is_file()]

    errores = []

    for archivo in archivos:
        if archivo.suffix.lower() not in MUSIC_EXTENSIONS:
            continue

        if archivo.name.startswith(ERROR_PREFIX):
            continue

        estado = procesar_archivo(archivo)

        if estado[0] == "error":
            errores.append((estado[1], estado[2]))

    escribir_log_errores(ruta, errores)

    print("\nProceso finalizado.")


def ejecutar(rutadirectorio):
    """Ejecuta la funcion principal."""

    renombra_musica_metadata(rutadirectorio)


if __name__ == "__main__":
    directorio = pedir_directorio()
    ejecutar(directorio)
