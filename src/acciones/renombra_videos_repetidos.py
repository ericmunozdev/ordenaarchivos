"""Renombra videos repetidos usando el hash de la primera imagen como referencia."""

import re
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import cv2
import imagehash
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.directorios import pedir_directorio

VIDEO_EXTENSIONS = (".mp4", ".avi", ".mkv", ".mov")
REPEAT_PREFIX_PATTERN = re.compile(r"^_repeat_\d{17}_\d+_")


def get_first_frame(video_path):
    """Obtiene el primer frame de un video como imagen PIL."""

    cap = cv2.VideoCapture(str(video_path))

    try:
        success, frame = cap.read()

        if not success:
            return None

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return Image.fromarray(frame_rgb)
    finally:
        cap.release()


def generate_phash(image):
    """Genera un hash perceptual (phash) para la imagen."""

    return imagehash.phash(image)


def ya_tiene_prefijo_repeat(nombre):
    """Indica si el archivo ya fue marcado como repetido."""

    return bool(REPEAT_PREFIX_PATTERN.match(nombre))


def generar_prefijo_repeat():
    """Genera un prefijo de repetido con timestamp de milisegundos."""

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    return f"_repeat_{timestamp}_"


def collect_video_data(rutadirectorio):
    """Recopila datos de los videos."""

    ruta = Path(rutadirectorio)
    data = []

    for archivo in ruta.iterdir():
        if not archivo.is_file():
            continue

        if archivo.suffix.lower() not in VIDEO_EXTENSIONS:
            continue

        frame = get_first_frame(archivo)
        if frame is None:
            print(f"No se pudo leer: {archivo.name}")
            continue

        phash = str(generate_phash(frame))
        size = archivo.stat().st_size

        data.append(
            {
                "filename": archivo.name,
                "path": archivo,
                "hash": phash,
                "size": size,
            }
        )

    return data


def renombra_videos_repetidos(rutadirectorio):
    """Renombra videos repetidos."""

    ruta = Path(rutadirectorio)
    data = collect_video_data(ruta)

    # Agrupar por hash
    groups = defaultdict(list)
    for item in data:
        groups[item["hash"]].append(item)

    # Nombres ocupados para evitar colisiones
    ocupados = {f.name for f in ruta.iterdir() if f.is_file()}

    # Procesar cada grupo
    for items in groups.values():
        # Los grupos de un solo elemento no tienen repetidos
        if len(items) < 2:
            continue

        # Si todos los archivos del grupo ya fueron marcados, no se renombran
        if all(ya_tiene_prefijo_repeat(item["filename"]) for item in items):
            continue

        # Ordenar por tamaño DESC (más grande primero)
        items_sorted = sorted(items, key=lambda x: x["size"], reverse=True)
        prefijo_repeat = generar_prefijo_repeat()

        # Renombrar todos los archivos del grupo
        for idx, item in enumerate(items_sorted, start=1):
            if ya_tiene_prefijo_repeat(item["filename"]):
                continue

            nuevo_nombre = f"{prefijo_repeat}{idx}_{item['filename']}"

            if nuevo_nombre == item["filename"]:
                continue

            contador = idx
            while nuevo_nombre in ocupados:
                contador += 1
                nuevo_nombre = f"{prefijo_repeat}{contador}_{item['filename']}"

            vieja_ruta = Path(item["path"])
            nueva_ruta = ruta / nuevo_nombre

            try:
                vieja_ruta.rename(nueva_ruta)
            except Exception as e:
                print(f"Error al renombrar '{item['filename']}': {e}")
                continue

            ocupados.discard(item["filename"])
            ocupados.add(nuevo_nombre)
            item["filename"] = nuevo_nombre
            item["path"] = nueva_ruta
            print(f"{vieja_ruta.name} --> {nuevo_nombre}")

        time.sleep(0.01)

    print("Renombrado finalizado.")


def ejecutar(rutadirectorio):
    """Ejecuta la funcion principal."""

    renombra_videos_repetidos(rutadirectorio)


if __name__ == "__main__":
    directorio = pedir_directorio()
    renombra_videos_repetidos(directorio)
