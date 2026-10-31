import math
import numpy as np
import pandas as pd

BENFORD = {d: math.log10(1 + 1 / d) for d in range(1, 10)}

def first_digit(x):
    x = abs(float(x))
    if x == 0:
        return 0
    return int(f"{x:e}"[0])

def benford_mad(amounts):
    d = pd.Series([first_digit(a) for a in amounts])
    d = d[d > 0]
    obs = d.value_counts(normalize=True).reindex(range(1, 10), fill_value=0)
    return float(np.mean([abs(obs[k] - BENFORD[k]) for k in range(1, 10)]))

def flag_entries(je, approval_threshold=10000, near_pct=0.05, business_hours=(7, 19), usual_users=None):
    df = je.copy()
    ts = pd.to_datetime(df["posted_at"])
    df["f_weekend"] = ts.dt.dayofweek >= 5
    df["f_after_hours"] = (ts.dt.hour < business_hours[0]) | (ts.dt.hour >= business_hours[1])
    df["f_round"] = (df["amount"].abs() >= 1000) & (df["amount"].abs() % 1000 == 0)
    a = df["amount"].abs()
    df["f_near_threshold"] = (a < approval_threshold) & (a >= approval_threshold * (1 - near_pct))
    if usual_users is not None:
        df["f_unusual_user"] = df["manual"] & ~df["user"].isin(usual_users)
    else:
        df["f_unusual_user"] = False
    flags = [c for c in df.columns if c.startswith("f_")]
    df["risk_score"] = df[flags].sum(axis=1)
    return df.sort_values("risk_score", ascending=False)
