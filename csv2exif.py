"""
version 0.2
date 2022-06-10
Martin Gersbach [mg@museosabiertos.org]

Use exiftool (by Phil Harvey) to write EXIF metadata on jpgs according to an input CSV and a set of mapping rules according to naming
standards: VRAE/ISADG/DC

Usage:
    python csv2exif.py CSV_PATH IMAGES_ROOT_PATH

A JSON map is used to map Screen Name - Tag Name, for each of the standards. The file must be within the data/
directory, in a JSON file called: maps.json. The structure is as follows:

{'vrae':
    {
        Screen Name: Tag Name,
        Screen Name 2: Tag Name 2,
    },
'isadg':
    {
        Screen Name: Tag Name,
        Screen Name 2: Tag Name 2,
    },
'dc':
    {
        Screen Name: Tag Name,
        Screen Name 2: Tag Name 2,
    },
}

- Rows in the CSV must have a column called "File Name"
- vrae.config and isadg.config must be in exiftool_configs/ directory inside the data/ directory.

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

License
This is free software; you can redistribute it and/or modify it under GNU General Public License v3.0

"""
import os
import sys
import csv
import time
import json
import datetime
import argparse
import subprocess

from typing import Optional

import colorama  # type: ignore

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
colorama.init()


def _get_current_time() -> str:
    """ Get the current date and time as a string """
    now = datetime.datetime.now()
    return f'{now.year}-{now.month}-{now.day} {"{:02d}".format(now.hour)}:' \
           f'{"{:02d}".format(now.minute)}:{"{:02d}".format(now.second)}'


def _get_current_time_for_filename() -> str:
    """ Get the current date and time fixed for usage in filenames """
    return _get_current_time().replace(':', '-')


