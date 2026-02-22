from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class DiscountCurve:
    '''
    Discount curve represented by (t, df) nodes, with log-linear interpolation on DF.
    '''
    times: np.ndarray  # shape (n,)
    dfs: np.ndarray    # shape (n,)

    def df(self, t: float) -> float:
        t = float(t)
        if t <= self.times[0]:
            return float(self.dfs[0] ** (t / self.times[0])) if self.times[0] > 0 else 1.0
        if t >= self.times[-1]:
            z = -np.log(self.dfs[-1]) / self.times[-1]
            return float(np.exp(-z * t))

        i = np.searchsorted(self.times, t)
        t0, t1 = self.times[i - 1], self.times[i]
        df0, df1 = self.dfs[i - 1], self.dfs[i]
        w = (t - t0) / (t1 - t0)
        return float(np.exp((1 - w) * np.log(df0) + w * np.log(df1)))

    def zero_rate(self, t: float) -> float:
        t = float(t)
        if t <= 0:
            return 0.0
        return float(-np.log(self.df(t)) / t)
