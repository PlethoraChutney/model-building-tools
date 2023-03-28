import starfile
import sys
import subprocess
import shutil

if len(sys.argv) != 3:
    print('Usage: orientation_plotter.py {starfile name}')
    sys.exit(1)

df = starfile.read(sys.argv[1])
df = df['particles'][['rlnCoordinateX', 'rlnCoordinateY', 'rlnAngleRot', 'rlnAngleTilt', 'rlnAnglePsi']]
df.to_csv('processed-star.csv', index = False)
subprocess.run(['Rscript', 'plot-particles.R'])
shutil.move('processed-star.csv', sys.argv[1].replace(".star", "_orientations.csv"))
shutil.move('hexplot.pdf', sys.argv[1].replace(".star", "_plot.pdf"))