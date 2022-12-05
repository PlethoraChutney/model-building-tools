#!/usr/bin/env python3
import argparse
import atomium as at
from glob import glob
import sys
import os

# ugh
aa_one_to_three = {
    'A': 'ALA',
    'R': 'ARG',
    'N': 'ASN',
    'D': 'ASP',
    'C': 'CYS',
    'E': 'GLU',
    'Q': 'GLN',
    'G': 'GLY',
    'H': 'HIS',
    'I': 'ILE',
    'L': 'LEU',
    'K': 'LYS',
    'M': 'MET',
    'F': 'PHE',
    'P': 'PRO',
    'S': 'SER',
    'T': 'THR',
    'W': 'TRP',
    'Y': 'TYR',
    'V': 'VAL'
}

aa_three_to_one = {aa_one_to_three[x]: x for x in aa_one_to_three.keys()}

canonicals = tuple(aa_one_to_three.values())

def seqs_from_fasta(filename: str) -> dict:
    sequences = {}
    curr_seq_name = None
    curr_seq = []

    with open(filename, 'r') as f:
        for line in f:
            if line[0] == '>':
                if curr_seq_name is not None:
                    sequences[curr_seq_name] = ''.join(curr_seq)
                # don't include \n
                curr_seq_name = line[1:-1]
                curr_seq = []
            else:
                curr_seq.append(line[:-1])

    if len(curr_seq) != 0:
        sequences[curr_seq_name] = ''.join(curr_seq)

    return sequences


def process_fastas(seq_glob: str) -> dict:
    # really big fastas will use up all your memory --- if I was
    # working with DNA, I'd return generators here. But I assume
    # nobody's using this to check the structure of a chromosome...

    fasta_seqs = {}

    fastas = glob(seq_glob)
    for fasta in fastas:
        new_seqs = seqs_from_fasta(fasta)
        if any(x in fasta_seqs for x in new_seqs.keys()):
            print(f'WARNING: {fasta} has overlapping sequence name.')
        fasta_seqs.update(new_seqs)

    return fasta_seqs

def find_mismatches(fastas: dict, model: at.Model, chain_pairs: list) -> dict:
    mismatches = {}

    for chain in chain_pairs:
        chain, seq = chain
        seq = fastas[seq]

        mismatches[chain] = []

        for res in model.chain(chain).residues():
            # zero-index
            num = int(res.id.split('.')[1]) - 1

            if res.name not in canonicals:
                print(f'Info: skipping chain {chain} residue {num} named {res.name}')
                continue

            fasta_res = aa_one_to_three[seq[num]]

            if res.name != fasta_res:
                mismatches[chain].append((
                    num + 1,
                    res.name,
                    fasta_res
                ))

    return mismatches

def main(args):
    if args.chain is None:
        print('Provide chain/sequences pairs using --chain. E.g., --chain A alpha to match chain A with sequence `alpha`.')
        sys.exit(1)

    fastas = process_fastas(args.sequence)
    model = at.open(args.model).model

    mismatches = find_mismatches(fastas, model, args.chain)

    for chain, mutations in mismatches.items():
        print(f'Found {len(mutations)} potential corrections in chain {chain}:')
        for m in mutations:
            print(f'\t{aa_three_to_one[m[1]]}{m[0]} -> {aa_three_to_one[m[2]]}')

    with open(f'mutate_{os.path.split(args.model)[1][:-4]}.cxc', 'w') as f:
        f.write(f'open {os.path.abspath(args.model)}\n')
        f.write(f'select "##name={os.path.split(args.model)[1]}"\n')
        for chain, mutations in mismatches.items():
            for m in mutations:
                f.write(f'swapaa "sel & /{chain}:{m[0]}" {m[2]}\n')

        f.write('\n')

    print('To make these mutations, run `mutate-model.cxc` in chimeraX.')


parser = argparse.ArgumentParser()

parser.add_argument(
    'model',
    help = 'Model to check.'
)
parser.add_argument(
    'sequence',
    help = 'Glob for fasta or fastas.'
)

parser.add_argument(
    '-c',
    '--chain',
    help = 'Pair chain to fasta sequence name. Must match exactly. Give once for each chain.',
    nargs = 2,
    action = 'append'
)

args = parser.parse_args()

main(args)