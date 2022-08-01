![mme-logo-300](https://user-images.githubusercontent.com/693328/178120901-6aa48cbe-dadb-4ec2-8ea9-33c6b5a32491.jpg)

# Museum Metadata Embedder (MME)

Embed (write) metadata -[Dublin Core](https://dublincore.org/specifications/dublin-core/), [VRA Core](https://core.vraweb.org/), [XMP](https://www.adobe.com/products/xmp.html), [ISAD(G)](https://www.ica.org/sites/default/files/CBPS_2000_Guidelines_ISAD(G)_Second-edition_EN.pdf), [IPTC](https://iptc.org/standards/photo-metadata/), [EXIF](https://docs.fileformat.com/image/exif/)- into all types of images and PDF files from a normalized CSV.

**MME** is a Python 3 command line application, which uses [ExifTool](https://exiftool.org/) (de Phil Harvey) and also has a graphical interface, runnable on Linux, MacOS and Windows.


## Use
```s
python mme.py CSV_PATH IMAGES_PATH
```
Positional arguments: CSV_PATH path to the CSV file to be processed. JPGS_PATH path to the JPG files.

Example:
```s
python3 mme.py csv/test.csv images/
```

### Options
-h (--help)
    Show this help message and exit.

-r ROW_PROGRESS_NOTIFY (--row-progress-notify ROW_PROGRESS_NOTIFY)
    The number of rows between progress notifications. 100 by default.

-n NOTIFY_BROKEN_KEYS (--notify-broken-keys NOTIFY_BROKEN_KEYS)
    Notify about broken/missing keys in the CSV. False by default.

-m MAX_DEPTH (--max-depth MAX_DEPTH)
    Maximum depth of subfolders to search for JPGS. 3 by default.

### GMME (GUI)
gmme' is the graphical version of mme.py. It is a python3 script (only). It does not accept arguments.

Use:
```s
python3 gmme.py &
```


## Manual
### English
https://docs.museosabiertos.org/en/museum-metadata-embedder

### Spanish
https://docs.museosabiertos.org/es/museum-metadata-embedder

## Tags
Embedded Metadata, Access to Digital Image Files, Open Content, Open Data, Metadata editor, Heritage

## Acknowledgments
* **Martin Gersbach**, project management and development
* **Harry van der Wolf**, for his invaluable collaboration and creation of the graphical user interface (GUI) and its cross-platform executables
* **Greg Reser**, for all his support and collaboration on this VRA Core implementation
* **Phil Harvey**, for his excellent ExifTool, soon to be 30 years old!
* **Patricia Harpring** (Getty Vocabulary Program)
* **Robin Johnson** (Getty Vocabulary Program)
* **Jairo Serrano**, SysOp who makes everything work without breaking and fixes it when it does break
* **Sebastián Gersbach**, for the logo design and the icon package
* **Centro de Documentación de Bienes Patrimoniales de Chile** [https://www.aatespanol.cl/]

## Patrons
This application has been made possible thanks to the Cultural Patronage program of the Autonomous City of Buenos Aires, Argentina.

![Logo Mecenazgo 2021 blanco](https://user-images.githubusercontent.com/693328/177692429-480ab71b-02e4-4757-bed7-102d828958b6.png)

and especially to our sponsors

* Banco Hipotecario https://www.hipotecario.com.ar
* Techniques & Supplies https://www.techniques.com.ar
* Digital Ocean https://www.digitalocean.com


![logo-banco-hipotecario](https://user-images.githubusercontent.com/693328/177692227-572b9a9d-7de1-4c5a-a7b7-42ceae104cbb.jpeg)
![logo-techniques](https://user-images.githubusercontent.com/693328/177692263-682edeb4-8102-4241-9c59-2aede618c0a6.jpeg)
![dologohorizontalblue](https://user-images.githubusercontent.com/693328/177692273-c9a9dba6-c84c-4707-afea-51f20b484a99.png)

