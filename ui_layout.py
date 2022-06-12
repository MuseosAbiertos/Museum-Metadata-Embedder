# -*- coding: utf-8 -*-

import PySimpleGUI as sg

def create_and_show_gui():
    folderfileframelayout = [
        [sg.Text('Specify the path for the CSV file to process.')],
        [sg.Input('', key='-CSVFILE-', size=(100, 1)), sg.FileBrowse()],
        [sg.Text('Specify the root path for the JPG files.')],
        [sg.Input('', key='-IMGFOLDER-', size=(100, 1)), sg.FolderBrowse()],
    ]

    optionslayout = [
        [sg.Checkbox('Notify on broken/missing keys in the CSV.', key='-notify-broken-keys-', enable_events=True)],
        [sg.Text('Max depth of sub-folders to scan for JPGS.'),
         sg.Combo(values=sorted(('1', '2', '3', '4', '5', '6')), default_value='3', size=(3, 1), key='-max-depth-')],
        [sg.Text('how many rows between progress notifications'),
         sg.Combo(values=sorted(('025', '050', '100', '150', '200', '250')), default_value='100', size=(4, 1), key='-row-progress-notify-')],
    ]

    layout = [
        [sg.Frame('CSV file and JPGs root folder', folderfileframelayout)],
        [sg.Frame('Options', optionslayout)],
        [sg.Text('Output:')],
        [sg.Multiline(size=(140, 30), key = '_sgOutput_', autoscroll=True, auto_refresh=True)],
        [sg.Push(),
         sg.Button('write EXIF metadata', font=('Calibri', 10, 'bold'), key='_WriteExif_'),
         sg.Button('Close', font=('Calibri', 10, 'bold'), key='_Close_')]
    ]

    # Open the window and return it to main script
    return sg.Window('csv2exif', layout)
