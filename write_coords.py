import atomium
import glob
import sys

try:
    models = glob.glob(sys.argv[1])
    print(models)
except IndexError:
    print('Give model glob')
    sys.exit()

lines = ['Model,Chain,ResNum,CA_X, CA_Y, CA_Z']

for filename in models:
    model = atomium.open(filename).model
    no_ext = filename[:-4]

    for res in model.residues():
        try:
            ca = res.atom(name = 'CA')
            assert ca is not None
        except (AttributeError, AssertionError):
            continue

        lines.append(
            ','.join([no_ext, *res.id.split('.'), *[str(x) for x in ca.location]])
        )

with open('c_alphas.csv', 'w') as f:
    f.write('\n'.join(lines))
    f.write('\n')