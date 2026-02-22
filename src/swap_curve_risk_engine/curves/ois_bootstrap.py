from __future__ import annotations

import numpy as np
import pandas as pd

from swap_curve_risk_engine.curves.curve import DiscountCurve
from swap_curve_risk_engine.utils.tenor import tenor_to_years

def bootstrap_usd_sofr_ois(quotes: pd.DataFrame) -> DiscountCurve:
    '''
    Bootstrap a *single* USD SOFR OIS discount curve from:
      - DEPOSIT rows (simple money-market accrual)
      - OIS_SWAP rows on integer-year tenors (1Y..30Y), fixed annual payments

    Assumptions (explicit):
      - ACT/360 for deposits (tau = tenor_to_years)
      - OIS swap fixed leg pays annually with accrual alpha = 365/360 (approx).
      - Log-linear interpolation on DF between nodes is used by the curve object.
    '''
    df = quotes.copy()

    required = {"instrument_type", "tenor", "quote"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"quotes missing required columns: {sorted(missing)}")

    df["tenor"] = df["tenor"].astype(str).str.upper().str.strip()
    df["instrument_type"] = df["instrument_type"].astype(str).str.upper().str.strip()
    df["quote"] = df["quote"].astype(float)

    dep = df[df["instrument_type"] == "DEPOSIT"].copy()
    dep["t"] = dep["tenor"].map(tenor_to_years)
    dep = dep.sort_values("t")

    times = []
    dfs = []
    for _, r in dep.iterrows():
        t = float(r["t"])
        rate = float(r["quote"])
        if t <= 0:
            continue
        df_t = 1.0 / (1.0 + rate * t)
        times.append(t)
        dfs.append(df_t)

    swp = df[df["instrument_type"] == "OIS_SWAP"].copy()
    swp["t"] = swp["tenor"].map(tenor_to_years)
    swp = swp.sort_values("t")

    alpha = 365.0 / 360.0  # approx ACT/360 for 1Y period

    node = {float(t): float(dfv) for t, dfv in zip(times, dfs)}

    for _, r in swp.iterrows():
        T = float(r["t"])
        par = float(r["quote"])

        if abs(T - round(T)) > 1e-9:
            raise ValueError(
                f"OIS_SWAP tenors must be integer years for this bootstrap. Got tenor={r['tenor']!r} (T={T})."
            )
        n = int(round(T))

        sum_prev = 0.0
        for k in range(1, n):
            tk = float(k)
            if tk not in node:
                raise ValueError(f"Missing DF for {tk}Y required to bootstrap {n}Y")
            sum_prev += node[tk] * alpha

        df_T = (1.0 - par * sum_prev) / (1.0 + par * alpha)
        if df_T <= 0 or df_T >= 1.0:
            raise ValueError(f"Bootstrapped invalid DF at {n}Y: {df_T}")
        node[float(n)] = float(df_T)

    final_times = sorted(node.keys())
    final_dfs = [node[t] for t in final_times]

    return DiscountCurve(times=np.array(final_times, dtype=float), dfs=np.array(final_dfs, dtype=float))

def curve_nodes_table(curve: DiscountCurve) -> pd.DataFrame:
    return pd.DataFrame({
        "t_years": curve.times,
        "df": curve.dfs,
        "zero_rate_cc": [-np.log(df)/t for t, df in zip(curve.times, curve.dfs)],
    })
