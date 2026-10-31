import math, random

def attribute_sample_size(confidence=0.95, tolerable_rate=0.05, expected_deviations=0):
    """Smallest n such that P(X<=k | n, tolerable_rate) <= 1-confidence (binomial)."""
    alpha = 1 - confidence
    n = expected_deviations + 1
    while True:
        p = sum(math.comb(n, i) * tolerable_rate**i * (1 - tolerable_rate)**(n - i)
                for i in range(expected_deviations + 1))
        if p <= alpha:
            return n
        n += 1

def select_sample(population_ids, n, seed=0):
    ids = list(population_ids)
    if n > len(ids):
        raise ValueError("sample larger than population")
    return sorted(random.Random(seed).sample(ids, n))

def upper_deviation_limit(n, deviations, confidence=0.95, tol=1e-6):
    """Binomial upper bound on the population deviation rate (bisection)."""
    alpha = 1 - confidence
    lo, hi = 0.0, 1.0
    while hi - lo > tol:
        mid = (lo + hi) / 2
        p = sum(math.comb(n, i) * mid**i * (1 - mid)**(n - i) for i in range(deviations + 1))
        lo, hi = (mid, hi) if p > alpha else (lo, mid)
    return hi

def evaluate(n, deviations, tolerable_rate=0.05, confidence=0.95):
    udl = upper_deviation_limit(n, deviations, confidence)
    return {"sample_rate": deviations / n, "upper_limit": udl, "effective": udl <= tolerable_rate}
