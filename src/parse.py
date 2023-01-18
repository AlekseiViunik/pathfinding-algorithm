import json
import os
import pickle
import sqlite3

from os.path import join, abspath

FILES_PATH = join('..', 'Data')
JSON_FILE_NAME = 'scheme.json'

# Pickle file doesn't have the extension. 
# You can name the file as you wish without it.
# The same for sqlite3 file
PICKLE_FILE_NAME = 'scheme.pickle'
SQL_FILE_NAME = 'scheme.sqlite3'

JSON_PATH = abspath(join(FILES_PATH, JSON_FILE_NAME))
DATA_PATH = abspath(join(FILES_PATH, PICKLE_FILE_NAME))
DB_PATH = abspath(join(FILES_PATH, SQL_FILE_NAME))


def get_station_name(id_st):
    '''There might be several stations with the same name 
    (for example 'Belorusskaya' has id 44, 176 and 313).
    But for our graph we need only one certain station with this name. '''
    try:
        st_text = stations[id_st]['name']
    except KeyError:
        st_text = f'<<< {id_st} >>>'
    try:
        line_text = lines[stations[id_st]['line_id']]['name']
    except KeyError:
        line_text = '??????'
    result = st_text + ' (' + line_text + ')'
    return result

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
for key in stations:
    graph[key] = {'name': get_station_name(key)}
for val in transitions.values():
    id1, id2, ln12 = val['from_id'], val['to_id'], val['length']
    pers, bi = val['perspective'], val['bi']
    if (id1 in graph) and (id2 in graph) and (not pers) and bi:
        graph[id1][id2] = ln12
        graph[id2][id1] = ln12
for val in connections.values():
    id1, id2, ln12 = val['from_id'], val['to_id'], val['length']
    pers, bi = val['perspective'], val['bi']
    if (id1 in graph) and (id2 in graph) and (not pers) and bi:
        graph[id1][id2] = ln12
        graph[id2][id1] = ln12    

# Save (pack) our graph's dict and others dict to pickle file.
# Order is important! First in - first out.
with open(DATA_PATH, 'wb') as destination:
    pickle.dump(graph, destination)
    pickle.dump(lines, destination)
    pickle.dump(stations, destination)
print(f'All data are saved in "{DATA_PATH}" file')


# If DB_file is created, we remove it in case it filled wrong.
try:
    os.remove(DB_PATH)
except FileNotFoundError:
    pass

# Connect Database
con = sqlite3.connect(DB_PATH)
cur = con.cursor()

create_request = '''
CREATE TABLE graphs(
    stn_id INTEGER PRIMARY KEY,
    name TEXT
);
CREATE TABLE stn12_times(
    stn12_id INTEGERER PRIMARY KEY,
    stn1 INTEGER,
    stn2 INTEGER,
    time INTEGER
);
CREATE TABLE lines(
    line_id INTEGERER PRIMARY KEY,
    id INTEGER,
    color TEXT,
    name TEXT,
    ordering INTEGER
);
CREATE TABLE stations(
    stn_id INTEGERER PRIMARY KEY,
    color TEXT,
    id INTEGER,
    name TEXT,
    ordering INTEGER,
    perspective INTEGER,
    line_id INTEGER
);
'''
try:
    cur.executescript(create_request)
except sqlite3.DatabaseError as err:
    print(f'Something is wrong (1), {err}!')
else: 
    print(f'Databese "{DB_PATH}" successfully created!')

try:
    # Fill 'graphs' table
    for x in graph:
        sdata = x, graph[x]['name']
        insert_request = 'INSERT INTO graphs (stn_id, name) VALUES (?, ?)'
        cur.execute(insert_request, sdata)

    # Fill 'stn12_times' table
    for x1 in graph:
        for x2 in graph[x1]:
            try:
                # We don't need 'name' field, which is in 'graph'. 
                _ = int(x2)
                sdata = x1, x2, graph[x1][x2]
                insert_request = '''
                    INSERT INTO stn12_times (stn1, stn2, time) 
                    VALUES (?, ?, ?)
                '''
                cur.execute(insert_request, sdata)
            except ValueError:
                continue
    
    # Fill 'lines' table
    for x in lines:
        sdata = (
            x,
            lines[x]['id'],
            lines[x]['color'],
            lines[x]['name'],
            lines[x]['ordering'],
        )
        insert_request = '''
            INSERT INTO lines (line_id, id, color, name, ordering) 
            VALUES (?, ?, ?, ?, ?)
        '''
        cur.execute(insert_request, sdata)
    
    # Fill 'stations' table
    for x in stations:
        sdata = (
            x,
            stations[x]['color'],
            stations[x]['id'],
            stations[x]['line_id'],
            stations[x]['name'],
            stations[x]['ordering'],
            stations[x]['perspective'],
        )
        insert_request = '''
            INSERT INTO stations (stn_id, color, id, line_id, name, ordering,
            perspective) VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        cur.execute(insert_request, sdata)
        
except sqlite3.DatabaseError as err:
    print(f'Something is wrong (2), {err}!')
else:
    con.commit()
    print(f'All requests are successfully created!')
con.close()
print('END')