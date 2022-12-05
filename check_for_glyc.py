#!/usr/bin/env python3
import atomium as at
import sys

if len(sys.argv) != 2:
    print('Usage: check_for_glyc.py {model-name}')
    sys.exit(1)

model = at.open(sys.argv[1]).model
potential_glycosylations = []

for chain in model.chains():
    for res in chain:
        if res.name == 'ASN' and res.next.next.name in ['THR', 'SER']:
            rc, rn = res.id.split('.')
            potential_glycosylations.append(f'view /{rc}:{rn}')

print(f'Found {len(potential_glycosylations)} potential glycosylation sites.')

with open(f'{sys.argv[1][:-4]}_glycs.html', 'w') as f:
    f.write('''
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Glycosylation sites</title>
        <style>.hidden {visibility: hidden; display: none;}</style>
    </head>
    <body>
        <div style="display: flex; flex-direction: column;">''')

    for glyc in potential_glycosylations:
        f.write(f'<a href="cxcmd:{glyc}">{glyc}</a>')
        
    f.write('''     </div>
    </body>
    <script>
        document.querySelectorAll('a').forEach((glycLink) => {
            glycLink.addEventListener('click', (e) => {
                e.target.classList.add('hidden');
            })
        });
    </script>
</html>''')

print(f'Open {sys.argv[1][:-4]}_glycs.html in chimeraX to view them.')