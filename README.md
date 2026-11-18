# Sporting goods retail in France: 27 years of monthly demand

A time series analysis of the INSEE monthly turnover index for retail sale of sporting equipment in specialised stores (NAF 47.64), January 1999 to August 2026.

**[View the report](https://theophilemt92.github.io/sport-retail-forecasting/)**

## What it covers

- **Stationarity:** ADF and KPSS tests on levels and differences
- **Decomposition:** robust STL (trend, seasonality, remainder)
- **Anomaly detection:** robust z-scores (median and MAD) on the STL remainder
- **Drift:** change points in trend growth (PELT) and shifts in the seasonal profile
- **Forecasting:** rolling-origin backtest of seasonal naive, ETS, ARIMA and Theta (`statsforecast`) and the Chronos-2 time series foundation model (zero-shot), with and without Covid neutralisation, checking both accuracy (MAPE, bias) and interval calibration

## Main results

- Trend growth fell from 4.7 % a year (2000-2019) to 0.8 % a year (2022-2025), in current euros.
- August has gained weight in the seasonal profile, December has lost weight, and the November trough has become shallower.
- Neutralising the Covid period cuts the ETS 12-month error from 7.9 % to 3.0 %.
- On this flat market, the seasonal naive benchmark (2.4 % MAPE) beats ETS, ARIMA and Theta.
- Chronos-2, used zero-shot, reaches 3.4 % MAPE, stays robust on uncleaned Covid data (3.6 % versus 7.9 % for ETS) and gives the best-calibrated 80 % intervals (81 % coverage).

## Repository contents

```
.
├── report.qmd               # Quarto source (Python)
├── index.html               # rendered report (served by GitHub Pages)
├── data/insee_ica_4764.csv  # INSEE series 010770520 (raw) and 010770580 (adjusted)
├── data/chronos_*.csv       # precomputed Chronos-2 forecasts
├── scripts/fetch_insee.py   # refreshes the data from the INSEE SDMX API
├── scripts/chronos_backtest.py  # Chronos-2 zero-shot backtest (CPU)
├── requirements.txt
├── requirements-chronos.txt # separate environment for PyTorch and Chronos
└── template/                # DataSphere Analytics report styling
```

## Reproducing it

Requires [Quarto](https://quarto.org) and Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/fetch_insee.py    # optional: refresh the data
quarto render report.qmd
```

To recompute the Chronos-2 forecasts (optional, the results are cached in `data/`):

```bash
python -m venv .venv-chronos
.venv-chronos/bin/pip install -r requirements-chronos.txt
.venv-chronos/bin/python scripts/chronos_backtest.py
```

## Data

INSEE, *Indice de chiffre d'affaires - Commerce de détail d'articles de sport en magasin spécialisé* (NAF rév. 2, 47.64), base 2021 = 100. Public data, [INSEE BDM](https://www.insee.fr/fr/statistiques/serie/010770520).

---

Théophile L. Mouton · [DataSphere Analytics](https://theophile-mouton.com)
