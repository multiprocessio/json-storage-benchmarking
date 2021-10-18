import json
from time import time

def bench_avg(f, runs, name):
    start = time();
    for i in range(runs):
        res = f()
    end = time()
    print(f'{name}\n\tAverage: {((end - start) / runs):10.2f}s')
    return res

print('Array of arrays testing')

with open('array_of_arrays.json') as f:
    [header, *data] = bench_avg(lambda: json.load(f), 1, 'Read JSON')
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
    s = bench_avg(lambda: sum([row[first_int_column_index] for row in data]), 100, 'Sum int field')
    print(s)
    bench_avg(lambda: sorted(data, key=lambda r: r[0])[:100], 100, 'Sort by first field and take first 100')

print('\n\nArray of objects testing\n')

with open('array_of_objects.json') as f:
    data = bench_avg(lambda: json.load(f), 1, 'Read JSON')
    s = bench_avg(lambda: sum([row[key] for row in data]), 100, 'Sum int field')
    print(s)
    bench_avg(lambda: sorted(data, key=lambda r: r[header[0]])[:100], 100, 'Sort by first field and take first 100')

print('\n\nColumnar testing\n')

with open('columnar.json') as f:
    data = bench_avg(lambda: json.load(f), 1, 'Read JSON')
    s = bench_avg(lambda: sum(data[first_int_column_index][1:]), 100, 'Sum int field')
    print(s)
    def data_sort():
        guide = sorted(range(len(data[0][1:])), key=lambda i: data[0][i+1])
        return [row[:1] + [row[i+1] for i in guide[:100]] for row in data]
    bench_avg(data_sort, 100, 'Sort by first field and take first 100')
