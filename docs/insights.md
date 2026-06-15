# Technical Decisions & API Notes — EU Tech Salary Explorer

Engineering notes from building the dataset: why this Eurostat dataset, the exact API parameters that work, and the errors solved along the way.

## Dataset choice

- **Code:** `earn_ses22_20`
- **Name:** Mean monthly earnings by sex, age and economic activity (2022)
- **Source:** Eurostat — Structure of Earnings Survey (SES)
- **Coverage:** 2022 only. The SES is a *structural* survey (run roughly every 4 years), not annual — so this is a cross-sectional snapshot, not a time series. A deliberate, documented limitation.

## Confirmed API dimensions

| Dimension | Value | Note |
|---|---|---|
| `freq` | `A` | Annual |
| `sex` | `T` | Total |
| `indic_se` | `ERN` | Gross earnings — **required**, and not obvious from the docs |
| `age` | `TOTAL` | All age groups |
| `sizeclas` | `GE10` | Companies with 10+ employees |
| `nace_r2` | `J` | Information & Communication (ICT) |
| `unit` | `EUR` / `PPS` / `NAC` | The dimension is named **`unit`**, not `currency` |
| `geo` | ISO-2 | Country |
| `time` | `2022` | Only year in this dataset |

## Validated request

```
https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/earn_ses22_20?format=JSON&lang=EN&sex=T&age=TOTAL&sizeclas=GE10&nace_r2=J&indic_se=ERN&unit=EUR&geo=PT&geo=DE&geo=LU
```

## First values confirmed — mean monthly gross ICT salary (EUR, 2022)

| Country | Monthly (€) | Est. annual (€) |
|---|---|---|
| Luxembourg (LU) | 5,943 | ~71,316 |
| Germany (DE) | 5,077 | ~60,924 |
| Portugal (PT) | 2,234 | ~26,808 |

> Spread PT → LU: +166%. PT → DE: +127%. These gaps are the heart of the project's story.

## Errors hit and resolved

| Error | Cause | Fix |
|---|---|---|
| `earn_ses_pub2s` returns 400 | Dataset renamed in 2025 | Use `earn_ses22_20` |
| `INVALID_QUERY_DIMENSION: CURRENCY` | Dimension doesn't exist in this dataset | Use `unit=EUR` / `unit=PPS` |

---
---

# Decisões Técnicas & Notas da API — EU Tech Salary Explorer

Notas de engenharia da construção do dataset: por que este dataset do Eurostat, os parâmetros de API que funcionam e os erros resolvidos no caminho.

## Escolha do dataset

- **Código:** `earn_ses22_20`
- **Nome:** Mean monthly earnings by sex, age and economic activity (2022)
- **Fonte:** Eurostat — Structure of Earnings Survey (SES)
- **Cobertura:** apenas 2022. O SES é uma pesquisa *estrutural* (roda a cada ~4 anos), não anual — então é um recorte transversal, não uma série temporal. Limitação assumida e documentada.

## Dimensões da API confirmadas

| Dimensão | Valor | Observação |
|---|---|---|
| `freq` | `A` | Anual |
| `sex` | `T` | Total |
| `indic_se` | `ERN` | Ganho bruto — **obrigatório**, e não óbvio na documentação |
| `age` | `TOTAL` | Todas as faixas etárias |
| `sizeclas` | `GE10` | Empresas com 10+ funcionários |
| `nace_r2` | `J` | Informação e Comunicação (TIC) |
| `unit` | `EUR` / `PPS` / `NAC` | A dimensão se chama **`unit`**, não `currency` |
| `geo` | ISO-2 | País |
| `time` | `2022` | Único ano neste dataset |

## Requisição validada

```
https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/earn_ses22_20?format=JSON&lang=EN&sex=T&age=TOTAL&sizeclas=GE10&nace_r2=J&indic_se=ERN&unit=EUR&geo=PT&geo=DE&geo=LU
```

## Primeiros valores confirmados — salário mensal bruto médio em TIC (EUR, 2022)

| País | Mensal (€) | Anual estimado (€) |
|---|---|---|
| Luxemburgo (LU) | 5.943 | ~71.316 |
| Alemanha (DE) | 5.077 | ~60.924 |
| Portugal (PT) | 2.234 | ~26.808 |

> Gap PT → LU: +166%. PT → DE: +127%. Esses números são o coração do storytelling do projeto.

## Erros encontrados e resolvidos

| Erro | Causa | Solução |
|---|---|---|
| `earn_ses_pub2s` retorna 400 | Dataset renomeado em 2025 | Usar `earn_ses22_20` |
| `INVALID_QUERY_DIMENSION: CURRENCY` | Dimensão não existe neste dataset | Usar `unit=EUR` / `unit=PPS` |
