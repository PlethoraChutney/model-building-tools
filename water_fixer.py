#!/usr/bin/env python
import sys
import re
import os

path_to_pdb = os.path.abspath(os.path.realpath(sys.argv[1]))

with open(path_to_pdb) as f:
    lines = [x for x in f]

water_num = 0
with open(path_to_pdb.replace('.pdb', '_modified.pdb'), 'w') as f:
    for line in lines:
        if (re.search(r'HOH [A-Z]', line)):
            water_num += 1
            line = re.sub(r'HOH [A-Z]', 'HOH H', line)
            line = re.sub(r'HOH H([ 0-9]{4})', f'HOH H{water_num: >4}', line)
        
        f.write(line)
