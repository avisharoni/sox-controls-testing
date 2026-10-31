"""SYNTHETIC data generators. Nothing here is real company data."""
import numpy as np
import pandas as pd

def synthetic_journal_entries(n=500, seed=0):
    rng = np.random.default_rng(seed)
    start = pd.Timestamp("2025-01-01")
    ts = start + pd.to_timedelta(rng.integers(0, 365 * 24 * 60, n), unit="m")
    amt = np.round(rng.lognormal(7, 1.2, n), 2)
    users = rng.choice(["u01", "u02", "u03", "u04"], n)
    manual = rng.random(n) < 0.2
    return pd.DataFrame({"je_id": range(1, n + 1), "posted_at": ts, "amount": amt,
                         "user": users, "manual": manual, "synthetic": True})
