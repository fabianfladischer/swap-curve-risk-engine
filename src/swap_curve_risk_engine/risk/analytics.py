from __future__ import annotations

import pandas as pd

from swap_curve_risk_engine.curves.ois_bootstrap import bootstrap_usd_sofr_ois
from swap_curve_risk_engine.products.swap import price_swap, swap_from_portfolio_row
from swap_curve_risk_engine.utils.tenor import tenor_to_years

BP = 1e-4

def bump_quotes_parallel(quotes: pd.DataFrame, bump_bp: float) -> pd.DataFrame:
    bumped = quotes.copy()
    bumped["quote"] = bumped["quote"].astype(float) + (bump_bp * BP)
    return bumped

def apply_scenario(quotes: pd.DataFrame, scenario: dict) -> pd.DataFrame:
    q = quotes.copy()
    q["quote"] = q["quote"].astype(float)

    par = float(scenario.get("parallel_bp", 0.0))
    se  = float(scenario.get("short_end_bp", 0.0))
    le  = float(scenario.get("long_end_bp", 0.0))

    t = q["tenor"].astype(str).str.upper().str.strip().map(tenor_to_years)

    bump = pd.Series([par]*len(q), index=q.index, dtype=float)
    bump = bump + se * (t <= 2.0) + le * (t >= 10.0)

    q["quote"] = q["quote"] + bump * BP
    return q

def portfolio_risk(quotes: pd.DataFrame, portfolio: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    curve = bootstrap_usd_sofr_ois(quotes)

    rows = []
    cfs = []
    for _, r in portfolio.iterrows():
        sw = swap_from_portfolio_row(r.to_dict())
        pv, cf = price_swap(curve, sw)
        rows.append({"trade_id": sw.trade_id, "pv": pv})
        cfs.append(cf)

    base = pd.DataFrame(rows).sort_values("trade_id").reset_index(drop=True)
    cashflows = pd.concat(cfs, ignore_index=True) if cfs else pd.DataFrame()

    curve_up = bootstrap_usd_sofr_ois(bump_quotes_parallel(quotes, bump_bp=1.0))
    dv01_rows = []
    for _, r in portfolio.iterrows():
        sw = swap_from_portfolio_row(r.to_dict())
        pv_up, _ = price_swap(curve_up, sw)
        pv0 = float(base.loc[base["trade_id"] == sw.trade_id, "pv"].iloc[0])
        dv01_rows.append({"trade_id": sw.trade_id, "dv01_parallel_1bp": pv_up - pv0})

    dv01 = pd.DataFrame(dv01_rows).sort_values("trade_id").reset_index(drop=True)
    risk = base.merge(dv01, on="trade_id", how="left")
    return risk, cashflows

def scenario_matrix(quotes: pd.DataFrame, portfolio: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    base_risk, _ = portfolio_risk(quotes, portfolio)
    base_pv = float(base_risk["pv"].sum())

    out = []
    for _, s in scenarios.iterrows():
        scen_name = str(s["scenario"])
        if scen_name.upper() == "BASE":
            out.append({"scenario": scen_name, "portfolio_pv": base_pv, "delta_pv": 0.0})
            continue
        q_s = apply_scenario(quotes, s.to_dict())
        risk_s, _ = portfolio_risk(q_s, portfolio)
        pv_s = float(risk_s["pv"].sum())
        out.append({"scenario": scen_name, "portfolio_pv": pv_s, "delta_pv": pv_s - base_pv})

    return pd.DataFrame(out)
