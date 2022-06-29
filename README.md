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

## Requerimientos
ejecutar en la consola:  
    python3 -m pip install -r requirements.txt


---
# Acknowledgments/Agradecimientos
* Harry van der Wolf (Por su inestimable colaboración y crear la GUI y ejecutables multiplataforma)
* Greg Reser (Por todo su apoyo y colaboración en esta implementacion de VRA Core)
* Phil Harvey (Por su maravilloso ExifTool, que pronto cumplirá 30 años!)
* Jairo Serrano (Mi amigo y estimado SysOp que logra que todo funcione sin romperse y lo repara cuando se rompe)

# Sponsors/Mecenas
Esta aplicación ha sido posible gracias al programa de **Mecenazgo Cultural** de la Ciudad Autónoma de Buenos Aires, Argentina

![Logo Mecenazgo 2021 blanco](https://user-images.githubusercontent.com/693328/175651622-df6f7d4d-ba78-4862-88f1-3b161c48d428.png)

https://www.buenosaires.gob.ar/mecenazgo

y especialmente a nuestros mecenas

* Banco Hipotecario https://www.hipotecario.com.ar
* Techniques & Supplies https://www.techniques.com.ar
* Digital Ocean [https://www.digitalocean.com](https://www.digitalocean.com/community/pages/hollies-hub-for-good)

|                                                                                                                                |                                                                                                                         |                                                                                                                                 |
| ------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| ![Logo Banco Hipotecario](https://user-images.githubusercontent.com/693328/175657136-2524d56b-a0a8-493d-b96c-d84c7c5ef468.jpg) | ![Logo Techniques](https://user-images.githubusercontent.com/693328/175666054-1ca8f020-2c31-448e-8e9d-b6f2e26811e6.jpg) | ![DO_Logo_Horizontal_Blue](https://user-images.githubusercontent.com/693328/176058383-2fa26c85-a67b-4065-8707-451a0e4daa45.png) |

