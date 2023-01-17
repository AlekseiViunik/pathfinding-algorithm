import json

from os.path import join, abspath


JSON_PATH = join('.', 'Data', 'scheme.json')
JSON_PATH = abspath(JSON_PATH)
print(JSON_PATH)

# Get dict from json as scheme. File closes automaticaly
with open(JSON_PATH, 'rt', encoding='utf-8') as src:
    scheme = json.load(src)

lines = {}
for line_id in scheme['data']['lines']:
    lines[line_id['id']] = {
        'id': line_id['id'],
        'name': line_id['name']['ru'],
        'ordering': line_id['ordering'],
        'color': line_id['color']
    }

stations = {}
for metro in scheme['data']['stations']:
    stations[metro['id']]={
        'id': metro['id'],
        'name': metro['name']['ru'],
    }
print('END')