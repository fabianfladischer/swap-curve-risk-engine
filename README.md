# Swap Curve Risk Engine (USD/SOFR)

A reusable Python rates analytics module for **USD SOFR curve construction**, **vanilla swap valuation**, and **DV01/BP01-style sensitivity reporting**.

> Portfolio project: clean architecture, no vendor lock-in, and an I/O layer that can be mapped to Bloomberg exports.

## Quickstart (runs end-to-end on mock data)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

swap-risk --market data/market/usd_sofr_ois_market_quotes.csv          --portfolio data/portfolio/usd_swap_portfolio.csv          --scenarios data/scenarios.csv          --out outputs
```

Outputs:
- `outputs/curve_nodes.csv`
- `outputs/portfolio_risk.csv`
- `outputs/portfolio_cashflows.csv`
- `outputs/scenario_matrix.csv`

## Notes
Educational/portfolio project (not investment advice).
