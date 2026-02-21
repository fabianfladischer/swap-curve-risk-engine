# Swap Curve Risk Engine

A reusable Python rates analytics module for curve construction, swap valuation, and DV01/BP01-style sensitivity reporting. Built as a clean portfolio project (no vendor lock-in).

## What this project does
- Builds a simple curve layer (discount/forward curve objects)
- Prices vanilla interest rate swaps (par rate, PV, cashflows)
- Computes DV01/BP01 via bump-and-reprice
- Runs scenario shocks (parallel / steepener / flattener) for decision-ready risk views

## Outputs (planned)
- Curve and par-rate tables across maturities
- PV and DV01/BP01 tables per trade or portfolio
- Scenario matrix (PV / DV01 changes under shocks)
- Basic plots for curve shape and sensitivity distribution

## Repository structure
- `notebooks/` — example notebooks and demos (coming soon)
- `src/` — reusable functions/modules (coming soon)
- `docs/` — one-pager and documentation

## One-pager
See: `docs/one_pager.pdf` (or the uploaded PDF in `docs/`).

## Notes
Educational/portfolio project (not investment advice).
