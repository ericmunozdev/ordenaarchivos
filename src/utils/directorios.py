"""Utilidades para el manejo de directorios."""

from pathlib import Path


def validar_directorio(ruta):
    """Valida que la ruta exista y sea un directorio.

    Retorna el directorio (Path) si es válido, o None en caso contrario.
    """

    if not ruta:
        return None

    directorio = Path(ruta).expanduser()

    if directorio.is_dir():
        return directorio

    return None


def pedir_directorio(mensaje="Ingrese el directorio: "):
    """Solicita un directorio por consola hasta obtener uno válido."""

    while True:
        ruta = input(mensaje).strip()

        directorio = validar_directorio(ruta)

        if directorio is not None:
            return directorio

        print("El directorio ingresado no existe o no es válido.")
