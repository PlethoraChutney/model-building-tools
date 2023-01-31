#!/usr/bin/env python3
import atomium as at
from seaborn import color_palette
from math import sqrt
from mutator import process_fastas
import argparse
import sys

def distance(a1, a2) -> float:
    return sqrt(sum((a1[x] - a2[x])**2 for x in [0,1,2]))

def ca_locs(model:at.Model) -> dict:
    locs = {}
    def write_loc(loc):
        try:
            locs[chain][res_num] = loc
        except KeyError:
            locs[chain] = {res_num: loc}

    for res in model.residues():
        ca = res.atom(name = 'CA')
        chain, res_num = res.id.split('.')

        try:
            write_loc(ca.location)
        except AttributeError:
            continue


    return locs

def make_fasta_pairs(f1:str, f2:str) -> dict:
    # return a dict mapping residue id in model 1 to the aligned residue
    # id in model 2
    
    alignment = {}

    index_1 = 0
    skips_1 = 0
    index_2 = 0
    skips_2 = 0

    while index_1 < len(f1) and index_2 < len(f2):
        if f1[index_1] == '-':
            skips_1 += 1
        elif f2[index_2] == '-':
            skips_2 += 1
        else:
            # convert to strings b/c we're working with split atomium ids
            alignment[str(index_1 - skips_1)] = str(index_2 - skips_2)

        index_1 += 1
        index_2 += 1

    return alignment

def write_bild(mod_1:str, mod_2:str, alignments:dict, width, chain_dict: dict) -> None:
    mod_1 = at.open(mod_1).model
    mod_2 = at.open(mod_2).model

    lines = []
    dists = []

    mod_1_locs = ca_locs(mod_1)
    mod_2_locs = ca_locs(mod_2)

    for m1_chain, residues in mod_1_locs.items():
        m2_chain = chain_dict.get(m1_chain, m1_chain)

        if m2_chain not in mod_2_locs:
            continue

        for res_id in residues:
            if alignments is not None:
                res2_id = alignments[m1_chain][res_id]
            else:
                res2_id = res_id

            try:
                res_1_loc = residues[res_id]
                res_2_loc = mod_2_locs[m2_chain][res2_id]
            except KeyError:
                continue

            dist = distance(res_1_loc, res_2_loc)

            # dists is used to set our color scheme
            dists.append(dist)
            # still need to add something to lines to preserve
            # the cylinder distance relationship. We'll edit the
            # distance to the appropriate color later
            lines.append(f'X {dist}')

            # 0.5 at the end is the cylinder width.
            lines.append(f'.cylinder {" ".join(str(x) for x in res_1_loc)} {" ".join(str(x) for x in res_2_loc)} {width}\n')

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

def main(args):
    # dictionary matching chain in model 1 to chain in model 2
    # query using .get(key, missing) for default behavior
    chain_dict = {}
    if args.pair_chain is not None:
        for chain_pair in args.pair_chain:
            mod_1, mod_2 = chain_pair
            chain_dict[mod_1] = mod_2

    if args.fastas is not None:
        if args.chain_fasta is None:
            print('ERROR: If you are aligning different proteins, you must pair chains to fasta sequences using --chain-fasta')
            sys.exit()

        raw_fastas = process_fastas(args.fastas)

        # chain_fastas[model_num][chain] = fasta
        chain_fastas = {1: {}, 2:{}}
        for pair in args.chain_fasta:
            chain_fastas[int(pair[0])][pair[1]] = pair[2]

        # alignments[chain 1][index of chain 1] = [aligned index of corresponding chain in model 2]
        alignments = {}
        for c1 in chain_fastas[1].keys():
            c2 = chain_dict.get(c1, c1)
            fasta1 = raw_fastas[chain_fastas[1][c1]]
            fasta2 = raw_fastas[chain_fastas[2][c2]]
            alignments[c1] = make_fasta_pairs(fasta1, fasta2)

    else:
        alignments = None

    write_bild(*args.models, alignments, args.width, chain_dict)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'models',
        help = 'Location of two models to build cylinders between.',
        nargs = 2
    )
    parser.add_argument(
        '-f',
        '--fastas',
        help = 'If you are comparing models if different proteins, you must provide a fasta-format alignment (i.e., with dashes for indels).'
    )
    parser.add_argument(
        '-c',
        '--chain-fasta',
        help = 'Pair a model number, chain name, and a fasta name. Model 1 is the first model you provide. Give once per chain.)',
        nargs = 3,
        action = 'append'
    )
    parser.add_argument(
        '-p',
        '--pair-chain',
        help = 'Give two chain names: the first from model 1, and the second from model 2. These chains will have cylinders drawn between them. Default is to pair A with A, etc. Give once per pair.',
        nargs = 2,
        action = 'append'
    )
    parser.add_argument(
        '-w',
        '--width',
        help = 'Width of .bild cylinders. Default 0.5.',
        default="0.5"
    )

    args = parser.parse_args()

    main(args)