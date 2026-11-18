"""Zero-shot Chronos-2 backtest on the INSEE sporting goods series.

Same protocol as the report: 12-month horizon, origins August 2023, 2024 and 2025,
raw and Covid-neutralised history (March 2020 to May 2021 replaced by the robust
STL trend + seasonal fit). No training on this series: the model is used zero-shot.

Writes data/chronos_backtest.csv (one row per forecast point) and
data/chronos_forecast.csv (forecast from the last observation).
Runs on CPU in a few minutes. Usage: python scripts/chronos_backtest.py
"""
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from chronos import Chronos2Pipeline
from statsmodels.tsa.seasonal import STL

ROOT = Path(__file__).resolve().parent.parent
H = 12
QUANTILES = [0.025, 0.1, 0.5, 0.9, 0.975]
CUTOFFS = ["2023-08-01", "2024-08-01", "2025-08-01"]

torch.manual_seed(0)
df = pd.read_csv(ROOT / "data" / "insee_ica_4764.csv", parse_dates=["period"])
s = df.set_index("period")["brut"].asfreq("MS")

# Covid-neutralised series (same as report.qmd)
y = np.log(s)
stl = STL(y, period=12, robust=True, seasonal=13).fit()
clean = y.copy()
covid = (y.index >= "2020-03-01") & (y.index <= "2021-05-01")
clean[covid] = (stl.trend + stl.seasonal)[covid]
series = {"Raw data": s, "Covid neutralised": np.exp(clean)}

pipe = Chronos2Pipeline.from_pretrained("amazon/chronos-2", device_map="cpu")


def forecast(context):
    ctx = pd.DataFrame({"unique_id": "sport", "ds": context.index, "y": context.values})
    out = pipe.predict_df(ctx, prediction_length=H, quantile_levels=QUANTILES,
                          id_column="unique_id", timestamp_column="ds", target="y")
    out = out.rename(columns={str(q): f"q{q}" for q in QUANTILES})
    return out[["ds"] + [f"q{q}" for q in QUANTILES]]


rows = []
for variant, ser in series.items():
    for c in CUTOFFS:
        fc = forecast(ser.loc[:c])
        fc["cutoff"] = pd.Timestamp(c)
        fc["data"] = variant
        fc["y"] = s.reindex(fc["ds"]).values  # actuals are always the observed series
        rows.append(fc)
bt = pd.concat(rows, ignore_index=True)
bt.to_csv(ROOT / "data" / "chronos_backtest.csv", index=False)

final = forecast(series["Covid neutralised"])
final.to_csv(ROOT / "data" / "chronos_forecast.csv", index=False)

for variant, g in bt.groupby("data"):
    a, f = g["y"], g["q0.5"]
    cov = ((a >= g["q0.1"]) & (a <= g["q0.9"])).mean() * 100
    print(f"{variant}: MAPE {(abs(a - f) / a).mean() * 100:.2f} %, "
          f"bias {((f - a) / a).mean() * 100:+.2f} %, 80% coverage {cov:.0f} %")
