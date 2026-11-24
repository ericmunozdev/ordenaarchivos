"""Module providing a function to execute the main program logic."""

import importlib
import pkgutil

import acciones
from utils.directorios import pedir_directorio

ACCIONES = {}


def cargar_acciones():
    """Carga desde el paquete 'acciones'."""

    for _, module_name, _ in pkgutil.iter_modules(acciones.__path__):
        modulo = importlib.import_module(f"acciones.{module_name}")

        if hasattr(modulo, "ejecutar"):
            ACCIONES[module_name] = modulo.ejecutar


def mostrar_menu():
    """Muestra el menú de acciones."""

    print("\nSeleccione una acción:\n")
    for i, key in enumerate(ACCIONES.keys(), start=1):
        print(f"{i}. {key}")


def main():
    """Función principal del programa."""

    cargar_acciones()

    if not ACCIONES:
        print("No se encontraron acciones disponibles.")
        return

    mostrar_menu()
    opcion = input("\nOpción: ").strip()

    try:
        indice = int(opcion) - 1
    except ValueError:
        print("Opción no válida")
        return

    claves = list(ACCIONES.keys())

    if not 0 <= indice < len(claves):
        print("Opción no válida")
        return

    directorio = pedir_directorio()
    key = claves[indice]

    print(f"\nEjecutando: {key}\n")

    ACCIONES[key](directorio)


if __name__ == "__main__":
    main()
