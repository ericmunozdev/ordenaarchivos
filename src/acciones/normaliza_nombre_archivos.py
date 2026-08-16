"""Normaliza el nombre de los archivos."""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.directorios import pedir_directorio


def transformar_texto(texto, formato):
    """Aplica el estilo de Case seleccionado al cuerpo del nombre del archivo."""

    # Extraemos solo palabras ignorando guiones bajos o puntos internos
    palabras = re.findall(r"[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\-\[\]]+", texto.lower())

    if not palabras:
        return texto

    if formato == "1":  # lower case
        return texto.lower()
    elif formato == "2":  # UPPER CASE
        return texto.upper()
    elif formato == "3":  # camelCase
        temp = "".join(p.capitalize() for p in palabras)
        return temp[0].lower() + temp[1:]
    elif formato == "4":  # PascalCase
        return "".join(p.capitalize() for p in palabras)
    elif formato == "5":  # snake_case
        return "_".join(p for p in palabras)
    elif formato == "6":  # kebab-case
        return "-".join(p for p in palabras)
    elif formato == "7":  # Sentence case (Primera letra total en mayúscula)
        return " ".join(p for p in palabras).capitalize()
    elif formato == "8":  # Title Case (Primera letra de cada palabra)
        return " ".join(p.capitalize() for p in palabras)
    else:
        return texto


def normaliza_nombre_archivos(rutadirectorio, formato):
    """Normaliza el nombre de todos los archivos del directorio."""

    ruta = Path(rutadirectorio)
    archivos = [f for f in ruta.iterdir() if f.is_file()]

    # Nombres ocupados para evitar colisiones
    ocupados = {f.name for f in archivos}

    for archivo in archivos:
        nombre_base = transformar_texto(archivo.stem, formato)
        extension = archivo.suffix

        nuevo_nombre = f"{nombre_base}{extension}"
        contador = 1

        while nuevo_nombre in ocupados and nuevo_nombre != archivo.name:
            nuevo_nombre = f"{nombre_base}_{contador}{extension}"
            contador += 1

        if nuevo_nombre == archivo.name:
            continue

        try:
            archivo.rename(ruta / nuevo_nombre)
            ocupados.discard(archivo.name)
            ocupados.add(nuevo_nombre)
            print(f"{archivo.name}  --->  {nuevo_nombre}")
        except Exception as e:
            print(f"Error al renombrar '{archivo.name}': {e}")


def ejecutar(rutadirectorio):
    """Ejecuta la funcion principal."""

    print("\nSelecciona el formato deseado:")
    print("1. minúsculas")
    print("2. MAYÚSCULAS")
    print("3. camelCase")
    print("4. PascalCase")
    print("5. snake_case")
    print("6. kebab-case")
    print("7. Sentence case")
    print("8. Title Case")
    formato = input("\nOpción (1-8): ")

    if formato not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
        print("Opción no válida.")
        return

    normaliza_nombre_archivos(rutadirectorio, formato)


if __name__ == "__main__":
    directorio = pedir_directorio()
    ejecutar(directorio)
