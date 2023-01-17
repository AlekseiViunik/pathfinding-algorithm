import json

from os.path import join, abspath


JSON_PATH = join('.', 'Data', 'scheme.json')
JSON_PATH = abspath(JSON_PATH)
print(JSON_PATH)

# Get dict from json as scheme. File closes automaticaly
with open(JSON_PATH, 'rt', encoding='utf-8') as src:
    scheme = json.load(src)

# Get lines info from scheme
lines = {}
for line_id in scheme['data']['lines']:
    lines[line_id['id']] = {
        'id': line_id['id'],
        'name': line_id['name']['ru'],
        'ordering': line_id['ordering'],
        'color': line_id['color']
    }

# Get stations info from scheme
stations = {}
for metro in scheme['data']['stations']:
    stations[metro['id']]={
        'id': metro['id'],
        'name': metro['name']['ru'],
        'ordering': metro['ordering'],
        'line_id': metro['lineId'],
        'perspective': metro['perspective'],
        'color': lines[metro['lineId']]['color'],
    }

# Get transitions info from scheme
transitions = {}
for trans in scheme['data']['transitions']:
    transitions[trans['id']] = {
        'id': trans['id'],
        'from_id': trans['stationFromId'],
        'to_id': trans['stationToId'],
        'perspective': trans['perspective'],
        'bi': trans['bi'],
        'length': trans['pathLength']
    }

# Get connections info from scheme
connections = {}
for con in scheme['data']['connections']:
    connections[con['id']] = {
        'id': con['id'],
        'from_id': con['stationFromId'],
        'to_id': con['stationToId'],
        'length': con['pathLength'],
        'perspective': con['perspective'],
        'bi': con['bi'],
    }

# Graph's creation
graph = {}

print('END')