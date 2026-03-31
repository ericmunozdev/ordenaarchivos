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
