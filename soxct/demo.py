from .sampling import attribute_sample_size, select_sample, evaluate
from .je_anomaly import flag_entries, benford_mad
from .sod import sod_conflicts
from .synthetic import synthetic_journal_entries

if __name__ == "__main__":
    n = attribute_sample_size(0.95, 0.05, 0)
    print("Sample size (95% conf, 5% tolerable, 0 expected):", n)
    print("Selected IDs:", select_sample(range(1, 2001), 5, seed=1), "...")
    print("Evaluation with 1 deviation:", evaluate(n, 1))
    je = synthetic_journal_entries()
    print("Benford MAD (synthetic JE):", round(benford_mad(je["amount"]), 4))
    print(flag_entries(je, usual_users={"u01", "u02"}).head(5)[["je_id", "amount", "risk_score"]])
    print(sod_conflicts({"alice": ["create_vendor", "approve_payment"], "bob": ["create_po"]}))
