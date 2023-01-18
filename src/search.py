import pickle

from prettytable import PrettyTable

from parse import DATA_PATH, get_station_name

SEC_IN_HOUR = 3600
SEC_IN_MIN = 60


# Searching shortest way
def find_min_path(start_st, end_st):
    ''' This function searches the shortest way between start_st and end_st,
    which are given as station's id. It uses Dijkstra's algorithm. '''
    nodes, prev, dist_to_node = set(), {}, {start_st: 0}
    while True:
        node, cur_dist = None, None
        for x in dist_to_node:
            if x not in nodes:
                if node is None:
                    node, cur_dist = x, dist_to_node[x]
                else:
                    if dist_to_node[x] < cur_dist:
                        node, cur_dist = x, dist_to_node[x]
        if node is None:
            return None
        if node == end_st:
            result = [end_st]
            x = end_st
            while x != start_st:
                x = prev[x]
                result.append(x)
            return result, dist_to_node[end_st]
        nodes.add(node)
        for x in graph[node]:
            try:
                _ = int(x)
            except ValueError:
                continue
            if x not in nodes:
                if x not in dist_to_node:
                    dist_to_node[x], prev[x] = graph[node][x] + cur_dist, node
                else:
                    if dist_to_node[x] > graph[node][x] + cur_dist:
                        dist_to_node[x] = graph[node][x] + cur_dist
                        prev[x] = node


# 'Asking user' block
def ask_station():
    ''' Function which asks user to chose start/end line and start/end
    station using its id. As an argument we give 'start' or 'end'.'''
    # 'Chose line' block
    temp_lines = [(x['ordering'], x['id'], x['name']) for x in lines.values()]
    temp_lines.sort()

    temp_line_dict = {}

    my_table = PrettyTable(['Line No', 'Line name'])
    for (_, line_id, line_name), line_number in zip(
        temp_lines, range(1, 100)
    ):
        temp_line_dict[line_number] = line_id
        my_table.add_row([line_number, line_name])

    print(my_table)
    nline = input('\nEnter the number of line: ')
    nline = int(nline)
    nline = temp_line_dict[nline]

    # 'Chose station' block
    temp_stations_dict = {}
    n = 0
    my_table = PrettyTable(['Station No', 'Station name', 'Id_st'])
    for station in stations.values():
        if station['line_id'] == nline:
            n += 1
            my_table.add_row([
                n, get_station_name(station['id']), station['id']
            ])
            temp_stations_dict[n] = station['id']
    my_table.align['Station name'] = 'l'
    print(my_table)

    nstation = input('\nEnter the number of station: ')
    nstation = int(nstation)
    nstation = temp_stations_dict[nstation]
    return nstation


# 'Translate time' block
def show_time(time):
    hours = time // SEC_IN_HOUR
    minutes = (time % SEC_IN_HOUR) // SEC_IN_MIN
    seconds = time_x % SEC_IN_MIN

    return f'{hours}:{minutes}:{seconds}'


# Unpack pickle file
with open(DATA_PATH, 'rb') as dst:
    graph = pickle.load(dst)
    lines = pickle.load(dst)
    stations = pickle.load(dst)

# "Call 'ask' function" block
start_st = ask_station()
end_st = ask_station()
start_st_name = get_station_name(start_st)
end_st_name = get_station_name(end_st)
print(f'\nStart station is: {start_st_name}')
print(f'End station is: {end_st_name}')
print(f'Here is your shortest way between {start_st_name} and {end_st_name}:')
start_st, end_st = end_st, start_st   # It's for showing result in right order

# Call searching function
result = find_min_path(start_st, end_st)

# Create a readable result
if result:
    my_table = PrettyTable(['Time', 'Station name', 'id_st'])
    min_path, min_time = result
    x_prev = None
    time_x = 0
    for x in min_path:
        if x_prev:
            time_x += graph[x_prev][x]
        else:
            time_x = 0
        my_table.add_row([
            f'{show_time(time_x)}',
            f'{get_station_name(x)}',
            f'({x})'
        ])
        x_prev = x
    my_table.align['Station name'] = 'r'
    print(my_table)
    print(f'\nTotal time: {show_time(min_time)}')
else:
    print('The is no way between this stations')
