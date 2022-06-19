# csv2exif

'csv2exif' records metadata on images from a normalized CSV using VRA Core, ISAD-G & Dublin Core standards.

Use ExifTool (by Phil Harvey) to write EXIF metadata on images according to an 
input CSV and a set of mapping rules according to naming standards: VRA CORE / ISAD-G / Dublin Core

See supported images: https://exiftool.org/#supported

Usage:  
    python csv2exif.py CSV_PATH IMAGES_ROOT_PATH

positional arguments:
CSV_PATH path for the CSV file to process.
JPGS_PATH root path for the JPG files.

Options:  

-h, --help  [show this help message and exit]  
  
-r ROW_PROGRESS_NOTIFY  --row-progress-notify ROW_PROGRESS_NOTIFY  
[how many rows between progress notifications. 100 by default]  
  
-n NOTIFY_BROKEN_KEYS   --notify-broken-keys NOTIFY_BROKEN_KEYS  
[Notify on broken/missing keys in the CSV. False by default]  
  
-m MAX_DEPTH    --max-depth MAX_DEPTH  
[Max depth of sub-folders to look into when looking for JPGS. 3 by default]  
  
A JSON map is used to map Screen Name - Tag Name, for each of the standards. The file must be within the 'data' directory, in a JSON file called 'maps.json'. 

# gcsv2exif

'gcsv2exif' is the graphical version of csv2exif.py. It is a python3 (only) script. It does not accept arguments.  

Usage:  
    python3 gcsv2exif.py &

## Requirements
run on the command prompt:  
    python3 -m pip install -r requirements.txt

---
---
# csv2exif

'csv2exif' registra los metadatos de las imágenes a partir de un CSV normalizado utilizando los estándares VRA Core, ISAD-G y Dublin Core.

Utiliza ExifTool (por Phil Harvey) para escribir los metadatos EXIF en las imágenes, según un CSV de entrada y un conjunto de reglas de mapeo según los estándares: VRA CORE / ISAD-G / Dublin Core

Ver imágenes soportadas: https://exiftool.org/#supported

Uso:  
    python csv2exif.py RUTA_CSV RUTA_IMAGES

argumentos posicionales:
CSV_PATH ruta para el archivo CSV a procesar.
JPGS_PATH ruta de acceso a los archivos JPG.

Opciones:  
-h, --help mostrar este mensaje de ayuda y salir  
  
--row-progress-notify ROW_PROGRESS_NOTIFY, -r ROW_PROGRESS_NOTIFY  
el número de filas entre las notificaciones de progreso. 100 por defecto  
  
--notify-broken-keys NOTIFY_BROKEN_KEYS, -n NOTIFY_BROKEN_KEYS  
Notificar sobre claves rotas/faltantes en el CSV. Falso por defecto.  
  
--max-depth MAX_DEPTH, -m MAX_DEPTH  
Profundidad máxima de las subcarpetas para buscar JPGS. 3 por defecto  
  
Se utiliza un mapa JSON para mapear Nombre de pantalla - Nombre de etiqueta, para cada uno de los estándares. El archivo debe estar dentro del directorio 'data', en un archivo JSON llamado 'maps.json'. 

# gcsv2exif

'gcsv2exif' es la versión gráfica de csv2exif.py. Es un script de python3 (solamente). No acepta argumentos.  

Uso:  
    python3 gcsv2exif.py &

## Requirements
ejecutar en la consola:  
    python3 -m pip install -r requirements.txt

