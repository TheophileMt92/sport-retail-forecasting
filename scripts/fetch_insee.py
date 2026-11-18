"""Download the INSEE turnover index for sporting goods retail (NAF 47.64).

Series 010770520: raw (brut). Series 010770580: seasonally and calendar adjusted (CVS-CJO).
Writes data/insee_ica_4764.csv with columns period, brut, cvs.

Usage: python scripts/fetch_insee.py
"""
import re
import ssl
import urllib.request
from pathlib import Path

URL = "https://bdm.insee.fr/series/sdmx/data/SERIES_BDM/010770520+010770580"
SERIES = {"010770520": "brut", "010770580": "cvs"}
OUT = Path(__file__).resolve().parent.parent / "data" / "insee_ica_4764.csv"


def main():
    try:
        import certifi
        ctx = ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        ctx = ssl.create_default_context()
    xml = urllib.request.urlopen(URL, timeout=60, context=ctx).read().decode("utf-8")
    values = {}
    for block in re.findall(r"<Series (.*?)</Series>", xml, re.S):
        idbank = re.search(r'IDBANK="(\d+)"', block).group(1)
        for period, value in re.findall(r'TIME_PERIOD="([^"]+)" OBS_VALUE="([^"]+)"', block):
            values.setdefault(period, {})[SERIES[idbank]] = value
    OUT.parent.mkdir(exist_ok=True)
    with open(OUT, "w") as f:
        f.write("period,brut,cvs\n")
        for p in sorted(values):
            f.write(f"{p},{values[p].get('brut', '')},{values[p].get('cvs', '')}\n")
    print(f"Wrote {len(values)} months to {OUT} (last: {max(values)})")


if __name__ == "__main__":
    main()
