from __future__ import annotations

import argparse
from pathlib import Path

from swap_curve_risk_engine.io.loaders import load_market_quotes, load_portfolio, load_scenarios
from swap_curve_risk_engine.curves.ois_bootstrap import bootstrap_usd_sofr_ois, curve_nodes_table
from swap_curve_risk_engine.risk.analytics import portfolio_risk, scenario_matrix

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="swap-risk", description="Swap Curve Risk Engine demo (USD/SOFR).")
    p.add_argument("--market", required=True, help="Market quotes CSV (canonical schema)")
    p.add_argument("--portfolio", required=True, help="Portfolio swaps CSV (canonical schema)")
    p.add_argument("--scenarios", required=False, help="Scenarios CSV", default=None)
    p.add_argument("--out", required=True, help="Output directory")

    args = p.parse_args(argv)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    quotes = load_market_quotes(args.market)
    portfolio = load_portfolio(args.portfolio)

    curve = bootstrap_usd_sofr_ois(quotes)
    curve_nodes_table(curve).to_csv(out / "curve_nodes.csv", index=False)

    risk, cashflows = portfolio_risk(quotes, portfolio)
    risk.to_csv(out / "portfolio_risk.csv", index=False)
    cashflows.to_csv(out / "portfolio_cashflows.csv", index=False)

    if args.scenarios:
        scen = load_scenarios(args.scenarios)
        scenario_matrix(quotes, portfolio, scen).to_csv(out / "scenario_matrix.csv", index=False)

    print(f"Wrote outputs to: {out.resolve()}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
