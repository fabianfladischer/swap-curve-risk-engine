from swap_curve_risk_engine.io.loaders import load_market_quotes, load_portfolio
from swap_curve_risk_engine.curves.ois_bootstrap import bootstrap_usd_sofr_ois
from swap_curve_risk_engine.risk.analytics import portfolio_risk

def test_bootstrap_monotone_df():
    q = load_market_quotes("data/market/usd_sofr_ois_market_quotes.csv")
    curve = bootstrap_usd_sofr_ois(q)
    assert all(curve.dfs[i] > curve.dfs[i+1] for i in range(len(curve.dfs)-1))

def test_portfolio_risk_runs():
    q = load_market_quotes("data/market/usd_sofr_ois_market_quotes.csv")
    p = load_portfolio("data/portfolio/usd_swap_portfolio.csv")
    risk, cfs = portfolio_risk(q, p)
    assert len(risk) == len(p)
    assert {"trade_id","pv","dv01_parallel_1bp"} <= set(risk.columns)
    assert len(cfs) > 0
