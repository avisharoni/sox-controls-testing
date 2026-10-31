import pandas as pd
from soxct.sampling import attribute_sample_size, select_sample, evaluate
from soxct.je_anomaly import flag_entries, benford_mad, first_digit
from soxct.sod import sod_conflicts

def test_sample_size_matches_audit_tables():
    assert attribute_sample_size(0.95, 0.05, 0) == 59   # standard AICPA table value
    assert attribute_sample_size(0.90, 0.10, 0) == 22

def test_selection_reproducible():
    assert select_sample(range(100), 5, 3) == select_sample(range(100), 5, 3)

def test_evaluate():
    assert evaluate(59, 0)["effective"]
    assert not evaluate(59, 3)["effective"]

def test_flags():
    je = pd.DataFrame({"je_id": [1, 2], "posted_at": ["2025-03-08 23:00", "2025-03-05 10:00"],
                       "amount": [9800.0, 1234.5], "user": ["x", "u01"], "manual": [True, False]})
    out = flag_entries(je, usual_users={"u01"}).set_index("je_id")
    assert out.loc[1, "risk_score"] == 4 and out.loc[2, "risk_score"] == 0

def test_benford():
    assert first_digit(0.0042) == 4
    import math
    perfect = [d for d in range(1, 10) for _ in range(round(1000 * math.log10(1 + 1/d)))]
    assert benford_mad(perfect) < 0.002

def test_sod():
    c = sod_conflicts({"a": ["create_vendor", "approve_payment"], "b": ["create_vendor"]})
    assert c == [("a", "create_vendor", "approve_payment")]
