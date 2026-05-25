"""
fetch_eurostat_salary.py
Baixa salários médios mensais do setor TIC (nace_r2=J) por país EU,
em EUR e PPS, via Eurostat API (dataset earn_ses22_20).
Salva CSV cru em data/raw/eurostat_salary_raw.csv
"""

import requests
import pandas as pd
from pyjstat import pyjstat
from pathlib import Path

BASE = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
DATASET = "earn_ses22_20"
RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

# 27 países EU + Noruega, Suíça, Reino Unido
GEO = [
    "AT","BE","BG","HR","CY","CZ","DK","EE","FI","FR","DE","EL","HU","IE",
    "IT","LV","LT","LU","MT","NL","PL","PT","RO","SK","SI","ES","SE",
    "NO","CH","UK"
]

# Parâmetros fixos confirmados na sessão de 25/05
BASE_PARAMS = {
    "format": "JSON",
    "lang":   "EN",
    "sex":      "T",
    "age":      "TOTAL",
    "sizeclas": "GE10",
    "nace_r2":  "J",
    "indic_se": "ERN",
}

def fetch(unit: str) -> pd.DataFrame:
    """Busca uma unidade (EUR ou PPS) e devolve DataFrame longo."""
    params = {**BASE_PARAMS, "unit": unit}
    # geo como lista — requests repete a chave automaticamente
    geo_params = [("geo", g) for g in GEO]

    print(f"  Baixando unit={unit}...")
    resp = requests.get(
        f"{BASE}/{DATASET}",
        params=list(params.items()) + geo_params,
        timeout=60
    )
    resp.raise_for_status()

    dataset = pyjstat.Dataset.read(resp.text)
    df = dataset.write("dataframe")
    df["unit"] = unit
    return df

def main():
    print("=== fetch_eurostat_salary.py ===")
    frames = []
    for unit in ("EUR", "PPS"):
        df = fetch(unit)
        frames.append(df)
        print(f"  {unit}: {len(df)} linhas, {df['value'].notna().sum()} com valor")

    out = pd.concat(frames, ignore_index=True)
    out_path = RAW_DIR / "eurostat_salary_raw.csv"
    out.to_csv(out_path, index=False)

    print(f"\nOK -> {out_path}")
    print(f"Total linhas: {len(out)}")
    print(f"Países com dados (EUR): {out[out['unit']=='EUR']['Geopolitical entity (reporting)'].nunique()}")
    print("\nAmostra (top 5 por salário EUR):")
    eur = out[out['unit']=='EUR'].dropna(subset=['value'])
    print(eur.nlargest(5, 'value')[['Geopolitical entity (reporting)','value']].to_string(index=False))

if __name__ == "__main__":
    main()