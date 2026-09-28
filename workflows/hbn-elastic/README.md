# h-BN elastic constants: cellrelaxdft → elasticdft

This July 21, 2026 run computed the elastic constants of hexagonal boron nitride through
[AURAMCP](https://nanohub.org/tools/auramcp) (built by Juan Carlos Verduzco, Daniel Mejia, and Mohnish
Harwani). It chains two nanoHUB DFT Sim2Ls (Quantum ESPRESSO, PBEsol).

| File | What it is |
|---|---|
| `session_log_jul21.md` | Full export of the agent session, including every tool call, error, and retry |
| `data/elasticdft_output_jul21.json` | The raw `elasticdft` result (6×6 tensor and derived moduli), transcribed from the log |
| `vrh_moduli.py` | Recomputes the Voigt / Reuss / Hill moduli from the raw tensor and compares them with the tool's values |

## Pipeline

1. **Structure.** `Materials-Project-MCP:get_structure` was broken at the time (see
   [bug reports](../../docs/bug-reports.md)). The h-BN cell (mp-aaabikuu) was rebuilt by hand from
   `fetch_material` output instead.
2. **cellrelaxdft.** k-points 12 × 12 × 5, `bulk_m` = 1024 kbar (from MP's VRH bulk modulus). Relaxed to
   **a = 2.5024 Å, c = 7.1534 Å**.
   squid `cellrelaxdft/r99/62fb519a931e4abc1bdf0c5b4ff5a1c873c7e6ba`
3. **elasticdft.** Takes the cellrelaxdft **squid_id**, not a raw structure dict. The first job came back
   `not_found` after about 35 minutes (session TTL). The resubmitted job finished.
   squid `elasticdft/r27/29b00baeaf8558ac73d46617cea91f2c3694acfc`

## Result

| C11 | C12 | C13 | C33 | C44 | C66 |
|---|---|---|---|---|---|
| 820.7 | 189.9 | 2.4 | 3.7 | 2.3 | 314.3 GPa |

| | |
|---|---|
| Bulk modulus (VRH) | 114.6 GPa (Voigt 225.5, Reuss 3.7) |
| Shear modulus (VRH) | 82.2 GPa |
| Young's modulus | 199.1 GPa |
| Poisson's ratio | 0.210 |

```bash
cd workflows/hbn-elastic
python vrh_moduli.py   # reproduces every modulus above to 3 decimals
```

**Why C33 and C44 are tiny.** They describe out-of-plane and interlayer response. In h-BN, that response
comes from van der Waals bonding between the layers. PBEsol without a vdW correction barely binds the
layers, so these constants come out near zero. That is a known limit of the functional, not a bug in the
workflow. It is also why the Reuss bound (3.7 GPa) pulls the VRH bulk modulus far below the Voigt value.

**Note on the raw tensor.** The raw tensor is not quite symmetric (C12 = 189.9 vs. C21 = 191.5 GPa). elasticdft
derived its moduli from the matrix as returned, and `vrh_moduli.py` does the same.
