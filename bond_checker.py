import atomium

pko = atomium.open('121.pdb').model
deg = atomium.open('126.pdb').model

ids_in_both = []

for res in deg.residues():
    if pko.residue(id = res.id) is not None:
        ids_in_both.append(res.id)

pko_ca_distances = []
pko_bonds = []

for res_id in ids_in_both:
    chain, num = res_id.split('.')
    res = pko.residue(id = res_id)
    next_res = pko.residue(id = f'{chain}.{int(num) + 1}')
    if next_res is None:
        continue

    try:
        ca = res.atom(name = 'CA').location
        cc = res.atom(name = 'C').location
        next_ca = next_res.atom(name = 'CA').location
    except AttributeError:
        continue

    bond_length = (sum((ca[i]- cc[i])**2 for i in range(3)))**0.5
    ca_dist = (sum((ca[i]- next_ca[i])**2 for i in range(3)))**0.5

    pko_bonds.append(bond_length)
    pko_ca_distances.append(ca_dist)

deg_ca_distances = []
deg_bonds = []

for res_id in ids_in_both:
    chain, num = res_id.split('.')
    res = deg.residue(id = res_id)
    next_res = deg.residue(id = f'{chain}.{int(num) + 1}')
    if next_res is None:
        continue

    try:
        ca = res.atom(name = 'CA').location
        cc = res.atom(name = 'C').location
        next_ca = next_res.atom(name = 'CA').location
    except AttributeError:
        continue

    bond_length = (sum((ca[i]- cc[i])**2 for i in range(3)))**0.5
    ca_dist = (sum((ca[i]- next_ca[i])**2 for i in range(3)))**0.5

    deg_bonds.append(bond_length)
    deg_ca_distances.append(ca_dist)

pko_ca_distances.extend([''] * (len(deg_ca_distances) - len(pko_ca_distances)))
pko_bonds.extend([''] * (len(deg_bonds) - len(pko_bonds)))

pko_ca_distances = [str(x) for x in pko_ca_distances]
deg_ca_distances = [str(x) for x in deg_ca_distances]
pko_bonds = [str(x) for x in pko_bonds]
deg_bonds = [str(x) for x in deg_bonds]

with open('distances.csv', 'w') as f:
    f.write('PKO.ca,PKO/DEG.ca,PKO.bond,PKO/DEG.bond\n')
    f.write('\n'.join(','.join(x) for x in zip(pko_ca_distances, deg_ca_distances, pko_bonds, deg_bonds)))
    f.write('\n')
