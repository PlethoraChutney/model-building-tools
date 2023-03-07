#!/usr/bin/env python
import sys
import re
import os
import glob
import pandas as pd

renamer = {
    'hum-pko': 'Digitonin',
    'hum-pko-nd': 'Nanodisc',
    'hum-pko-deg': 'Difab',
    'hum-pko-deg_monofab': 'Monofab',
    'jan-mouse-31': 'Uncleaved',
    'mouse-tryp': 'Trypsin'
}

def parse_phenix_table(path):
    print(path)
    separated_path = path.split(os.path.sep)
    mb_root = separated_path.index('model-building')
    construct = separated_path[mb_root + 1]
    construct = renamer[construct]

    try:
        with open(path, 'r') as f:
            lines = [re.split(r'\s{2,}', x.rstrip()) for x in f]
    except FileNotFoundError:
        return None

    # drop empty entries
    lines = [[y for y in x if y] for x in lines]
    lines = [x for x in lines if x]

    while lines:
        line = lines.pop(0)
        if line[0] == 'Atoms':
            num_atoms = f'{int(line[1].split(" ")[0]):,}'
        elif line[0] == 'Residues':
            num_residues = int(line[1].split(' ')[1])
        elif line[0] == 'Ligands':
            line[0] = line[1]
            is_ligand = True
            num_ligands = 0
            while is_ligand:
                ligand, number = line[0].split(': ')
                if ligand == 'UNK':
                    num_residues += int(number)
                else:
                    num_ligands += int(number)
                line = lines.pop(0)
                if line[0].split(' ')[0] == 'Bonds':
                    is_ligand = False
                    num_ligands = f'{num_ligands:,}'
                    num_residues = f'{num_residues:,}'
        elif line[0] == 'Length (Å) (# > 4σ)':
            length_rmsd = line[1].split(' ')[0]
        elif line[0] == 'Angles (°) (# > 4σ)':
            angle_rmsd = line[1].split(' ')[0]
        elif line[0] == 'MolProbity score':
            molprob_score = line[1]
        elif line[0] == 'Clash score':
            clash_score = line[1]
        elif line[0] == 'Ramachandran plot (%)':
            line = lines.pop(0)
            rama_outliers = line[1]
            line = lines.pop(0)
            rama_allowed = line[1]
            line = lines.pop(0)
            rama_favored = line[1]
            line = lines.pop(0)
        elif line[0] == 'Rotamer outliers (%)':
            rot_outliers = line[1]
        elif line[0] == 'Cβ outliers (%)':
            cbeta_outliers = line[1]
        elif line[0] == 'CaBLAM outliers (%)':
            cablam_outliers = line[1]
        elif line[0] == 'd FSC model (0/0.143/0.5)':
            fsc_res = line[1].split('/')[1]
        elif line[0] == 'CC (mask)':
            cc_mask = line[1]

    to_write = [
        construct,
        num_atoms, num_residues, num_ligands,
        length_rmsd, angle_rmsd, molprob_score,
        clash_score, rama_outliers, rama_allowed,
        rama_favored, rot_outliers, cbeta_outliers,
        cablam_outliers, fsc_res, cc_mask
    ]

    return to_write


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Give path to model building root. Each model should be in a subdir, and symlinked to the phenix project.')
        sys.exit(1)
    
    mb_root = sys.argv[1]
    latest_models = glob.glob(os.path.join(mb_root, '*', '*latest.pdb'))
    phenix_tables = [os.path.join(os.path.dirname(os.path.realpath(x)), 'table_one.txt') for x in latest_models]
    print(*phenix_tables, sep='\n')

    columns = [parse_phenix_table(x) for x in phenix_tables]
    columns = [x for x in columns if x]

    df = {
        'Section': ['Model Building'] * (len(columns[0]) - 1),
        'Parameter': [
            "No. non-H atoms",
            "No. residues",
            "No. ligands",
            "Bond length RMSD",
            "Bond angle RMSD",
            'Molprobity score',
            'Clash score',
            'Rama. outliers (%)',
            'Rama. allowed (%)',
            'Rama. favored (%)',
            'Rotamer outliers',
            'C&beta; outliers',
            'CaBLAM outliers',
            "Resolution (0.143 FSC)",
            "CC (mask)"
        ]
    }
    for column in columns:
        df[column[0]] = column[1:]

    pd.DataFrame(df).to_csv('processed_tables.csv', index=False)