"""Normaliza el nombre de los archivos."""

import os
import re
import random
from pathlib import Path


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
        frase = " ".join(p for p in palabras)
        return frase.capitalize()
    elif formato == "8":  # Title Case (Primera letra de cada palabra)
        return " ".join(p.capitalize() for p in palabras)
    else:
        return texto


def normaliza_nombre_archivos(rutadirectorio, formato):

    os.chdir(rutadirectorio)
    archivos = [f for f in os.listdir() if os.path.isfile(f)]
    # archivos_limpios = [re.sub(r'\s+', ' ', os.path.splitext(f)[0]).strip() for f in archivos]

    listado = []

    for archivo in archivos:
        path_aux = Path(archivo)
        nombre_sin_ext = path_aux.stem
        extension = path_aux.suffix

        nombre_base = transformar_texto(nombre_sin_ext, formato)
        contador = listado.count(nombre_base)

        if contador > 0:
            nombre_base = f"{nombre_base}_{contador}"

        nuevo_nombre = f"{nombre_base}{extension}"

        if archivo != nuevo_nombre:
            try:
                os.rename(
                    os.path.join(rutadirectorio, archivo),
                    os.path.join(rutadirectorio, nuevo_nombre),
                )
                print(f"{archivo}  --->  {nuevo_nombre}")
            except Exception as e:
                os.rename(
                    os.path.join(rutadirectorio, archivo),
                    os.path.join(rutadirectorio, f"_{random.random()}_{nuevo_nombre}"),
                )
                print(f"Error ---> {e}")

        listado.append(nombre_base)


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

    normaliza_nombre_archivos(rutadirectorio, formato)


if __name__ == "__main__":
    directorio = input("Ingrese el directorio: ").strip()
    ejecutar(directorio)
