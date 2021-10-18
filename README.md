## To generate fake data

```
pip3 install faker
python3 ./generate_schema_data.py 1_000_000
```

## To run the benchmarks

```
python3 ./benchmark.py
+------------------+--------------+--------------------+----------------------------------------+---------------------+-----------------------------+
|                  |  Read JSON   |   Sum int field    | Sort by first field and take first 100 | Sort by first field | Group by first field, count |
+------------------+--------------+--------------------+----------------------------------------+---------------------+-----------------------------+
| array of arrays  | 40.54s (N/A) | 0.27s (4999013444) |      1.02s (1970-01-01T00:18:47)       |     1.01s (N/A)     |       0.69s (999668)        |
+------------------+--------------+--------------------+----------------------------------------+---------------------+-----------------------------+
| array of objects | 47.35s (N/A) | 0.35s (4999013444) |      1.09s (1970-01-01T00:18:47)       |     1.09s (N/A)     |       0.72s (999668)        |
+------------------+--------------+--------------------+----------------------------------------+---------------------+-----------------------------+
|     columnar     | 29.19s (N/A) | 0.01s (4999013444) |      0.51s (1970-01-01T00:18:47)       |    49.30s (N/A)     |       0.94s (999668)        |
+------------------+--------------+--------------------+----------------------------------------+---------------------+-----------------------------+
```