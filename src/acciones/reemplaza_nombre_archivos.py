"""Reemplaza texto en los nombres de los archivos de un directorio."""

import os

def reemplaza_nombre_archivos(rutadirectorio, texto_reemplazar, texto_reemplazo):

    os.chdir(rutadirectorio)
    archivos = [f for f in os.listdir() if os.path.isfile(f)]

    for archivo in archivos:
        nuevo_nombre = archivo.replace(texto_reemplazar, texto_reemplazo)

        if nuevo_nombre != archivo:
            try:
                os.rename(
                    os.path.join(rutadirectorio, archivo),
                    os.path.join(rutadirectorio, nuevo_nombre),
                )
                print(f"{archivo}  --->  {nuevo_nombre}")
            except Exception as e:
                print(f"Error al renombrar '{archivo}': {e}")

def ejecutar(rutadirectorio):
    """Ejecuta la funcion principal."""

    print("\nIngrese texto a reemplazar:")
    texto_reemplazar = input("\nTexto a reemplazar: ")

    print("\nIngrese texto de reemplazo:")
    texto_reemplazo = input("\nTexto de reemplazo: ")

    if texto_reemplazar == texto_reemplazo:
        print("Los textos de reemplazo no pueden ser iguales.")
        return

    reemplaza_nombre_archivos(rutadirectorio, texto_reemplazar, texto_reemplazo)


if __name__ == "__main__":
    directorio = input("Ingrese el directorio: ").strip()
    ejecutar(directorio)
