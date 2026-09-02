"""
Generate a realistic synthetic transaction dataset for anomaly detection.

Simulates 12,000 member transactions across common spending categories,
each with its own typical amount range, plus a small injected set of
true anomalies (unusually large or unusually frequent transactions)
so detection methods have something real to find.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

RNG = np.random.default_rng(seed=42)

CATEGORIES = {
    "food": (8, 45),
    "gas": (20, 90),
    "retail": (10, 200),
    "utilities": (40, 220),
    "entertainment": (10, 120),
    "travel": (50, 900),
    "other": (5, 150),
}

N_TRANSACTIONS = 12000
N_ANOMALIES = 240  # ~2% of transactions, injected as true outliers
START_DATE = datetime(2025, 1, 1)
DAYS_RANGE = 300


def generate_normal_transactions(n):
    rows = []
    categories = list(CATEGORIES.keys())
    weights = [0.28, 0.15, 0.20, 0.10, 0.12, 0.05, 0.10]

    for i in range(n):
        cat = RNG.choice(categories, p=weights)
        low, high = CATEGORIES[cat]
        # log-normal-ish spread so most amounts cluster low with a long right tail,
        # which mirrors real transaction data better than a uniform draw
        mean = (low + high) / 2
        sigma = (high - low) / 4
        amount = float(np.clip(RNG.normal(mean, sigma), low * 0.5, high * 1.5))
        day_offset = int(RNG.integers(0, DAYS_RANGE))
        date = START_DATE + timedelta(days=day_offset)
        rows.append({
            "txn_id": f"t{i+1}",
            "date": date.strftime("%Y-%m-%d"),
            "category": cat,
            "amount": round(amount, 2),
        })
    return rows


def generate_anomalies(n):
    rows = []
    categories = list(CATEGORIES.keys())
    for i in range(n):
        cat = RNG.choice(categories)
        low, high = CATEGORIES[cat]
        # anomalies: either a spike far above normal range, or a suspicious
        # near-round large amount (common fraud/structuring pattern)
        if RNG.random() < 0.5:
            amount = round(high * RNG.uniform(4, 12), 2)
        else:
            amount = round(RNG.choice([500, 750, 1000, 1500, 2000, 5000]) + RNG.uniform(-5, 5), 2)
        day_offset = int(RNG.integers(0, DAYS_RANGE))
        date = START_DATE + timedelta(days=day_offset)
        rows.append({
            "txn_id": f"a{i+1}",
            "date": date.strftime("%Y-%m-%d"),
            "category": cat,
            "amount": amount,
        })
    return rows


def main():
    normal = generate_normal_transactions(N_TRANSACTIONS - N_ANOMALIES)
    anomalies = generate_anomalies(N_ANOMALIES)
    df = pd.DataFrame(normal + anomalies)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)  # shuffle
    df.to_csv("data/sample/transactions.csv", index=False)
    print(f"Wrote {len(df)} transactions to data/sample/transactions.csv")
    print(f"  Normal: {len(normal)} | Injected anomalies: {len(anomalies)}")


if __name__ == "__main__":
    main()
