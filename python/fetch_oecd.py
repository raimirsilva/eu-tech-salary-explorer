"""
fetch_oecd.py
Baixa Purchasing Power Parities (PPP) por país via Eurostat
dataset prc_ppp_ind — Price Level Indices (base EU=100).
Salva CSV cru em data/raw/ppp_raw.csv
"""

import eurostat
import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

DATASET = "prc_ppp_ind"

def main():
    print("=== fetch_oecd.py (via Eurostat PPP) ===")
    print("  Baixando Price Level Indices...")

    df = eurostat.get_data_df(DATASET)

    # Filtrar: PLI base EU27=100, categoria consumo privado agregado
    pli = df[
        (df["na_item"] == "PLI_EU27_2020") &
        (df["ppp_cat"] == "A0101")
    ].copy()

    # Normalizar: renomear coluna geo, manter só anos relevantes
    pli = pli.rename(columns={"geo\\TIME_PERIOD": "geo"})
    anos = [str(a) for a in range(2018, 2025)]
    cols = ["geo"] + [a for a in anos if a in pli.columns]
    pli = pli[cols]

    # Pegar o ano mais recente disponível por país (ignora NaN)
    pli["pli_latest"] = pli[cols[1:]].apply(
        lambda row: row.dropna().iloc[-1] if row.dropna().shape[0] > 0 else None,
        axis=1
    )
    pli["pli_year"] = pli[cols[1:]].apply(
        lambda row: row.dropna().index[-1] if row.dropna().shape[0] > 0 else None,
        axis=1
    )

    out = pli[["geo", "pli_latest", "pli_year"]].dropna()
    out_path = RAW_DIR / "ppp_clean.csv"
    out.to_csv(out_path, index=False)

    print(f"  Países com PLI: {len(out)}")
    print(f"\nOK -> {out_path}")
    print("\nAmostra (top 5 mais caros):")
    print(out.nlargest(5, "pli_latest")[["geo","pli_latest","pli_year"]].to_string(index=False))
    print("\nAmostra (5 mais baratos):")
    print(out.nsmallest(5, "pli_latest")[["geo","pli_latest","pli_year"]].to_string(index=False))

if __name__ == "__main__":
    main()