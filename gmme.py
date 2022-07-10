"""
version 0.3.1
date 2022-07-10
HvdWolf (Surfer63)

----------
Use ExifTool, by Phil Harvey to write XMP, EXIF and IPTC metadata on jpgs according to an input CSV and a set of mapping rules according to naming
standards: VRAE/ISADG/DC

Usage:
    python3 gmme.py

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
----------

ExifTool [https://exiftool.org/]
THIS script [https://github.com/MuseosAbiertos/mme/]

LICENCE
  This is free software; you can redistribute it and/or modify it under GNU General Public License v3.0

VERSIONS
v0.1 First code
v0.2 Any corrections, help, howtos
v0.3 GUI version (Thanks to @hvdwolf)

"""
import os
import sys
import csv
import time
import json
import datetime
import platform
import subprocess
import webbrowser

from typing import Optional
from pathlib import Path

import colorama  # type: ignore

import PySimpleGUI as sg
import ui_layout

# Some global variables
csvfile = True
jpgfolder = True
baselogfile = "" # Use it as copy for output_name

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
colorama.init()

def _get_log_path() -> str:
    """ Get and create log folder"""
    log_path = str(Path.home()) + os.path.sep + 'gcsv2exif_logs'
    if not os.path.isdir(log_path):
        os.mkdir(log_path)
    return log_path


def _get_current_time() -> str:
    """ Get the current date and time as a string """
    now = datetime.datetime.now()
    return f'{now.year}-{now.month}-{now.day} {"{:02d}".format(now.hour)}:' \
           f'{"{:02d}".format(now.minute)}:{"{:02d}".format(now.second)}'


def _get_current_time_for_filename() -> str:
    """ Get the current date and time fixed for usage in filenames """
    return _get_current_time().replace(':', '-')


