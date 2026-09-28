"""Extract the ESMFold structure embedded in the 3Dmol HTML viewers and summarize pLDDT.

The `proteindl` (ESMFold) results were saved as standalone 3Dmol.js pages. Each page holds the
PDB text in a JavaScript string (`const pdbData = "..."`), with per-residue pLDDT in the B-factor
column. This script pulls that text out, writes it as a .pdb file, and reports the confidence stats.

Usage:
    python extract_plddt.py                  # both viewers in data/
    python extract_plddt.py path/to/page.html
"""
import json
import re
import sys
from pathlib import Path

DATA = Path(__file__).parent / "data"
DEFAULT_PAGES = [
    DATA / "esmfold_asna_backbone_trace.html",
    DATA / "esmfold_asna_ribbon_cartoon.html",
]

THREE_TO_ONE = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLN": "Q", "GLU": "E",
    "GLY": "G", "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F",
    "PRO": "P", "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V",
}

# Same bands as the viewer's colorfunc and the poster legend
BANDS = [("very high (>90)", 90, 101), ("high (70-90)", 70, 90), ("low (50-70)", 50, 70), ("very low (<=50)", -1, 50)]


def pdb_from_html(path):
    html = Path(path).read_text()
    m = re.search(r'const pdbData = ("(?:[^"\\]|\\.)*")', html)
    if not m:
        raise ValueError(f"no pdbData string found in {path}")
    return json.loads(m.group(1))


def ca_records(pdb_text):
    return [l for l in pdb_text.splitlines() if l.startswith("ATOM") and l[12:16].strip() == "CA"]


def summarize(path):
    pdb_text = pdb_from_html(path)
    out = Path(path).with_suffix(".pdb")
    out.write_text(pdb_text if pdb_text.endswith("\n") else pdb_text + "\n")

    ca = ca_records(pdb_text)
    plddt = [float(l[60:66]) for l in ca]
    seq = "".join(THREE_TO_ONE.get(l[17:20], "X") for l in ca)
    atoms = sorted({l[12:16].strip() for l in pdb_text.splitlines() if l.startswith("ATOM")})

    print(f"{Path(path).name}  ->  {out.name}")
    print(f"  atoms kept: {', '.join(atoms)}   residues: {len(ca)}")
    print(f"  sequence:   {seq[:30]}...{seq[-15:]}")
    print(f"  mean pLDDT: {sum(plddt) / len(plddt):.2f}   (min {min(plddt):.2f}, max {max(plddt):.2f})")
    for label, lo, hi in BANDS:
        n = sum(1 for b in plddt if lo < b <= hi)
        print(f"  {label:<16} {n:4d}  ({100 * n / len(plddt):.1f}%)")
    return seq, plddt


if __name__ == "__main__":
    pages = sys.argv[1:] or DEFAULT_PAGES
    results = [summarize(p) for p in pages]
    if len(results) > 1:
        same = all(r == results[0] for r in results[1:])
        print(f"\nSame sequence and per-residue pLDDT across pages: {same}")
