#!/usr/bin/env python
import atomium as at
import sys

model = at.open(sys.argv[1]).model
model.optimise_distances()

for chain in model.chains():
    sugars = 0
    for res in chain.residues():
        if res.name == 'ASN':
            nd2 = [x for x in res.atoms() if x.name == 'ND2'][0]
            nearby_atoms = nd2.nearby_atoms(3)
            if any([x.name == 'C1' for x in nearby_atoms]):
                sugars += 1

    print(f'Chain {chain.id} has {sugars} glycans.')        
    