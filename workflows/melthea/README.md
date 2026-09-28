# MeltHEAs: Tsolid regression and live run

Reproduces the July 17, 2026 MeltHEAs analysis done through
[AURAMCP](https://nanohub.org/tools/auramcp) (built by Juan Carlos Verduzco, Daniel Mejia, and Mohnish
Harwani).

| File | What it is |
|---|---|
| `meltheas_regression.ipynb` | The analysis: data checks, rule-of-mixtures fit, model comparison, parity plots, novel composition |
| `data/meltheas_runs_jul17.csv` | The 2,000-run ResultsDB table returned by `get_data_from_nanohub` on July 17 (already filtered on Coexistence = 1, Converged = 1) |
| `data/reference_model_jul17.json` | Coefficients exported from the saved July model (`meltheas_Tsolid_model.pkl`, not committed) |
| `meltheas_temperature_predictor.py` | Standalone predictor used to choose `Tsolid` / `Tliquid` for the live run |
| `fetch_resultsdb.py` | Optional: re-pull fresh data from ResultsDB (needs `.env` credentials) |
| `figures/parity_rule_of_mixtures.png` | Parity plot for the linear model (matches the reported metrics) |
| `figures/poster_rf_parity_jul17.png` | The original poster figure, which shows **Random Forest**, not the linear model |

## Result

The notebook reproduces the July numbers exactly. One run (pure Cr, Tliquid/Tsolid = 2.4) breaks the 2× convention
and is dropped, which leaves 1,999 runs. An 80/20 split with `random_state=42` then gives test
**R² 0.983, MAE 19.2 K, RMSE 23.3 K** (n_test = 400). Refitting on all 1,999 runs recovers the saved July
coefficients to within 0.001 K.

```bash
cd workflows/melthea
jupyter nbconvert --to notebook --execute --inplace meltheas_regression.ipynb
```
