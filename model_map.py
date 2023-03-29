#!/usr/bin/env python
import sys
import os
import shutil
import subprocess

if len(sys.argv) != 2:
    print('Usage: model_map.py {rename to}')
    sys.exit(1)

script_location = os.path.dirname(os.path.realpath(__file__))

with open('model_map_fsc.txt', 'r') as f:
    lines = [x.rstrip() for x in f]

with open('processed_table.csv', 'w') as f:
    f.write('Table,res,FSC\n')
    for line in lines:
        if line in ['Unmasked', 'Masked']:
            curr_table = line
        else:
            try:
                res, fsc = [float(x) for x in line.split()]
                f.write(f'{curr_table},{res},{fsc}\n')
            except ValueError:
                continue

subprocess.run([
    'Rscript',
    os.path.join(script_location, 'plot-model-map.R')
])
shutil.move('processed_table.csv', f'{sys.argv[1]}_model-map.csv')
shutil.move('model-map.pdf', f'{sys.argv[1]}_model-map.pdf')
