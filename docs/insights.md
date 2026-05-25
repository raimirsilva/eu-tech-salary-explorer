# Insights e decisões técnicas — EU Tech Salary Explorer

---

## Sessão 25/05/2026 — Exploração da API Eurostat

### Dataset escolhido
- **Código:** `earn_ses22_20`
- **Nome:** Mean monthly earnings by sex, age and economic activity (2022)
- **Fonte:** Eurostat — Structure of Earnings Survey (SES)
- **Único ano disponível:** 2022 (o SES não é anual — é estrutural, roda a cada ~4 anos)

### Dimensões confirmadas via API
| Dimensão | Código usado | Descrição |
|---|---|---|
| `freq` | `A` | Annual |
| `sex` | `T` | Total (homens + mulheres) |
| `indic_se` | `ERN` | Gross earnings ← **obrigatório, não era esperado** |
| `age` | `TOTAL` | Todas as faixas etárias |
| `sizeclas` | `GE10` | Empresas com 10+ funcionários |
| `nace_r2` | `J` | Information and communication (setor TIC) |
| `unit` | `EUR` / `PPS` / `NAC` | ← **chama "unit", não "currency"** |
| `geo` | código ISO-2 | País |
| `time` | `2022` | Único ano disponível neste dataset |

### URL de teste validada
```
https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/earn_ses22_20?format=JSON&lang=EN&sex=T&age=TOTAL&sizeclas=GE10&nace_r2=J&indic_se=ERN&unit=EUR&geo=PT&geo=DE&geo=LU
```

### Primeiros valores confirmados — salário mensal médio bruto TIC (EUR, 2022)
| País | Salário mensal (€) | Salário anual estimado (€) |
|---|---|---|
| Luxemburgo (LU) | 5.943 | ~71.316 |
| Alemanha (DE) | 5.077 | ~60.924 |
| Portugal (PT) | 2.234 | ~26.808 |

> Gap PT → LU: +166%. Gap PT → DE: +127%. Estes números são o coração do storytelling do projeto.

### Erros encontrados e resolvidos
| Erro | Causa | Solução |
|---|---|---|
| `earn_ses_pub2s` retorna 400 | Dataset renomeado em 2025 | Usar `earn_ses22_20` |
| `INVALID_QUERY_DIMENSION: CURRENCY` | Dimensão não existe neste dataset | Usar `unit=EUR` / `unit=PPS` |

---

## Pendências para as próximas sessões

- [ ] **Terça 26/05:** escrever `fetch_eurostat_salary.py` com todos os ~30 países em EUR e depois em PPS
- [ ] Investigar datasets para série temporal (o SES só tem 2022):
  - `earn_ses2018_*` — edição 2018 do SES
  - `earn_ses2014_*` — edição 2014 do SES
  - `lc_lci_lev` — custo da mão de obra, **anual** (alternativa para o gráfico de tendência)
- [ ] Confirmar quais países EU têm dados disponíveis (alguns podem estar vazios)
- [ ] Testar `unit=PPS` com a mesma URL e verificar se os valores fazem sentido
