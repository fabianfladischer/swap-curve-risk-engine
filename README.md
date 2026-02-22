# Swap Curve Risk Engine (USD / SOFR)

A production-style Python project for **USD SOFR curve construction**, **vanilla interest rate swap valuation**, and **DV01/BP01 risk reporting**.

This repository is built to be **reproducible**, **testable**, and **vendor-agnostic** (easy to map Bloomberg exports into the canonical CSV schema).

---

## What this project does

- **Bootstraps a USD SOFR OIS discount curve** from short-end money-market quotes + OIS par swap rates  
- **Prices fixed-vs-float vanilla swaps** using discount factors and implied forwards  
- Computes **DV01 (parallel 1bp bump-and-reprice)** per trade and for the portfolio  
- Runs **simple scenario shocks** (parallel / steepener / flattener) and outputs reporting tables as CSV

---

## Repository layout

```text
.
├─ src/                       # engine (curves, products, risk, io)
├─ data/                      # canonical mock data (market quotes + portfolio + scenarios)
├─ scripts/                   # demo entrypoints
├─ tests/                     # pytest unit tests
└─ outputs/                   # generated reports (local)
```

## Quickstart (runs end-to-end on mock data)
```bash
python -m venv .venv && source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"

swap-risk \
  --market data/market/usd_sofr_ois_market_quotes.csv \
  --portfolio data/portfolio/usd_swap_portfolio.csv \
  --scenarios data/scenarios.csv \
  --out outputs
```

### Generated Outputs:
- `outputs/curve_nodes.csv` - curve nodes (t, DF, continuous-compounded zero rate)
- `outputs/portfolio_risk.csv` - PV and DV01 per trade
- `outputs/portfolio_cashflows.csv` - detailed cashflow table per trade
- `outputs/scenario_matrix.csv` - portfolio PV under each scenario + ΔPV vs base

## Data
This repo uses a canonical CSV format so you can later swap mock data for real exports (e.g., Bloomberg) with a simple mapping/rename step.

`data/market/usd_sofr_ois_market_quotes.csv`
Short-end deposits + annual SOFR OIS swap par rates (1Y..30Y)
`data/portfolio/usd_swap_portfolio.csv`
Example cleared USD SOFR swaps (PAY/RECEIVE, notionals, fixed rates, maturities)
`data/scenarios.csv`
Scenario shocks (parallel ±bp and bucketed steepener/flattening)
See: `data/README.md` for column-level details.

## Disclaimer
Educational/portfolio project (not investment advice).
