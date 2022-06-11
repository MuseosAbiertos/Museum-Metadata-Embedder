# csv2exif

'csv2exif' records metadata on images (ex. jpg) from a normalized CSV using VRAE, ISADG & Dublin Core standards.

Use exiftool (by Phil Harvey) to write EXIF metadata on jpgs according to an 
input CSV and a set of mapping rules according to naming standards: VRAE/ISADG/DC

Usage:
    python csv2exif.py CSV_PATH IMAGES_ROOT_PATH

positional arguments:
CSV_PATH path for the CSV file to process.
JPGS_PATH root path for the JPG files.

options:
-h, --help show this help message and exit

--row-progress-notify ROW_PROGRESS_NOTIFY, -r ROW_PROGRESS_NOTIFY
how many rows between progress notifications. 100 by default

--notify-broken-keys NOTIFY_BROKEN_KEYS, -n NOTIFY_BROKEN_KEYS
Notify on broken/missing keys in the CSV. False by default.

--max-depth MAX_DEPTH, -m MAX_DEPTH
Max depth of sub-folders to look into when looking for JPGS. 3 by default

A JSON map is used to map Screen Name - Tag Name, for each of the standards. The file must be within the data/
directory, in a JSON file called: maps.json. The structure is as follows:
