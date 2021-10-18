import json
from time import time

from beautifultable import BeautifulTable

table = BeautifulTable()
table.max_table_width=150

tests = {}

def bench_avg(storage, f, runs, name, sv=None):
    if not storage:
        raise Exception('Missing storage')
    start = time();
    for i in range(runs):
        res = f()
    end = time()
    if name not in tests:
        tests[name] = []
    tests[name].append({ 'time': f'{((end - start) / runs):.2f}s', 'signal': sv(res) if sv else 'N/A', 'storage': storage })
    return res

print('Testing arrays')

with open('array_of_arrays.json') as f:
    [header, *data] = bench_avg('array of arrays', lambda: json.load(f), 1, 'Read JSON')
    first_int_column = header[0]
    first_int_column_index = 0
    for i, key in enumerate(header):
        try:
            int(data[0][i])
            first_int_column = key
            first_int_column_index = i
            break
        except:
            pass
    bench_avg('array of arrays', lambda: sum([row[first_int_column_index] for row in data]), 5, 'Sum int field', lambda a: a)
    bench_avg('array of arrays', lambda: sorted(data, key=lambda r: r[0])[:100], 5, 'Sort by first field and take first 100', lambda a: a[0][0])
    bench_avg('array of arrays', lambda: sorted(data, key=lambda r: r[0]), 5, 'Sort by first field')

    def group():
        matches = {}
        for row in data:
            if row[0] not in matches:
                matches[row[0]] = 0
            matches[row[0]] += 1

        return list(matches.items())

    bench_avg('array of arrays', group, 5, 'Group by first field, count', lambda g: len(g))

print('Testing objects')

with open('array_of_objects.json') as f:
    data = bench_avg('array of objects', lambda: json.load(f), 1, 'Read JSON')
    bench_avg('array of objects', lambda: sum([row[key] for row in data]), 5, 'Sum int field', lambda a: a)
    bench_avg('array of objects', lambda: sorted(data, key=lambda r: r[header[0]])[:100], 5, 'Sort by first field and take first 100', lambda n: n[0][header[0]])
    bench_avg('array of objects', lambda: sorted(data, key=lambda r: r[header[0]]), 5, 'Sort by first field')

    def group():
        matches = {}
        key = header[0]
        for row in data:
            if row[key] not in matches:
                matches[row[key]] = 0
            matches[row[key]] += 1

        return list(matches.items())

    bench_avg('array of objects', group, 5, 'Group by first field, count', lambda g: len(g))

print('Testing columnar')

with open('columnar.json') as f:
    data = bench_avg('columnar', lambda: json.load(f), 1, 'Read JSON')
    columns = [r[0] for r in data]
    data = [r[1:] for r in data]
    bench_avg('columnar', lambda: sum(data[first_int_column_index]), 5, 'Sum int field', lambda a: a)
    def data_sort(n=None):
        guide = sorted(range(len(data[0])), key=lambda i: data[0][i])
        return [[row[i] for i in (guide[:n] if n else guide)] for row in data]
    bench_avg('columnar', lambda: data_sort(100), 5, 'Sort by first field and take first 100', lambda n: n[0][0])
    bench_avg('columnar', data_sort, 5, 'Sort by first field')

    def group():
        matches = {}
        for val in data[0]:
            if val not in matches:
                matches[val] = 0
            matches[val] += 1

        return list(matches.items())

    bench_avg('columnar', group, 5, 'Group by first field, count', lambda g: len(g))

table.columns.header = tests.keys()
storages = [t['storage'] for t in tests[list(tests.keys())[0]]]

for storage in storages:
    row = []
    for testname in tests.keys():
        for t in tests[testname]:
            if (t['storage'] == storage):
                row.append(t['time'] + f' ({t["signal"]})')

    table.rows.append(row)

table.rows.header = storages
print(table)
