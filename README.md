# Model Building Tools

Little scripts to simplify model building. Most require atomium.

## ca-bilder.py

Build cylinders between CA atoms of two models.

If you want to compare two different proteins, you've got a bit more work to do.

1. Prepare FASTA alignments and provide to `--fastas`
2. Provide a mapping between model 1 chains and model 2 chains using `--pair-chain`
3. Provide a mapping between all model chains and their fasta sequences using `--chain-fasta`

## check_for_glyc.py

Read through a model sequence and locate potential N-glycosylation sites.
The script will print sites to the terminal, and generate an HTML file.
The HTML file has ChimeraX command links to view each glycosylation site,
and the links disappear as they are clicked (functioning as a checklist)

## mutator.py

Check a model sequence against a FASTA file. Sites of model/FASTA mismatch
are printed to the terminal, and a chimeraX `.cxc` command file is
generated to mutate all mismatches to the FASTA sequence.

You'll need to tell the script which chain belongs to which FASTA. If your protein.fasta is:

```
>whatever
AAFAKLCA...
```

then you'll need to give `--chain A whatever` as an argument to match
that sequence to chain A of your model.

Known mutations can be given in mutation `.txt` files, with one
mutation per line. If you're using multiple mutants off the same
construct, this'll save you from having to make a bunch of FASTAs.

For instance, if you have `protein.fasta` and a model that should
have that sequence, except chain A has a mutation of C260K and chain
B has A120F, for instance, you could provide a text file `mutant.txt`:

```
/A:C260K
/B:A120F
```

and that'll take care of the mismatches between the FASTA and
your model.

## write_cords.py

Just writes out the model, chain, residue number, and
X, Y, Z coords for the CAs of a model. I know that's all in the PDB,
but god is the PDB format a pain.

## Validation

It's good to validate your map and model. I've included a few
helpers, but they're specific to my situation so might take
a bit of modification.

`3dfsc_reader.py` reads in 3DFSC results files from cryoSPARC and
produces a nicer plot. You need `histogram.lst` and `lineplot.py`
from the cryoSPARC job.

`orientation_plotter.py` re-plots the Euler orientation angle heatmap.
I mostly wrote it because I hate the cryoSPARC default color theme,
it's probably not broadly necessary.

`model_map.py` re-plots model-map FSC values from phenix. No
modifications are made --- it's just a bit prettier.

`phenix_table_reader.py` reads in refinement tables exported
from phenix. It's set up in a bit of a weird way: it'll look
for a .pdb file ending in "latest.pdb". It expects that to
be a symlink to a phenix job. It'll look in that phenix job
for `table_one.txt`, which it will read and make a column
of a combined table. This is probably not that useful unless
you think about building models the same way I do, and you're building
a lot of them.