class Csv2Exif:
    """ Main class """
    DELETE_VRAE_TAGS = ['exiftool', '-v', '-xmp-vrae:all=']
    DELETE_ISADG_TAGS = ['exiftool', '-v', '-xmp-isadg:all=']
    DELETE_DC_TAGS = ['exiftool', '-v', '-xmp-dc:all=']

    WRITE_VRAE_TAGS = ['exiftool', '-config', f'{SCRIPT_PATH}/data/exiftool_configs/vrae.config']
    WRITE_ISADG_TAGS = ['exiftool', '-config', f'{SCRIPT_PATH}/data/exiftool_configs/isadg.config']
    WRITE_DC_TAGS = ['exiftool']

    def __init__(self, csv_filepath: str, images_root_path: str, row_progress_notify: int = 100,
                 notify_on_broken_keys: bool = False, max_depth: int = 3):
        self.csv_filepath: str = csv_filepath
        self.images_root_path: str = images_root_path
        self.row_progress_notify: int = row_progress_notify  # Every how many rows to notify progress
        self.exif_tool_error_log: list = []
        self.exif_tool_success_log: list = []
        self.notify_on_broken_keys: bool = notify_on_broken_keys
        self.max_depth = max_depth

        # Read maps and CSV
        self.maps = self._read_maps()
        self.rows = self._read_csv()

        # Validate images root path
        self._validate_image_path()

    @staticmethod
    def _info_msg(msg: str) -> None:
        """ Print information message. """
        print(f'{colorama.Fore.CYAN}[*] {msg}{colorama.Fore.RESET}')

    @staticmethod
    def _error_msg(msg: str, fatal: bool = True) -> None:
        """ Print error message, if fatal is True call sys.exit. """
        print(f'{colorama.Fore.RED if fatal else colorama.Fore.YELLOW}[!] {msg}{colorama.Fore.RESET}')
        if fatal:
            sys.exit(0)

    @staticmethod
    def _status_msg(msg) -> None:
        """ Print a status message using carriage return in order to provide a working animation """
        print(f'{colorama.Fore.GREEN}[...]{msg}{" " * 80}{colorama.Fore.RESET}', end='\r')

    @staticmethod
    def _end_status() -> None:
        """ End the status line """
        print('')

    def _read_maps(self) -> dict:  # type: ignore
        """ Read the standard maps file """
        try:
            return json.load(open(f'{SCRIPT_PATH}/data/maps.json', 'r', encoding='utf-8'))
        except json.JSONDecodeError as e:
            self._error_msg(f'_read_maps failed to decode the JSON file, with exception: {str(e)}')
        except FileNotFoundError as e:
            self._error_msg(f'_read_maps failed to found the file: {str(e)}')

    def _read_csv(self) -> list[dict]:  # type: ignore
        """ Read the CSV and create a list of dictionary from it """
        try:
            with open(self.csv_filepath, 'r', encoding='utf-8') as r_file:
                csv_reader = csv.DictReader(r_file)
                return [d for d in csv_reader]
        except FileNotFoundError as e:
            self._error_msg(f'_read_csv failed to found the file: {str(e)}')

    def _save_logs(self) -> None:
        """ Save the error and success logs for the sessions """
        output_name = self.csv_filepath.split('/')[-1].replace('.csv', '')
        output_name = f'{SCRIPT_PATH}/%s_{output_name}-{_get_current_time_for_filename()}.txt'
        with open(output_name % 'error_log', 'w', encoding='utf-8') as w_file:
            w_file.write('\n'.join(self.exif_tool_error_log))
        with open(output_name % 'success_log', 'w', encoding='utf-8') as w_file:
            w_file.write('\n'.join(self.exif_tool_success_log))

    def _validate_image_path(self):
        """ Check that the image_path exists/is not empty """
        if not list(os.walk(self.images_root_path)):
            self._error_msg(f'_validate_image_path found no files/directory at: f{self.images_root_path} (Does the '
                            f'path exist?')

    def _find_file_path(self, filename: str) -> Optional[str]:  # type: ignore
        """ Return the filepath for a filename, if it exists """
        for root, dirs, files in os.walk(self.images_root_path, followlinks=True):
            if len(root.replace(self.images_root_path, '').split('/')) > self.max_depth:
                return None

            if filename in files:
                return os.path.join(root, filename)

    def run(self):
        """ Main entry-point for the application """
        start_time = time.time()
        self._info_msg(f'Starting script with CSV path: "{self.csv_filepath}", {len(self.rows)} rows, and '
                       f'root image path: "{self.images_root_path}" at {_get_current_time()}')
        self._info_msg(f'This might take a while...')

        for index, row in enumerate(self.rows):
            if index % self.row_progress_notify == 0:
                if index != 0:
                    self._end_status()
                self._info_msg(f'Progress: {index}/{len(self.rows)}. Errors: {len(self.exif_tool_error_log)}, '
                               f'Successes: {len(self.exif_tool_success_log)}')

            csv_index = index + 2  # CSV Row index, for proper debugging

            # 1 - Check the row has a "File Name"
            filename = self.__get_file_name(csv_index, row)
            if not filename:
                continue  # Next row
            filepath = self.__get_file_path(csv_index, filename)
            if not filepath:
                continue  # Next row

            # 2 - Delete tags
            delete_map = {'DELETE VRAE TAGS': Csv2Exif.DELETE_VRAE_TAGS,
                          'DELETE ISADG TAGS': Csv2Exif.DELETE_ISADG_TAGS,
                          'DELETE DC TAGS': Csv2Exif.DELETE_DC_TAGS}

            for delete_key in delete_map.keys():
                self._status_msg(f'{index}/{len(self.rows)} - {delete_key} on {filename}')
                if not self.__delete_command(csv_index, filepath, delete_key, delete_map[delete_key]):
                    continue  # Next row

            # 3 - Write tags
            write_map = {'WRITE VRAE TAGS': [self.maps['vrae'], Csv2Exif.WRITE_VRAE_TAGS],
                         'WRITE ISADG TAGS': [self.maps['isadg'], Csv2Exif.WRITE_ISADG_TAGS],
                         'WRITE DC TAGS': [self.maps['dc'], Csv2Exif.WRITE_DC_TAGS]}

            for write_key in write_map.keys():
                tag_map, write_command = write_map[write_key]
                self._status_msg(f'{index}/{len(self.rows)} - {write_key} on {filename}')

                # Mark row as successfully written if there were no errors
                if self.__write_command(csv_index, row, filepath, write_key, tag_map, write_command):
                    self.exif_tool_success_log.append(f'On {write_key}: Row: "{csv_index}", filepath: "{filepath}"')

        # 4 - Write error/success logs
        self._end_status()
        self._info_msg(f'Writing logs...')
        self._save_logs()

        self._info_msg(f'Finished processing {len(self.rows)} with {len(self.exif_tool_error_log)} errors '
                       f'and {len(self.exif_tool_success_log)} successes at {_get_current_time()}')
        end_time = time.time()
        self._info_msg(f'Script took: {str(datetime.timedelta(seconds=(end_time - start_time)))}')

    def __get_file_name(self, row_index: int, row: dict) -> Optional[str]:
        """ Get row's filename, or log an error if the "File Name" column is empty. """
        if not row.get('File Name'):
            self.exif_tool_error_log.append(f'Row "{row_index}": No "File Name" column, or empty.')
            self._end_status()
            self._error_msg(f'Row "{row_index}": No "File Name" column, or empty.', fatal=False)
            return None
        else:
            return row.get('File Name')

    def __get_file_path(self, row_index: int, filename: str) -> Optional[str]:
        """ Get row's filepath, or log an error if the filepath is not found. """
        filepath = self._find_file_path(filename)
        if not filepath:
            self.exif_tool_error_log.append(f'Row "{row_index}": File not found in this path: "{filename}"')
            self._end_status()
            self._error_msg(f'Row "{row_index}": File not found in this path: "{filename}"', fatal=False)
            return None
        else:
            return filepath

    def __delete_command(self, row_index: int, filepath: str, delete_key: str, delete_command: list[str]) -> bool:
        """ Run tag DELETE commands """
        success, error = self.__delete_command_wrapper(delete_command, filepath)
        if error:
            self.exif_tool_error_log.append(f'On {delete_key}: Row: "{row_index}", filepath: "{filepath}", '
                                            f'ERROR: "{error}"')
            self._end_status()
            self._error_msg(f'On {delete_key}: Row: "{row_index}", filepath: "{filepath}", ERROR: "{error}"',
                            fatal=False)
            return False
        elif success:
            self.exif_tool_success_log.append(f'On {delete_key}: Row: "{row_index}", filepath: "{filepath}", '
                                              f'SUCCESS: "{success}"')
            return True
        else:
            self._end_status()
            self._error_msg(f'FATAL ERROR: Invalid return (no error nor success): On {delete_key}: '
                            f'Row: "{row_index}", filepath: "{filepath}".')  # Fatal error
            return False

    def __write_command(self, row_index: int, row: dict, filepath: str, write_key: str, tag_map: dict,
                        write_command: list) -> bool:
        """ Run tag WRITE commands  """
        for key in tag_map.keys():
            if key in row.keys():
                key_value_pair = f'-{tag_map[key]}={row[key]}'
                success, error = self.__write_command_wrapper(write_command, key_value_pair, filepath)
                if error:
                    self.exif_tool_error_log.append(f'On {write_key}: Row: "{row_index}", filepath: "{filepath}",'
                                                    f' Row key: {key}, ERROR: "{error}"')
                    self._end_status()
                    self._error_msg(f'On {write_key}: Row: "{row_index}", filepath: "{filepath}", Row key: {key},'
                                    f' ERROR: "{error}"', fatal=False)
                    return False
            else:
                if self.notify_on_broken_keys:
                    self.exif_tool_error_log.append(f'MISSING KEY: {key} - On {write_key}: Row: "{row_index}, '
                                                    f'filepath: "{filepath}"')
                    self._end_status()
                    self._error_msg(f'MISSING KEY: {key} - On {write_key}: Row: "{row_index}, filepath: "{filepath}"',
                                    fatal=False)
        return True

    @staticmethod
    def __delete_command_wrapper(delete_command: list[str], filepath: str) -> tuple[str, str]:
        """ Wrap a call to exiftool to delete tags """
        x = subprocess.run(delete_command + [filepath], capture_output=True)
        return Csv2Exif._prettify_success_message(x.stdout.decode("utf-8").replace('\n', '|')), \
               x.stderr.decode("utf-8").replace('\n', '|')

    @staticmethod
    def __write_command_wrapper(write_command: list[str], key_value_pair: str, filepath: str) -> tuple[str, str]:
        """ Wrap a call to exiftool to write tags """
        x = subprocess.run(write_command + [key_value_pair, filepath], capture_output=True)
        return Csv2Exif._prettify_success_message(x.stdout.decode("utf-8").replace('\n', '|')), \
               x.stderr.decode("utf-8").replace('\n', '|')

    @staticmethod
    def _prettify_success_message(msg: str) -> str:
        """ Transform "Rewriting" into "REWRITING:", "Editing tags in" into "EDITING TAGS IN" """
        return msg.replace('Rewriting', 'REWRITING:').replace('Editing tags in', 'EDITING TAGS IN')


parser = argparse.ArgumentParser(prog="csv2exif", description="Use exiftool to write exif data on jpgs according "
                                                              "to an input CSV and a set of mapping rules according "
                                                              "to naming standards: VRAE/ISADG/DC")
parser.add_argument('CSV_PATH', nargs=1, type=str, help='path for the CSV file to process.')
parser.add_argument('JPGS_PATH', nargs=1, type=str, help='root path for the JPG files.')
parser.add_argument('--row-progress-notify', '-r', nargs=1, type=int, help='how many rows between progress '
                                                                           'notifications. 100 by default', default=100)
parser.add_argument('--notify-broken-keys', '-n', type=bool, default=False,
                    help='Notify on broken/missing keys in the CSV. False by default.')
parser.add_argument('--max-depth', '-m', type=int, default=3, help='Max depth of sub-folders to look into when looking '
                                                                   'for JPGS. 3 by default')

parsed_args = (parser.parse_args())
C2E = Csv2Exif(parsed_args.CSV_PATH[0], parsed_args.JPGS_PATH[0], row_progress_notify=parsed_args.row_progress_notify,
               notify_on_broken_keys=parsed_args.notify_broken_keys, max_depth=parsed_args.max_depth)
C2E.run()
