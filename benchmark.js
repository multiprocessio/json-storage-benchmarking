const fs = require('fs');

async function readBigJson(f) {
  let res = '';
  const reader = fs.createReadStream(f);
  reader.on('data', (d) => {
    try {
      res += d.toString();
    } catch (e) {
      console.log(d.toString(), res.length);
      throw e;
    }
  });

  return new Promise((resolve, reject) => {
    reader.on('close', () => {
      return JSON.parse(res);
    });
  });
}

async function bench_avg(f, runs, name) {
  const start = new Date();
  let res;
  for (let i = 0; i < runs; i++) {
    res = await f();
  }
  const end = new Date();
  console.log(`${name}\n\tAverage: ${(end - start) / runs}s`);
  return res;
}

let first_int_column = '';
let first_int_column_index = 0;
let headers = [];

async function array_of_arrays_testing(f) {
  const data = await bench_avg(() => readBigJson(f), 1, 'Read JSON');
  headers = data.unshift();
  for (let i = 0; i < header.length; i++) {
    const key = header[i];
    if (typeof data[0][i] === 'number') {
      first_int_column = key;
      first_int_column_index = i;
      break;
    }
  }

  function dosum() {
    let sum = 0;
    for (const row of data) {
      sum += row[first_int_column_index];
    }

    return sum;
  }

  const s = await bench_avg(dosum, 100, 'Sum int field');
  console.log(s);
  await bench_avg(() => data.slice().sort((r) => r[0]), 100, 'Sort by first field and take first 100')
}

async function array_of_objects_testing(f) {
  const data = await bench_avg(() => readBigJson(f), 1, 'Read JSON');

  function dosum() {
    let sum = 0;
    for (const row of data) {
      sum += row[first_int_column];
    }

    return sum;
  }

  const s = await bench_avg(dosum, 100, 'Sum int field');
  console.log(s);
  await bench_avg(() => data.slice().sort((r) => r[headers[0]]), 100, 'Sort by first field and take first 100')
}

async function columnar_testing(f) {
  const data = await bench_avg(() => readBigJson(f), 1, 'Read JSON');

  function dosum() {
    let sum = 0;
    for (const c of data[first_int_column_index].slice(1)) {
      sum += c;
    }

    return sum;
  }

  const s = await bench_avg(dosum, 100, 'Sum int field');
  console.log(s);

  function dosort() {
    const firstcol = data[0].slice(1);
    const guide = new Array(firstcol); // -1 to ignore header in first row
    for (let i = 0; i < len; i++) {
      guide[i] = i;
    }
    guide.sort((i, j) => firstcol[i] < firstcol[j] ? -1 : firstcol[i] > firstcol[j] ? 1 : 0);

    const rows = [];
    for (const i of guide.slice(0, 100)) {
      const row = [];
      for (const col of data) {
	row.push(col[i+1]);
      }

      rows.push(row)
    }

    return rows;
  }
  await bench_avg(dosort, 100, 'Sort by first field and take first 100')
}

async function main() {
  console.log('\n\nArray of arrays testing\n');
  await array_of_arrays_testing('array_of_arrays.json');

  console.log('\n\nArray of objects testing\n');
  await array_of_objects_testing('array_of_objects.json');

  console.log('\n\nColumnar testing\n');
  await columnar_testing('columnar.json');
}

main();
