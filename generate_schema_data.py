import json
import sys

from faker import Faker

fake = Faker()

N = int(sys.argv[1])

keys = fake.words(200)
schema = {}
for key in keys:
    schema[key] = fake.random_choices((fake.iso8601, fake.paragraph, fake.random_int, fake.word), length=1)[0]

array_of_objects = []
for i in range(N):
    obj = {}
    if i % 10_000 == 0:
        print(f'Done generating {i} of {N} ({i / N * 100:.0f}%)')
    for key in keys:
        obj[key] = schema[key]()
    array_of_objects.append(obj)

print('Generated data')

with open('array_of_objects.json', 'w') as f:
    json.dump(array_of_objects, f)

print('Dumped array of objects')

array_of_arrays = [keys]
for row in array_of_objects:
    array_row = []
    for key in keys:
        array_row.append(row[key])
    array_of_arrays.append(array_row)

with open('array_of_arrays.json', 'w') as f:
    json.dump(array_of_arrays, f)

print('Dumped array of arrays')

columnar = [[] for key in keys]
for row in array_of_arrays:
    for i in range(len(keys)):
        columnar[i].append(row[i])

with open('columnar.json', 'w') as f:
    json.dump(columnar, f)

print('Dumped columnar')
