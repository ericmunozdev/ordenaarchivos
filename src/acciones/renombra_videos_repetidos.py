"""Renombra videos repetidos usando el hash de la primera imagen como referencia."""

import cv2
import imagehash
from PIL import Image
from collections import defaultdict
from pathlib import Path

VIDEO_EXTENSIONS = (".mp4", ".avi", ".mkv", ".mov")


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

        # Ordenar por tamaño DESC (más grande primero)
        items_sorted = sorted(items, key=lambda x: x["size"], reverse=True)

        # El líder define el nombre base y mantiene su nombre
        leader = items_sorted[0]
        base_name = Path(leader["filename"]).stem
        ext = Path(leader["filename"]).suffix

        # Renombrar los demás
        for idx, item in enumerate(items_sorted[1:], start=1):
            nuevo_nombre = f"{base_name}_{idx}{ext}"

            if nuevo_nombre == item["filename"]:
                continue

            contador = idx
            while nuevo_nombre in ocupados:
                contador += 1
                nuevo_nombre = f"{base_name}_{contador}{ext}"

            vieja_ruta = Path(item["path"])
            nueva_ruta = ruta / nuevo_nombre

            vieja_ruta.rename(nueva_ruta)
            ocupados.discard(item["filename"])
            ocupados.add(nuevo_nombre)
            print(f"{item['filename']} --> {nuevo_nombre}")

    print("Renombrado finalizado.")


def ejecutar(rutadirectorio):
    """Ejecuta la funcion principal."""

    renombra_videos_repetidos(rutadirectorio)


if __name__ == "__main__":
    directorio = input("Ingrese el directorio: ").strip()
    renombra_videos_repetidos(directorio)
