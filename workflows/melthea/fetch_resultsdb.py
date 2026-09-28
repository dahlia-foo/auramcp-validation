"""Pull converged, coexisting meltheas runs from nanoHUB ResultsDB into data/meltheas_runs.csv.

Sends the same `results/dbexplorer/search` request that AURAMCP's `get_data_from_nanohub` makes,
but authenticates with an OAuth password grant (credentials from .env), so it also works outside
a nanoHUB tool session.

    python workflows/melthea/fetch_resultsdb.py [--limit 2000]
"""
import argparse
import json
import os
from pathlib import Path

import nanohubremote as nr
import pandas as pd
from dotenv import load_dotenv

HERE = Path(__file__).resolve().parent
OUT = HERE / "data" / "meltheas_runs.csv"

INPUTS = [f"composition{i}" for i in range(1, 6)] + ["Tsolid", "Tliquid"]
OUTPUTS = ["Coexistence", "Converged", "melting_temperature", "melting_temperature_ci"] + [
    f"true_comp{i}" for i in range(1, 6)
]
FILTERS = [
    {"field": "output.Coexistence", "operation": "==", "value": 1},
    {"field": "output.Converged", "operation": "==", "value": 1},
]


def session() -> nr.Session:
    load_dotenv(HERE.parents[1] / ".env")
    return nr.Session({
        "grant_type": "password",
        "client_id": os.environ["NANOHUB_CLIENT_ID"],
        "client_secret": os.environ["NANOHUB_CLIENT_SECRET"],
        "username": os.environ["NANOHUB_USERNAME"],
        "password": os.environ["NANOHUB_PASSWORD"],
    })


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=2000)
    args = ap.parse_args()

    fields = [f"input.{f}" for f in INPUTS] + [f"output.{f}" for f in OUTPUTS] + ["revision"]
    search = {
        "tool": "meltheas",
        "filters": json.dumps(FILTERS),
        "results": json.dumps(fields),
        "limit": args.limit,
        "revision": 0,
        "sort": "revision",
        "sort_asc": 0,
        "simtool": 1,
        "valid_runs": 0,
    }
    resp = session().requestPost("results/dbexplorer/search", data=search, timeout=60)
    resp.raise_for_status()
    df = pd.DataFrame(resp.json()["results"])
    OUT.parent.mkdir(exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"wrote {len(df)} rows -> {OUT.relative_to(HERE.parents[1])}")


if __name__ == "__main__":
    main()
