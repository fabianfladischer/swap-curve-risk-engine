from __future__ import annotations
import pandas as pd

def load_market_quotes(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    for c in ["tenor", "instrument_type", "curve"]:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip()
    return df

def load_portfolio(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def load_scenarios(path: str) -> pd.DataFrame:
    return pd.read_csv(path)
