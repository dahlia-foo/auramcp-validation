# Protein structure: E. coli AsnA with ESMFold

The July 2026 protein-structure workflow was run through
[AURAMCP](https://nanohub.org/tools/auramcp) (built by Juan Carlos Verduzco, Daniel Mejia, and Mohnish
Harwani). The prompt to the agent was *"Predict the shape of the following protein sequence"*, given the sequence
of asparagine synthetase A from E. coli (UniProt P00963, 330 residues). The agent found and ran the `proteindl`
(ESMFold) Sim2L.

| File | What it is |
|---|---|
| `data/esmfold_asna_backbone_trace.html` | Original 3Dmol viewer from the ESMFold run (Jul 17): Cα trace colored by pLDDT. This is the poster's "Backbone format" panel. |
| `data/esmfold_asna_ribbon_cartoon.html` | Second viewer of the **same** prediction, made later for the poster: backbone atoms (N, Cα, C, O) drawn as a cartoon. This is the "Ribbons and Segments" panel. |
| `data/*.pdb` | PDB text extracted from each viewer. pLDDT is in the B-factor column. |
| `extract_plddt.py` | Pulls the PDB out of the HTML and reports the sequence, mean pLDDT, and confidence bands |

Open either HTML file in a browser to rotate the structure.

## Result

```bash
cd workflows/protein
python extract_plddt.py
```

Both viewers contain the same 330-residue model with identical per-residue pLDDT:

| | |
|---|---|
| Mean pLDDT | **90.19** (min 60.43, max 96.35) |
| Very high (>90) | 227 residues (68.8%) |
| High (70–90) | 94 (28.5%) |
| Low (50–70) | 9 (2.7%) |
| Very low (≤50) | 0 |

The bands match the viewer's color scheme and the poster legend.

## AlphaFold comparison (not reproduced here)

The same sequence was also run through `alphafold231`, which took retries after the job expired. The July
notes record that prediction as having a mean pLDDT of **97.95**, and the Kabsch Cα RMSD between it and the ESMFold model
was **0.62 Å**. The AlphaFold structure was not saved, so these two numbers can't be checked from this
folder. The 0.62 Å figure compares two predictions with each other. It is not a comparison against an
experimental structure.

The poster's "pLDDT 90–98" range comes from these two runs. Both poster images are ESMFold. An earlier pLDDT
chart (90.2 / 70.7) came from an unrelated alpha-synuclein test and is not used here.
