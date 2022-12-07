#!/usr/bin/env python3
import atomium as at
import sys
from seaborn import color_palette
from math import sqrt


def distance(a1, a2):
    return sqrt(sum((a1[x] - a2[x])**2 for x in [0,1,2]))

mod_1 = at.open(sys.argv[1]).model
mod_2 = at.open(sys.argv[2]).model

lines = []
dists = []

for res_1 in mod_1.residues():
    ca_1 = res_1.atom(name = 'CA')
    if ca_1 is None:
        continue

    res_2 = mod_2.residue(id = res_1.id)
    if res_2 is None:
        continue
    ca_2 = res_2.atom(name = 'CA')
    if ca_2 is None:
        continue

    locs = []
    locs.extend([str(x) for x in ca_1.location])
    locs.extend([str(x) for x in ca_2.location])
    locs.append('0.5')

    dist = distance(ca_1.location, ca_2.location)
    dists.append(dist)

    lines.append(f'X {dist}')
    lines.append(f'.cylinder {" ".join(locs)}\n')


pal = color_palette('mako', len(dists))
pal = [[int(x * 255) for x in y] for y in pal]

dists.sort()

dist_color = {dists[i]: pal[i] for i in range(len(dists))}

with open('comparison.bild', 'w') as f:
    for line in lines:
        if line[0] == '.':
            f.write(line)
        else:
            dist = float(line[2:])
            color = dist_color[dist]
            color = " ".join(str(x) for x in color)
            f.write(f'.color {color}\n')