# OrdenaArchivos

Herramienta CLI en Python para **organizar y renombrar archivos de forma masiva** dentro de un directorio: normalizar nombres, reemplazar texto, separar en carpetas, detectar duplicados, extraer texto o renombrar música según sus tags.

## ¿Qué hace?

- Se elige una **acción** desde un menú interactivo.
- Se indica el **directorio** a procesar (se valida que exista).
- La acción recorre los archivos del directorio y los modifica según su propósito.

## Arquitectura

El proyecto usa una arquitectura de **plugins**:

- `src/main.py` escanea dinámicamente el paquete `acciones/` con `pkgutil` y arma el menú.
- Cada módulo de `acciones/` es **independiente**: expone una función `ejecutar(rutadirectorio)` y, además, puede ejecutarse por separado (tiene su propio bloque `if __name__ == "__main__"`).
- `src/utils/directorios.py` centraliza la **validación reutilizable del directorio** (`validar_directorio` / `pedir_directorio`), usada tanto por `main.py` como por cada acción.

```
src/
├── main.py                            # Punto de entrada (menú)
├── acciones/                          # Paquete de plugins (cada uno es una acción)
│   ├── normaliza_nombre_archivos.py
│   ├── separa_archivos_carpetas.py
│   ├── reemplaza_nombre_archivos.py
│   ├── obtiene_texto_archivos.py
│   ├── renombra_imagenes_fecha.py
│   ├── renombra_videos_repetidos.py
│   └── renombra_musica_metadata.py
└── utils/
    ├── __init__.py
    └── directorios.py                 # Validación del directorio
```

## Acciones disponibles

| Acción | Qué hace |
|---|---|
| `normaliza_nombre_archivos` | Cambia el "case" de los nombres (minúsculas, MAYÚSCULAS, camelCase, PascalCase, snake_case, kebab-case, Sentence/Title case) evitando colisiones. |
| `separa_archivos_carpetas` | Agrupa los archivos en carpetas de N archivos, nombradas con timestamp. |
| `reemplaza_nombre_archivos` | Reemplaza texto en los nombres de los archivos evitando colisiones. |
| `obtiene_texto_archivos` | Extrae el texto de todos los archivos a un `output.txt` (soporta UTF-8/latin-1 y omite binarios). |
| `renombra_imagenes_fecha` | Renombra imágenes a `YYYYMMDD_hhmmss.ext` (extensión en minúscula) usando la fecha más antigua del archivo, con sufijo `_1`, `_2`, etc. si hay colisión. |
| `renombra_videos_repetidos` | Detecta videos duplicados comparando el hash perceptual del primer frame y les agrega `_1`, `_2`, etc. |
| `renombra_musica_metadata` | Renombra MP3 concatenando al nombre los tags del archivo (título, artista, año, género) con `mutagen`. |

## Cómo usar

### Modo menú (recomendado)

```
python src/main.py
```

Elige la acción, ingresa el directorio y sigue las instrucciones de cada acción.

### Modo directo (ejecutar una acción sola)

```
python src/acciones/normaliza_nombre_archivos.py
```

Cada acción pide el directorio por consola. Como se ejecuta fuera del paquete, agrega la carpeta `src/` a `sys.path` para importar `utils.directorios`.

## Detalles de implementación

- **Carga dinámica**: `main.py` importa cada módulo de `acciones/` y registra los que tengan `ejecutar`.
- **Validación del directorio**: `pedir_directorio()` repite la pregunta hasta obtener una ruta válida (evita que una ruta inexistente rompa el flujo).
- **Sin `os.chdir`**: las acciones trabajan con `pathlib.Path` y rutas absolutas, evitando estado global compartido.
- **Evitan colisiones**: al renombrar/mover archivos se controlan los nombres ya ocupados para no sobrescribir nada.

## Dependencias

- Entorno virtual en `env/` y dependencias fijadas en `requirements.txt` (entre otras: `mutagen`, `opencv-python`, `Pillow`, `ImageHash`).
- Nota: `requirements.txt` está guardado en **UTF-16 (Unicode)**. Si `pip install -r requirements.txt` falla por codificación, reconvierte el archivo a UTF-8.
- Para formatear el código se usa **Black Formatter**.

---

# Preparar el ambiente para desarrollo

**Notas**

Para formatear el código en python usar: Black Formatter

## PIP

Instalar y/o actualizar pip
```
python.exe -m pip install --upgrade pip
```

Listar los modulos existentes
```
pip list
```

Listar los modulos fuera de fecha
```
pip list --outdated
```

En caso de querer desinstalar
```
pip freeze > modulos.txt
pip uninstall -r modulos.txt -y
pip list

rm modulos.txt
```

## Entorno virtual

Verificar la versión actual
```
python --version
```

Instalar el entorno virtual
```
pip install virtualenv
```

Crear el entorno virtual
```
virtualenv -p python3 env
```

Activar el entorno virtual
```
.\env\Scripts\activate
```

Para guardar el listado de modulos desde el entorno virtual
```
pip freeze > requirements.txt
```

Instalar paquetes desde el listado de modulos
```
pip install -r requirements.txt
```

Desactivar el entorno virtual
```
deactivate
```
