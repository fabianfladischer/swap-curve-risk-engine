from __future__ import annotations

from dataclasses import dataclass
import numpy as np
import pandas as pd

from swap_curve_risk_engine.curves.curve import DiscountCurve

_FREQ_TO_YEARS = {
    "1M": 1/12,
    "3M": 0.25,
    "6M": 0.5,
    "1Y": 1.0,
}

def _freq_to_years(freq: str) -> float:
    f = freq.strip().upper()
    if f not in _FREQ_TO_YEARS:
        raise ValueError(f"Unsupported freq: {freq!r}")
    return float(_FREQ_TO_YEARS[f])

@dataclass(frozen=True)
class VanillaSwap:
    trade_id: str
    pay_receive_fixed: str  # PAY or RECEIVE
    notional: float
    fixed_rate: float
    maturity_years: float
    fixed_freq: str = "6M"
    float_freq: str = "3M"
    float_spread_bps: float = 0.0

    def sign(self) -> float:
        d = self.pay_receive_fixed.strip().upper()
        if d == "RECEIVE":
            return 1.0
        if d == "PAY":
            return -1.0
        raise ValueError(f"pay_receive_fixed must be PAY or RECEIVE, got {self.pay_receive_fixed!r}")

def _schedule_times(T: float, step: float) -> np.ndarray:
    n = int(np.round(T / step))
    times = np.array([step * i for i in range(1, n + 1)], dtype=float)
    if abs(times[-1] - T) > 1e-9:
        times[-1] = T
    return times

def price_swap(curve: DiscountCurve, swap: VanillaSwap) -> tuple[float, pd.DataFrame]:
    '''
    Price a fixed-vs-float vanilla swap under a single discount curve.
    Floating leg forwards are derived from DF ratios.
    '''
    sgn = swap.sign()
    N = float(swap.notional)
    T = float(swap.maturity_years)

    fixed_step = _freq_to_years(swap.fixed_freq)
    fixed_times = _schedule_times(T, fixed_step)
    alpha_f = fixed_step

    fixed_rows = []
    pv_fixed = 0.0
    for t in fixed_times:
        cf = N * swap.fixed_rate * alpha_f
        df = curve.df(t)
        pv = df * cf
        pv_fixed += pv
        fixed_rows.append((t, "FIXED", cf, df, pv))

    float_step = _freq_to_years(swap.float_freq)
    float_times = _schedule_times(T, float_step)
    alpha_fl = float_step
    spread = float(swap.float_spread_bps) * 1e-4

    float_rows = []
    pv_float = 0.0
    t_prev = 0.0
    for t in float_times:
        df_prev = curve.df(t_prev) if t_prev > 0 else 1.0
        df_t = curve.df(t)
        fwd = (df_prev / df_t - 1.0) / alpha_fl
        rate = fwd + spread
        cf = N * rate * alpha_fl
        pv = df_t * cf
        pv_float += pv
        float_rows.append((t, "FLOAT", cf, df_t, pv))
        t_prev = t

    pv = sgn * (pv_fixed - pv_float)

    cft = pd.DataFrame(fixed_rows + float_rows, columns=["t_years", "leg", "cashflow", "df", "pv"])            .sort_values(["t_years", "leg"]).reset_index(drop=True)
    cft.insert(0, "trade_id", swap.trade_id)
    return pv, cft

def swap_from_portfolio_row(row: dict) -> VanillaSwap:
    eff = pd.Timestamp(row["effective_date"])
    mat = pd.Timestamp(row["maturity_date"])
    T = (mat - eff).days / 360.0

    return VanillaSwap(
        trade_id=str(row["trade_id"]),
        pay_receive_fixed=str(row["pay_receive_fixed"]),
        notional=float(row["notional"]),
        fixed_rate=float(row["fixed_rate"]),
        maturity_years=float(T),
        fixed_freq=str(row.get("fixed_leg_freq", "6M")),
        float_freq=str(row.get("float_leg_freq", "3M")),
        float_spread_bps=float(row.get("float_spread_bps", 0.0)),
    )
