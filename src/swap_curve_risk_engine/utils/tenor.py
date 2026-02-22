from __future__ import annotations
import re

_TENOR_RE = re.compile(r"^(?P<n>\d+)(?P<u>[DWMY])$")

def tenor_to_years(tenor: str) -> float:
    '''
    Convert a tenor string to an ACT/360-style year fraction approximation.

    Supported:
    - ON (overnight) -> 1 day
    - nD, nW, nM, nY
    '''
    t = tenor.strip().upper()
    if t == "ON":
        return 1.0 / 360.0

    m = _TENOR_RE.match(t)
    if not m:
        raise ValueError(f"Unsupported tenor: {tenor!r}")

    n = int(m.group("n"))
    u = m.group("u")

    if u == "D":
        return n / 360.0
    if u == "W":
        return (7 * n) / 360.0
    if u == "M":
        return n / 12.0  # approx; 1Y = 12M
    if u == "Y":
        return float(n)

    raise ValueError(f"Unsupported tenor unit: {u!r}")
