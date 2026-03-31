"""Module providing a function to execute the main program logic."""

import pkgutil
import importlib
import acciones

ACCIONES = {}

def cargar_acciones():
    """Carga desde el paquete 'acciones'."""

    for loader, module_name, is_pkg in pkgutil.iter_modules(acciones.__path__):
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

    directorio = input("Ingrese el directorio: ").strip()

    try:
        opcion = int(opcion) - 1
        key = list(ACCIONES.keys())[opcion]

        print(f"\nEjecutando: {key}\n")

        ACCIONES[key](directorio)

    except (ValueError, IndexError):
        print("Opción no válida")

if __name__ == "__main__":
    main()
