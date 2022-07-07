**MME** (Museum Metadata Embedder) -anteriormente 'csv2exif'- escribe (incrusta) metadatos -[Dublin Core](https://dublincore.org/specifications/dublin-core/), [VRA Core](https://core.vraweb.org/), [XMP](https://www.adobe.com/products/xmp.html), [ISAD(G)](https://www.ica.org/sites/default/files/CBPS_2000_Guidelines_ISAD(G)_Second-edition_EN.pdf), [IPTC](https://iptc.org/standards/photo-metadata/), [EXIF](https://docs.fileformat.com/image/exif/) y otros más- en [todo tipo de imágenes](https://exiftool.org/#supported) y archivos PDF a partir de un CSV normalizado.

**MME** es una aplicación de línea de comandos Python 3, que utiliza [ExifTool](https://exiftool.org/) (de Phil Harvey) y también tiene una interfaz gráfica, ejecutable en Linux, MacOS y Windows.

## Uso
<code>python csv2exif.py RUTA_CSV RUTA_IMAGES</code>
argumentos posicionales: CSV_PATH ruta para el archivo CSV a procesar. JPGS_PATH ruta de acceso a los archivos JPG.
Ejemplo: <code> python3 csv2exif.py csv/test.csv images/</code>

### Opciones
-h, --help mostrar este mensaje de ayuda y salir

--row-progress-notify ROW_PROGRESS_NOTIFY, -r ROW_PROGRESS_NOTIFY
el número de filas entre las notificaciones de progreso. 100 por defecto

--notify-broken-keys NOTIFY_BROKEN_KEYS, -n NOTIFY_BROKEN_KEYS
Notificar sobre claves rotas/faltantes en el CSV. Falso por defecto.

--max-depth MAX_DEPTH, -m MAX_DEPTH
Profundidad máxima de las subcarpetas para buscar JPGS. 3 por defecto

### Configuración personalizada
**MME** utiliza un mapa JSON para mapear el _"Nombre de pantalla" (Encabezado de la columna CSV) <-> "Nombre de etiqueta"_, para cada uno de los estándares. El archivo debe encontrarse dentro del directorio 'data', en un archivo JSON llamado 'maps.json'.
Este archivo se puede editar para agregar nuevas etiquetas.

Sólo es necesario editar las cabeceras (primera fila de la hoja de cálculo) para que se ajusten al esquema. Esto puede implicar la división de algunas columnas para ajustarse al esquema, la adición de columnas y otras ediciones. Todo esto es probablemente más fácil, más rápido y más preciso de hacer en una hoja de cálculo.

### GMME (Interfaz gráfica)
'gmme' es la versión gráfica de mme.py. Es un script de python3 (solamente). No acepta argumentos.

Uso:
<code>python3 gmme.py & </code>

### Historia
Mayormente, las colecciones de objetos se encuentran en hojas de cálculo que listan el contenido de sus colecciones, acompañado por las imágenes que los representan. Es decir que para ver los metadatos de una imagen, se debe contar con una aplicación para hojas de cálculo; si quieres enviarla por email, debes enviar ambos archivos, donde el CSV o XLSX contiene normalmente la totalidad de la colección.
**MME** incrusta los metadatos de modo que ellos siempre se encuentren 'dentro' de la imagen, facilitando la ingestión por otras herramientas y simplificando los procesos de registro y difusión.

Para leer los metadatos 'detallados' de una imagen o un archivo PDF, solo es necesario ejecutar:
<code>exiftool -a -G1 -s [archivo] </code>
o utilizar [Adobe Bridge Custom Metadata Panel](https://github.com/adobe-dmeservices/custom-metadata) o un servicio online, como [The Exifer](https://www.thexifer.net/)


## Acknowledgments/Agradecimientos
* Harry van der Wolf [Por su inestimable colaboración y la creación de la interfaz gráfica (GUI) y sus ejecutables multiplataforma]
* Greg Reser [Por todo su apoyo y colaboración en esta implementacion de VRA Core]
* Phil Harvey [Por su maravilloso ExifTool, que pronto cumplirá 30 años!]
* Jairo Serrano [Amigo y estimado SysOp que logra que todo funcione sin romperse y lo repara cuando se rompe]
* Sebastián Gersbach [Por el diseño del logo y el paquete de iconos]

## Sponsors/Mecenas
Esta aplicación ha sido posible gracias al programa de Mecenazgo Cultural de la Ciudad Autónoma de Buenos Aires, Argentina

![Logo%20Mecenazgo%202021%20negro%20ch](Logo%20Mecenazgo%202021%20negro%20ch.png "Logo%20Mecenazgo%202021%20negro%20ch")

y especialmente a nuestros mecenas

Banco Hipotecario https://www.hipotecario.com.ar
Techniques & Supplies https://www.techniques.com.ar
Digital Ocean https://www.digitalocean.com

![Logo%20Banco%20Hipotecario](Logo%20Banco%20Hipotecario.jpg "Logo%20Banco%20Hipotecario")
![Logo%20Techniques](Logo%20Techniques.jpg "Logo%20Techniques")
![DO_Logo_Horizontal_Blue](DO_Logo_Horizontal_Blue.png "DO_Logo_Horizontal_Blue")
