"""Recompute the h-BN Voigt-Reuss-Hill moduli from the raw elasticdft tensor (Jul 21 run).

The tensor is used as returned (not symmetrized), which is what elasticdft itself did: the
Voigt bulk modulus it reports equals the sum of the raw upper-left 3x3 block divided by 9.

Usage:
    python vrh_moduli.py
"""
import json
from pathlib import Path

import numpy as np

run = json.loads((Path(__file__).parent / "data" / "elasticdft_output_jul21.json").read_text())
C = np.array(run["elastic_tensor"])
S = np.linalg.inv(C)

k_voigt = C[:3, :3].sum() / 9
g_voigt = (np.trace(C[:3, :3]) - (C[0, 1] + C[0, 2] + C[1, 2]) + 3 * np.trace(C[3:, 3:])) / 15
k_reuss = 1 / S[:3, :3].sum()
g_reuss = 15 / (4 * np.trace(S[:3, :3]) - 4 * (S[0, 1] + S[0, 2] + S[1, 2]) + 3 * np.trace(S[3:, 3:]))
k_vrh = (k_voigt + k_reuss) / 2
g_vrh = (g_voigt + g_reuss) / 2
youngs = 9 * k_vrh * g_vrh / (3 * k_vrh + g_vrh)
poisson = (3 * k_vrh - 2 * g_vrh) / (6 * k_vrh + 2 * g_vrh)

rep = run["reported"]
rows = [
    ("Bulk modulus, Voigt (GPa)", k_voigt, rep["bulk_modulus_voigt"]),
    ("Bulk modulus, Reuss (GPa)", k_reuss, rep["bulk_modulus_reuss"]),
    ("Bulk modulus, VRH (GPa)", k_vrh, rep["bulk_modulus_vrh"]),
    ("Shear modulus, VRH (GPa)", g_vrh, rep["shear_modulus_vrh"]),
    ("Young's modulus (GPa)", youngs, rep["youngs_modulus"]),
    ("Poisson's ratio", poisson, rep["homogeneous_poisson"]),
]
print(f"{'':28}{'recomputed':>12}{'elasticdft':>12}")
for name, ours, theirs in rows:
    print(f"{name:28}{ours:12.3f}{theirs:12.3f}")
print(f"\nAsymmetry max |C - C^T| = {np.abs(C - C.T).max():.2f} GPa (C12 vs C21, C13 vs C31)")
