""" Transform notion's tables copy-pastes into a JSON dictionary. """

import re
import json
re_pattern_notion_maps = re.compile(r'^\|(?P<csv_var>.*)\|(?P<tag>.*)\|$')
maps = {'vrae': {}, 'isadg': {}, 'dc': {}}


with open('vrae_map.txt', 'r', encoding='utf-8') as r_file:
    vrae_map_txt = r_file.read().split('\n')

with open('isdag_map.txt', 'r', encoding='utf-8') as r_file:
    isdag_map_txt = r_file.read().split('\n')

with open('dublin_map.txt', 'r', encoding='utf-8') as r_file:
    dublin_map_txt = r_file.read().split('\n')

for line in vrae_map_txt:
    match = re.search(re_pattern_notion_maps, line)
    csv_var = match.group('csv_var').strip()
    tag = match.group('tag').strip()
    maps['vrae'][csv_var] = tag

for line in isdag_map_txt:
    match = re.search(re_pattern_notion_maps, line)
    csv_var = match.group('csv_var').strip()
    tag = match.group('tag').strip()
    maps['isadg'][csv_var] = tag

for line in dublin_map_txt:
    match = re.search(re_pattern_notion_maps, line)
    csv_var = match.group('csv_var').strip()
    tag = match.group('tag').strip()
    maps['dc'][csv_var] = tag

json.dump(maps, open('maps.json', 'w', encoding='utf-8'), indent=4)
