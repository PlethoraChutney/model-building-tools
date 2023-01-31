#!/usr/bin/env python3
# translator.py is used to translate residue numbers between
# human and mouse enac, because I am just so damn lazy.

import sys
import os
from mutator import process_fastas
from ca_bilder import make_fasta_pairs

fasta_dir = os.path.join(
    os.path.split(os.path.realpath(__file__))[0],
    'fastas'
)
if not os.path.exists(fasta_dir):
    print(f'Put aligned fastas in {fasta_dir}')
    sys.exit(1)

aligned_fastas = process_fastas(
    os.path.join(fasta_dir, 'aligned*.fasta')
)
m_to_h = {
    'a': make_fasta_pairs(
        aligned_fastas['mouse_alpha'],
        aligned_fastas['human_alpha']
    ),
    'b': make_fasta_pairs(
        aligned_fastas['mouse_beta'],
        aligned_fastas['human_beta']
    ),
    'g': make_fasta_pairs(
        aligned_fastas['mouse_gamma'],
        aligned_fastas['human_gamma']
    )
}
h_to_m = {
    'a': make_fasta_pairs(
        aligned_fastas['human_alpha'],
        aligned_fastas['mouse_alpha']
    ),
    'b': make_fasta_pairs(
        aligned_fastas['human_beta'],
        aligned_fastas['mouse_beta']
    ),
    'g': make_fasta_pairs(
        aligned_fastas['human_gamma'],
        aligned_fastas['mouse_gamma']
    )
}

unaligned_fastas = {
    'ha': aligned_fastas['human_alpha'],
    'hb': aligned_fastas['human_beta'],
    'hg': aligned_fastas['human_gamma'],
    'ma': aligned_fastas['mouse_alpha'],
    'mb': aligned_fastas['mouse_beta'],
    'mg': aligned_fastas['mouse_gamma']
}
unaligned_fastas = {key: unaligned_fastas[key].replace('-', '') for key in unaligned_fastas}

def parse_translate(query_string:str):
    q_species, q_chain, q_res_id = query_string[0].lower(), query_string[1], query_string[2:]

    q_resname = unaligned_fastas[q_species + q_chain][int(q_res_id) - 1]

    search_dict = h_to_m if q_species == 'h' else m_to_h
    reply_species = 'h' if q_species == 'm' else 'm'
    reply_id = search_dict[q_chain][q_res_id]
    reply_resname = unaligned_fastas[reply_species + q_chain][int(reply_id) - 1]

    print(f'{q_species}{q_chain.upper()}-{q_resname.upper()}{q_res_id} => {reply_resname.upper()}{reply_id}')



if __name__ == '__main__':
    parse_translate(sys.argv[1])