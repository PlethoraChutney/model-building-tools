#!/usr/bin/env python
import starfile
import sys
import subprocess
import shutil
import os

if len(sys.argv) != 2:
    print('Usage: orientation_plotter.py {starfile name}')
    sys.exit(1)

script_location = os.path.dirname(os.path.realpath(__file__))

df = starfile.read(sys.argv[1])
df = df['particles'][['rlnCoordinateX', 'rlnCoordinateY', 'rlnAngleRot', 'rlnAngleTilt', 'rlnAnglePsi']]
df.to_csv('processed-star.csv', index = False)
subprocess.run(['Rscript', os.path.join(script_location, 'plot-particles.R')])
shutil.move('processed-star.csv', sys.argv[1].replace(".star", "_orientations.csv"))
shutil.move('hexplot.pdf', sys.argv[1].replace(".star", "_plot.pdf"))
if os.path.exists('Rplots.pdf'):
    os.remove('Rplots.pdf')