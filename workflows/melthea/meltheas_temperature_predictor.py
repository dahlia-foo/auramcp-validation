"""
meltheas_temperature_predictor.py

Predicts initial Tsolid / Tliquid values for the nanoHUB `meltheas` tool
(melting temperature of CrCoCuFeNi high-entropy alloys) that are likely to
produce a converged solid-liquid coexistence run on the first try.

Model
-----
Linear regression, no intercept, trained on composition (which sums to 1.0):

    Tsolid_predicted = sum(coef[element] * composition[element])
    Tliquid_predicted = 2 * Tsolid_predicted

Both design choices are empirical, derived from ResultsDB:
  - Tliquid = 2 x Tsolid held in 1999/2000 successful (Coexistence=1,
    Converged=1) historical runs pulled from nanoHUB ResultsDB (std = 0.009,
    i.e. essentially exact) -> this is a fixed convention, not something
    that needs to be searched.
  - A no-intercept linear ("rule of mixtures") fit of Tsolid on the five
    composition fractions achieves R^2 = 0.983 / MAE = 19.2 K / RMSE = 23.3 K
    on a held-out 20% test split (n=400) of 1999 successful runs. More
    flexible models (Ridge, degree-2 polynomial, RandomForest,
    GradientBoosting) were tried via 5-fold CV and gave no improvement,
    so the linear model was kept for simplicity/interpretability.

Coverage / caveats
-------------------
Training data spans composition1 (Cr) 0.0-1.0, and composition2-5
(Co, Cu, Fe, Ni) each 0.0-0.5, from 1999 historical successful runs.
Predictions inside this region are interpolation and should be reliable;
predictions far outside it (e.g. very high Co/Cu/Fe/Ni corners) are
extrapolation and less trustworthy. Coefficients are empirical fits, not
physical per-element melting points -- do not over-interpret them.

Usage
-----
    from meltheas_temperature_predictor import predict_temperatures

    Tsolid, Tliquid = predict_temperatures(
        {"Cr": 0.2, "Co": 0.2, "Cu": 0.2, "Fe": 0.2, "Ni": 0.2}
    )
"""

from __future__ import annotations

# Element -> composition field name expected by the meltheas tool.
ELEMENT_TO_FIELD = {
    "Cr": "composition1",
    "Co": "composition2",
    "Cu": "composition3",
    "Fe": "composition4",
    "Ni": "composition5",
}

# Fitted no-intercept linear regression coefficients (Kelvin),
# trained on 1999 successful meltheas ResultsDB runs.
COEFFICIENTS = {
    "Cr": 1252.18,
    "Co": 1424.96,
    "Cu": 783.88,
    "Fe": 1743.07,
    "Ni": 1426.88,
}

# Fixed empirical convention observed in 1999/2000 historical successful runs.
TLIQUID_OVER_TSOLID_RATIO = 2.0

# Model validation quality (held-out 20% test split, n=400).
MODEL_QUALITY = {
    "r2": 0.9831,
    "mae_kelvin": 19.2,
    "rmse_kelvin": 23.3,
    "n_train": 1599,
    "n_test": 400,
}

_TOLERANCE = 1e-6


def predict_temperatures(composition: dict) -> tuple:
    """
    Predict initial Tsolid and Tliquid (Kelvin) for a given HEA composition.

    Parameters
    ----------
    composition : dict
        Element fractions, e.g. {"Cr": 0.2, "Co": 0.2, "Cu": 0.2,
        "Fe": 0.2, "Ni": 0.2}. Keys must be a subset of
        {"Cr", "Co", "Cu", "Fe", "Ni"}; missing elements are treated as 0.
        Values must sum to 1.0 (within floating point tolerance).

    Returns
    -------
    (Tsolid, Tliquid) : tuple of float
        Suggested initial temperatures in Kelvin for the meltheas
        `Tsolid` and `Tliquid` inputs.

    Raises
    ------
    ValueError
        If an unknown element key is passed, or fractions don't sum to 1.0.
    """
    unknown = set(composition) - set(ELEMENT_TO_FIELD)
    if unknown:
        raise ValueError(f"Unknown element(s): {unknown}. Expected subset of {set(ELEMENT_TO_FIELD)}")

    total = sum(composition.values())
    if abs(total - 1.0) > _TOLERANCE:
        raise ValueError(f"Composition fractions must sum to 1.0, got {total}")

    Tsolid = sum(COEFFICIENTS[el] * frac for el, frac in composition.items())
    Tliquid = TLIQUID_OVER_TSOLID_RATIO * Tsolid
    return Tsolid, Tliquid


def to_meltheas_inputs(composition: dict, **overrides) -> dict:
    """
    Convenience helper: build a full `chosen_inputs` dict for run_sim2l,
    with predicted Tsolid/Tliquid filled in and any other meltheas inputs
    (box_length, time, rand_seed, etc.) passed through via **overrides.
    """
    Tsolid, Tliquid = predict_temperatures(composition)
    inputs = {ELEMENT_TO_FIELD[el]: frac for el, frac in composition.items()}
    inputs["Tsolid"] = Tsolid
    inputs["Tliquid"] = Tliquid
    inputs.update(overrides)
    return inputs


if __name__ == "__main__":
    example = {"Cr": 0.2, "Co": 0.2, "Cu": 0.2, "Fe": 0.2, "Ni": 0.2}
    Ts, Tl = predict_temperatures(example)
    print(f"Composition: {example}")
    print(f"Predicted Tsolid = {Ts:.1f} K, Tliquid = {Tl:.1f} K")
    print(f"Model quality (held-out): {MODEL_QUALITY}")
