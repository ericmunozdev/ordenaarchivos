"""Renombra videos repetidos usando el hash de la primera imagen como referencia."""

import os
import cv2
from PIL import Image
import imagehash
from collections import defaultdict

VIDEO_EXTENSIONS = ('.mp4', '.avi', '.mkv', '.mov')

def get_first_frame(video_path):
    """Obtiene el primer frame de un video como imagen PIL."""

    cap = cv2.VideoCapture(video_path)
    success, frame = cap.read()
    cap.release()

    if not success:
        return None

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return Image.fromarray(frame_rgb)

def generate_phash(image):
    """Genera un hash perceptual (phash) para la imagen."""

    return imagehash.phash(image)

def collect_video_data(rutadirectorio):
    """Recopila datos de los videos."""

    data = []

    for filename in os.listdir(rutadirectorio):
        if not filename.lower().endswith(VIDEO_EXTENSIONS):
            continue

        video_path = os.path.join(rutadirectorio, filename)

        frame = get_first_frame(video_path)
        if frame is None:
            print(f"No se pudo leer: {filename}")
            continue

        phash = str(generate_phash(frame))
        size = os.path.getsize(video_path)

        data.append({
            "filename": filename,
            "path": video_path,
            "hash": phash,
            "size": size
        })

    return data

def renombra_videos_repetidos(rutadirectorio):
    """Renombra videos repetidos."""

    data = collect_video_data(rutadirectorio)

    # Agrupar por hash
    groups = defaultdict(list)
    for item in data:
        groups[item["hash"]].append(item)

    rename_map = []

    # Procesar cada grupo
    for phash, items in groups.items():
        # Ordenar por tamaño DESC (más grande primero)
        items_sorted = sorted(items, key=lambda x: x["size"], reverse=True)

        # El líder define el nombre base
        leader = items_sorted[0]
        base_name, ext = os.path.splitext(leader["filename"])

        # El líder mantiene su nombre
        rename_map.append((leader["path"], os.path.join(rutadirectorio, leader["filename"])))

        # Renombrar los demás
        for idx, item in enumerate(items_sorted[1:], start=1):
            new_name = f"{base_name}_{idx}{ext}"
            new_path = os.path.join(rutadirectorio, new_name)

            rename_map.append((item["path"], new_path))

    # IMPORTANTE: evitar colisiones
    temp_map = []

    for old, new in rename_map:
        if old == new:
            continue

        temp_path = old + ".tmp_renaming"
        os.rename(old, temp_path)
        temp_map.append((temp_path, new))

    # Segundo paso: nombre final
    for temp, final in temp_map:
        print(f"{temp.replace(".tmp_renaming","")} --> {final}")
        os.rename(temp, final)

    print("Renombrado finalizado.")

def ejecutar(rutadirectorio):
    """Ejecuta la funcion principal."""
    renombra_videos_repetidos(rutadirectorio)

if __name__ == "__main__":
    directorio = input("Ingrese el directorio: ").strip()
    renombra_videos_repetidos(directorio)
