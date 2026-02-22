from swap_curve_risk_engine.cli import main

if __name__ == "__main__":
    raise SystemExit(
        main([
            "--market", "data/market/usd_sofr_ois_market_quotes.csv",
            "--portfolio", "data/portfolio/usd_swap_portfolio.csv",
            "--scenarios", "data/scenarios.csv",
            "--out", "outputs",
        ])
    )
