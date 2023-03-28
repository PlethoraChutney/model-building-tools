import starfile
import sys
import subprocess
import shutil

if len(sys.argv) != 3:
    print('Usage: orientation_plotter.py {starfile name} {output base name}')
    sys.exit(1)

df = starfile.read(sys.argv[1])
df = df['particles'][['rlnCoordinateX', 'rlnCoordinateY', 'rlnAngleRot', 'rlnAngleTilt', 'rlnAnglePsi']]
df.to_csv('processed-star.csv', index = False)
subprocess.run(['Rscript', 'plot-particles.R'])
shutil.move('processed-star.csv', f'{sys.argv[2]}_orientations.csv')
shutil.move('hexplot.pdf', f'{sys.argv[2]}_plot.pdf')