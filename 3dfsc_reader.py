#!/usr/bin/env python
import sys
import re
import shutil
import subprocess

def get_global_fsc(lineplot_filename:str) -> list: 
    # cryosparc puts the global fsc data directly into their python
    # plotting file

    with open(lineplot_filename, 'r') as f:
        lines = [x.strip() for x in f]

    global_fsc_lines = [x for x in lines if 'global' in x and x[-1] == ']']
    global_fsc_lines = [re.search(r'\[(.*)\]', x).group(1) for x in global_fsc_lines]
    global_fsc_lines = [[float(y) for y in x.split(', ')] for x in global_fsc_lines]

    return global_fsc_lines
    
def get_directional_histogram(histogram_filename:str) -> list:
    with open(histogram_filename, 'r') as f:
        hist_list = [float(x.strip()) for x in f if x.strip()]

    return hist_list

def main():
    if len(sys.argv) != 2:
        print('Usage: 3dfsc_reader.py {rename to}')
        sys.exit(1)

    global_fsc_x, global_fsc_y = get_global_fsc('lineplot.py')
    directional_hist = get_directional_histogram('histogram.lst')
    
    with open('3dfsc_results.csv', 'w') as f:
        f.write('GlobalX,GlobalY,DirectionalHist\n')
        while any(x for x in [global_fsc_x, global_fsc_y, directional_hist]):
            try:
                f.write(f'{global_fsc_x.pop(0)},')
            except IndexError:
                f.write('NA,')

            try:
                f.write(f'{global_fsc_y.pop(0)},')
            except IndexError:
                f.write('NA,')

            try:
                f.write(f'{directional_hist.pop(0)}\n')
            except IndexError:
                f.write('NA\n')

    subprocess.run(['Rscript', './plot_3dfsc.R'])
    shutil.move('processed_3dfsc.pdf', f'{sys.argv[1]}_3dfsc.pdf')
    shutil.move('processed_3dfsc.png', f'{sys.argv[1]}_3dfsc.png')

if __name__ == '__main__':
    main()
