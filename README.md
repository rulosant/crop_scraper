# crop_scraper
Crop Information Scraper



## Instalación :wrench:

### Requerimientos Previos :nut_and_bolt:

1. Tener instalado Python. Si no lo tenés instalado, [acá te dejo un link](https://tutorial.djangogirls.org/es/python_installation/)

2. Clonar este repo. Si no sabés clonar un repositorio, [acá te dejo un link](https://www.taloselectronics.com/blogs/tutoriales/como-descargar-un-proyecto-de-github)

3. Otra opción en lugar de clonar, se puede descargar el código desde el botón `<> Code`  -> `Download ZIP`

### Setup :hammer:

1. Abrir una terminal/consola donde puedas usar python.

2. Ir a la carpeta del repositorio en tu computadora.

2. Crear un entorno virtual y activarlo corriendo lo siguiente :

Windows:
```bash
python -m venv ./venv/
venv\Scripts\activate
```

3. Instalar lo que necesita el comando para funcionar:

```bash
pip install -r requirements.txt
```

4. Agregar el archivo ***config.py*** a la carpeta

5. Listo, ya se puede usar el script


## Uso :rainbow: 

Asegurarse que existan los archivos de configuración:
   - `config.py`
   - `cultivos.txt`
   - `paises.txt`

### Uso desde VirtualEnv

1. Abrir una terminal

2. Ir a la carpeta del repositorio

3. Activar el entorno virtual:

```bash
source venv/bin/activate
```

4. Ejecutar el script con 
```bash
python script.py
```

### Uso sin activar el virtualenv
1. Crear una carpeta en cualquier lugar

2. grabar en esa carpeta los archivos `paises.txt` y `cultivos.txt`

3. Ejecutar el script utilizando **la ruta completa al Python del VirtualEnv** y **la ruta completa a `script.py`**
```bash
RUTA_A_LA_CARPETA_DEL_REPO\venv\Scripts\python.exe RUTA_A_LA_CARPETA_DEL_REPO\script.py
```
Ejemplo:
```bash
C:\Users\Usuario\Proyectos\crop_scraper\venv\Scripts\python.exe C:\Users\Usuario\Proyectos\crop_scraper\script.py
```


## Secuencia de pasos

1. En la carpeta desde donde se ejecuta el script, tienen que estar los archivos `paises.txt` y `cultivos.txt`

3. En esa carpeta se creará el archivo `debug.txt`, que guarda el registro de lo ejecutado.

4. LA primera vez que se ejecuta, se crea atomaticamente la carpeta `export\`

5. En la carpeta `export\` se crea el archivo `searches.csv`, que contiene todas las combinaciones de {pais,cultivo} y el estado de la descarga

Si la descarga se interrumpe, al ejecutar nuevamente el script en la misma carpeta, retomará el estado desde según se indica en `export\searches.csv`
   
   