class MME:
    """ Main class """
    DELETE_VRAE_TAGS = ['exiftool', '-v', '-xmp-vrae:all=']
    DELETE_ISADG_TAGS = ['exiftool', '-v', '-xmp-isadg:all=']
    DELETE_DC_TAGS = ['exiftool', '-v', '-xmp-dc:all=']

    WRITE_VRAE_TAGS = ['exiftool', '-config', f'{SCRIPT_PATH}/data/exiftool_configs/vrae.config']
    WRITE_ISADG_TAGS = ['exiftool', '-config', f'{SCRIPT_PATH}/data/exiftool_configs/isadg.config']
    WRITE_DC_TAGS = ['exiftool']

    def __init__(self, window: sg.Window, csv_filepath: str, images_root_path: str, row_progress_notify: int = 100,
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
            window.Element('_sgOutput_').Update(f'_read_maps failed to decode the JSON file, with exception: {str(e)}\n', append=True)
        except FileNotFoundError as e:
            self._error_msg(f'_read_maps failed to found the file: {str(e)}')
            window.Element('_sgOutput_').Update(f'_read_maps failed to found the file: {str(e)}\n', append=True)

    def _read_csv(self) -> list[dict]:  # type: ignore
        """ Read the CSV and create a list of dictionary from it """
        try:
            with open(self.csv_filepath, 'r', encoding='utf-8') as r_file:
                csv_reader = csv.DictReader(r_file)
                return [d for d in csv_reader]
        except FileNotFoundError as e:
            self._error_msg(f'_read_csv failed to found the file: {str(e)}')
            window.Element('_sgOutput_').Update(f'_read_csv failed to found the file: {str(e)}\n', append=True)

    def _save_logs(self) -> None:
        """ Save the error and success logs for the sessions """
        output_name = self.csv_filepath.split('/')[-1].replace('.csv', '')
        window.Element('_baselogfile_').Update(f'_{output_name}-{_get_current_time_for_filename()}.txt')
        output_name = f'{_get_log_path()}/%s_{output_name}-{_get_current_time_for_filename()}.txt'
        with open(output_name % 'error_log', 'w', encoding='utf-8') as w_file:
            w_file.write('\n'.join(self.exif_tool_error_log))
        with open(output_name % 'success_log', 'w', encoding='utf-8') as w_file:
            w_file.write('\n'.join(self.exif_tool_success_log))

    def _validate_image_path(self):
        """ Check that the image_path exists/is not empty """
        if not list(os.walk(self.images_root_path)):
            self._error_msg(f'_validate_image_path found no files/directory at: f{self.images_root_path} (Does the '
                            f'path exist?')
            window.Element('_sgOutput_').Update('_validate_image_path found no files/directory at: f{self.images_root_path} (Does the '
                            f'path exist?\n', append=True)

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
        window.Element('_sgOutput_').Update(f'Starting script with CSV path: "{self.csv_filepath}", {len(self.rows)} rows, and '
                       f'root image path: "{self.images_root_path}" at {_get_current_time()}\n', append=True)
        self._info_msg(f'This might take a while...')
        window.Element('_sgOutput_').Update(f'This might take a while...\n', append=True)

        for index, row in enumerate(self.rows):
            if index % self.row_progress_notify == 0:
                if index != 0:
                    self._end_status()
                self._info_msg(f'Progress: {index}/{len(self.rows)}. Errors: {len(self.exif_tool_error_log)}, '
                               f'Successes: {len(self.exif_tool_success_log)}')
                window.Element('_sgOutput_').Update(f'Progress: {index}/{len(self.rows)}. Errors: {len(self.exif_tool_error_log)}, '
                               f'Successes: {len(self.exif_tool_success_log)}\n', append=True)

            csv_index = index + 2  # CSV Row index, for proper debugging

            # 1 - Check the row has a "File Name"
            filename = self.__get_file_name(csv_index, row)
            if not filename:
                continue  # Next row
            filepath = self.__get_file_path(csv_index, filename)
            if not filepath:
                continue  # Next row

            # 2 - Delete tags
            delete_map = {'DELETE VRAE TAGS': MME.DELETE_VRAE_TAGS,
                          'DELETE ISADG TAGS': MME.DELETE_ISADG_TAGS,
                          'DELETE DC TAGS': MME.DELETE_DC_TAGS}

            for delete_key in delete_map.keys():
                self._status_msg(f'{index}/{len(self.rows)} - {delete_key} on {filename}')
                window.Element('_sgOutput_').Update(f'{index}/{len(self.rows)} - {delete_key} on {filename}\n', append=True)
                if not self.__delete_command(csv_index, filepath, delete_key, delete_map[delete_key]):
                    continue  # Next row

            # 3 - Write tags
            write_map = {'WRITE VRAE TAGS': [self.maps['vrae'], MME.WRITE_VRAE_TAGS],
                         'WRITE ISADG TAGS': [self.maps['isadg'], MME.WRITE_ISADG_TAGS],
                         'WRITE DC TAGS': [self.maps['dc'], MME.WRITE_DC_TAGS]}

            for write_key in write_map.keys():
                tag_map, write_command = write_map[write_key]
                self._status_msg(f'{index}/{len(self.rows)} - {write_key} on {filename}')
                window.Element('_sgOutput_').Update(f'{index}/{len(self.rows)} - {write_key} on {filename}\n', append=True)

                # Mark row as successfully written if there were no errors
                if self.__write_command(csv_index, row, filepath, write_key, tag_map, write_command):
                    self.exif_tool_success_log.append(f'On {write_key}: Row: "{csv_index}", filepath: "{filepath}"')
                #window.Element('_sgOutput_').Update(f'On {write_key}: Row: "{csv_index}", filepath: "{filepath}"\n', append=True)

        # 4 - Write error/success logs
        self._end_status()
        self._info_msg(f'\n\nWriting logs to folder {_get_log_path()} ...')
        window.Element('_sgOutput_').Update(f'\nWriting logs to folder: {_get_log_path()} ...\n', append=True)
        self._save_logs()

        self._info_msg(f'Finished processing {len(self.rows)} with {len(self.exif_tool_error_log)} errors '
                       f'and {len(self.exif_tool_success_log)} successes at {_get_current_time()}')
        window.Element('_sgOutput_').Update(f'Finished processing {len(self.rows)} with {len(self.exif_tool_error_log)} errors '
                       f'and {len(self.exif_tool_success_log)} successes at {_get_current_time()}\n', append=True)
        end_time = time.time()
        self._info_msg(f'Script took: {str(datetime.timedelta(seconds=(end_time - start_time)))}')
        window.Element('_sgOutput_').Update(f'Script took: {str(datetime.timedelta(seconds=(end_time - start_time)))}\n', append=True)

    def __get_file_name(self, row_index: int, row: dict) -> Optional[str]:
        """ Get row's filename, or log an error if the "File Name" column is empty. """
        if not row.get('File Name'):
            self.exif_tool_error_log.append(f'Row "{row_index}": No "File Name" column, or empty.')
            self._end_status()
            self._error_msg(f'Row "{row_index}": No "File Name" column, or empty.', fatal=False)
            window.Element('_sgOutput_').Update(f'Row "{row_index}": No "File Name" column, or empty.\n', append=True)
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
            window.Element('_sgOutput_').Update(f'Row "{row_index}": File not found in this path: "{filename}"\n', append=True)
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
            window.Element('_sgOutput_').Update(f'On {delete_key}: Row: "{row_index}", filepath: "{filepath}", ERROR: "{error}"\n',append=True)
            return False
        elif success:
            self.exif_tool_success_log.append(f'On {delete_key}: Row: "{row_index}", filepath: "{filepath}", '
                                              f'SUCCESS: "{success}"')
            window.Element('_sgOutput_').Update(f'On {delete_key}: Row: "{row_index}", filepath: "{filepath}", 'f'SUCCESS: "{success}"\n', append=True)
            return True
        else:
            self._end_status()
            self._error_msg(f'FATAL ERROR: Invalid return (no error nor success): On {delete_key}: '
                            f'Row: "{row_index}", filepath: "{filepath}".')  # Fatal error
            window.Element('_sgOutput_').Update(f'FATAL ERROR: Invalid return (no error nor success): On {delete_key}: '
                            f'Row: "{row_index}", filepath: "{filepath}".\n',append=True)
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
                    window.Element('_sgOutput_').Update(f'On {write_key}: Row: "{row_index}", filepath: "{filepath}", Row key: {key},'
                                    f' ERROR: "{error}"\n', append=True)
                    return False
            else:
                if self.notify_on_broken_keys:
                    self.exif_tool_error_log.append(f'MISSING KEY: {key} - On {write_key}: Row: "{row_index}, '
                                                    f'filepath: "{filepath}"')
                    self._end_status()
                    self._error_msg(f'MISSING KEY: {key} - On {write_key}: Row: "{row_index}, filepath: "{filepath}"',
                                    fatal=False)
                    window.Element('_sgOutput_').Update(f'MISSING KEY: {key} - On {write_key}: Row: "{row_index}, filepath: "{filepath}"\n', append=True)
        return True

    @staticmethod
    def __delete_command_wrapper(delete_command: list[str], filepath: str) -> tuple[str, str]:
        """ Wrap a call to exiftool to delete tags """
        x = subprocess.run(delete_command + [filepath], capture_output=True)
        # Shows also all exiftool output
        #window.Element('_sgOutput_').Update(value=x.stdout.decode("utf-8"), append=True)
        #window.Element('_sgOutput_').Update(value=x.stderr.decode("utf-8"), append=True)
        #window.refresh()
        return MME._prettify_success_message(x.stdout.decode("utf-8").replace('\n', '|')), \
               x.stderr.decode("utf-8").replace('\n', '|')


    @staticmethod
    def __write_command_wrapper(write_command: list[str], key_value_pair: str, filepath: str) -> tuple[str, str]:
        """ Wrap a call to exiftool to write tags """
        x = subprocess.run(write_command + [key_value_pair, filepath], capture_output=True)
        # Shows also all exiftool output
        #window.Element('_sgOutput_').Update(value=x.stdout.decode("utf-8"), append=True)
        #window.Element('_sgOutput_').Update(value=x.stderr.decode("utf-8"), append=True)
        #window.refresh()
        return MME._prettify_success_message(x.stdout.decode("utf-8").replace('\n', '|')), \
               x.stderr.decode("utf-8").replace('\n', '|')

    @staticmethod
    def _prettify_success_message(msg: str) -> str:
        """ Transform "Rewriting" into "REWRITING:", "Editing tags in" into "EDITING TAGS IN" """
        return msg.replace('Rewriting', 'REWRITING:').replace('Editing tags in', 'EDITING TAGS IN')



##### --- Start of Main part --- #####
# Display the GUI to the user in the standard system default theme
sg.theme('SystemDefault1') # I really dislike all these colourful, childish themes.
window =  ui_layout.create_and_show_gui()


while True:
    event, values = window.Read(timeout=100)
    if event == sg.WIN_CLOSED or event == '_Close_' or event == 'Exit':
        break
    elif event == '_WriteExif_':
        if values['-CSVFILE-'] == '' or len(values['-CSVFILE-']) == 0:
            sg.popup("You did not provide/select a CSV file.")
            csvfile = False
        if values['-IMGFOLDER-'] == '' or len(values['-IMGFOLDER-']) == 0:
            sg.popup("You did not provide/select a folder containing your JPG files.")
            jpgfolder = False
        if csvfile and jpgfolder:
            window['_ViewLogs_'].update(disabled=True)
            if values['_clean_output_']:
                window.Element('_sgOutput_').Update('', append=False)
            try:
                C2E = MME(window, values['-CSVFILE-'], values['-IMGFOLDER-'], row_progress_notify=int(values['-row-progress-notify-']),
                               notify_on_broken_keys=values['-notify-broken-keys-'], max_depth=int(values['-max-depth-']))
                C2E.run()
                window['_ViewLogs_'].update(disabled=False)
                window.Element('_sgOutput_').Update(baselogfile, append=True)
            except Exception as ex:
                print(ex)
    elif event == '_ViewLogs_':
        if platform.system() == 'Windows':
            os.startfile(f'{_get_log_path()}/error_log' + values['_baselogfile_'])
            os.startfile(f'{_get_log_path()}/success_log' + values['_baselogfile_'])
        elif platform.system() == 'Darwin':
            subprocess.call(['open', '-a', 'TextEdit', f'{_get_log_path()}/error_log' + values['_baselogfile_']])
            subprocess.call(['open', '-a', 'TextEdit', f'{_get_log_path()}/success_log' + values['_baselogfile_']])
        else:
            webbrowser.open(f'{_get_log_path()}/error_log' + values['_baselogfile_'])
            webbrowser.open(f'{_get_log_path()}/success_log' + values['_baselogfile_'])
window.Close()
