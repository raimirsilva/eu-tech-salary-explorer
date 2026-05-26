"""
build_dataset.py
Junta salários (Eurostat) + PPP/PLI (Eurostat prc_ppp_ind)
e gera o dataset final: data/processed/salary_explorer.csv
"""

import pandas as pd
from pathlib import Path

Path("data/processed").mkdir(parents=True, exist_ok=True)

# Mapeamento nome completo -> código ISO-2 (confirmado com os 29 países do dataset)
NAME_TO_ISO = {
    "Austria":        "AT", "Belgium":     "BE", "Bulgaria":  "BG",
    "Croatia":        "HR", "Cyprus":      "CY", "Czechia":   "CZ",
    "Denmark":        "DK", "Estonia":     "EE", "Finland":   "FI",
    "France":         "FR", "Germany":     "DE", "Greece":    "EL",
    "Hungary":        "HU", "Ireland":     "IE", "Italy":     "IT",
    "Latvia":         "LV", "Lithuania":   "LT", "Luxembourg":"LU",
    "Malta":          "MT", "Netherlands": "NL", "Norway":    "NO",
    "Poland":         "PL", "Portugal":    "PT", "Romania":   "RO",
    "Slovakia":       "SK", "Slovenia":    "SI", "Spain":     "ES",
    "Sweden":         "SE", "Switzerland": "CH",
}

# ⚠️ Atenção: o Eurostat usa "EL" para a Grécia (não "GR" como o ISO padrão).
# O PPP dataset também usa "EL" — ok, o join vai funcionar.

def main():
    print("=== build_dataset.py ===")

    # --- Salários ---
    sal = pd.read_csv("data/raw/eurostat_salary_raw.csv")
    sal = sal.rename(columns={
        "Geopolitical entity (reporting)": "country",
        "value": "salary_monthly",
        "unit":  "unit",
    })
    sal = sal[["country", "unit", "salary_monthly"]].dropna()

    # Pivotar EUR e PPS para colunas separadas
    wide = sal.pivot_table(
        index="country", columns="unit", values="salary_monthly"
    ).reset_index()
    wide = wide.rename(columns={"EUR": "salary_eur", "PPS": "salary_pps"})
    wide["geo"] = wide["country"].map(NAME_TO_ISO)

    # --- PPP / PLI ---
    ppp = pd.read_csv("data/raw/ppp_clean.csv")
    ppp["geo"] = ppp["geo"].str.strip()

    # --- Join ---
    df = wide.merge(ppp, on="geo", how="left")

    # --- Calcular salário real ajustado pelo custo de vida ---
    # real_salary: quanto o salário EUR "rende" em termos de poder de compra
    # fórmula: salary_eur / (pli / 100)
    # ex: PT ganha €2.234, PLI=79 -> real = 2.234 / 0.79 = €2.827 "equivalentes"
    df["salary_real"] = (df["salary_eur"] / (df["pli_latest"] / 100)).round(0)

    # Gap entre nominal e PPS (%)
    df["eur_vs_pps_gap_pct"] = (
        (df["salary_eur"] - df["salary_pps"]) / df["salary_pps"] * 100
    ).round(1)

    # Salário anual estimado (mensal x 12)
    df["salary_eur_annual"]  = (df["salary_eur"]  * 12).round(0)
    df["salary_pps_annual"]  = (df["salary_pps"]  * 12).round(0)
    df["salary_real_annual"] = (df["salary_real"] * 12).round(0)

    # Ordenar por salário EUR
    df = df.sort_values("salary_eur", ascending=False).reset_index(drop=True)
    df["rank_eur"]  = df["salary_eur"].rank(ascending=False).astype(int)
    df["rank_real"] = df["salary_real"].rank(ascending=False).astype(int)

    # Salvar
    out_path = "data/processed/salary_explorer.csv"
    df.to_csv(out_path, index=False)

    print(f"OK -> {out_path}")
    print(f"Países no dataset final: {len(df)}")
    print(f"Colunas: {df.columns.tolist()}")
    print()
    print("=== Top 10 por salário EUR ===")
    print(df[["country","salary_eur","salary_real","pli_latest","rank_eur","rank_real"]]
          .head(10).to_string(index=False))
    print()
    print("=== Países onde o ranking MUDA mais (EUR vs Real) ===")
    df["rank_shift"] = (df["rank_real"] - df["rank_eur"]).abs()
    print(df[["country","salary_eur","salary_real","rank_eur","rank_real","rank_shift"]]
          .nlargest(5, "rank_shift").to_string(index=False))

if __name__ == "__main__":
    main()