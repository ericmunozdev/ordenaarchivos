"""Reemplaza texto en los nombres de los archivos de un directorio."""

from pathlib import Path


def reemplaza_nombre_archivos(rutadirectorio, texto_reemplazar, texto_reemplazo):
    """Reemplaza texto en los nombres de los archivos del directorio."""

    ruta = Path(rutadirectorio)
    archivos = [f for f in ruta.iterdir() if f.is_file()]

    # Nombres ocupados para evitar colisiones
    ocupados = {f.name for f in archivos}

    for archivo in archivos:
        nuevo_nombre = archivo.name.replace(texto_reemplazar, texto_reemplazo)

        if nuevo_nombre == archivo.name:
            continue

        nombre_base = Path(nuevo_nombre).stem
        extension = Path(nuevo_nombre).suffix
        contador = 1

        while nuevo_nombre in ocupados:
            nuevo_nombre = f"{nombre_base}_{contador}{extension}"
            contador += 1

        try:
            archivo.rename(ruta / nuevo_nombre)
            ocupados.discard(archivo.name)
            ocupados.add(nuevo_nombre)
            print(f"{archivo.name}  --->  {nuevo_nombre}")
        except Exception as e:
            print(f"Error al renombrar '{archivo.name}': {e}")


def ejecutar(rutadirectorio):
    """Ejecuta la funcion principal."""

    texto_reemplazar = input("\nIngrese texto a reemplazar: ").strip()

    if not texto_reemplazar:
        print("El texto a reemplazar no puede estar vacío.")
        return

    texto_reemplazo = input("\nIngrese texto de reemplazo: ").strip()

    if texto_reemplazar == texto_reemplazo:
        print("Los textos de reemplazo no pueden ser iguales.")
        return

    reemplaza_nombre_archivos(rutadirectorio, texto_reemplazar, texto_reemplazo)


if __name__ == "__main__":
    directorio = input("Ingrese el directorio: ").strip()
    ejecutar(directorio)
