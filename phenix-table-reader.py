#!/usr/bin/env python
import sys
import re
import os
import glob
import pandas as pd

def parse_phenix_table(path):
    separated_path = path.split(os.path.sep)
    mb_root = separated_path.index('model-building')
    construct = separated_path[mb_root + 1]
    rsr_num = separated_path[mb_root + 3].replace('RealSpaceRefine_', '')

    with open(path, 'r') as f:
        lines = [re.split(r'\s{2,}', x.rstrip()) for x in f]

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
    tables = glob.glob(sys.argv[1])
    columns = [parse_phenix_table(x) for x in tables]

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
            'Ramachandran outliers (%)',
            'Ramachandran allowed (%)',
            'Ramachandran favored (%)',
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