import os
import sys

import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.detect import combined_flags
from src.report import build_summary

os.makedirs("reports/tables", exist_ok=True)
os.makedirs("reports/figures", exist_ok=True)

df = pd.read_csv("data/sample/transactions.csv")
result = combined_flags(df)

result.to_csv("reports/tables/anomalies_full.csv", index=False)
result[result["flag_any"]].to_csv("reports/tables/anomalies_flagged.csv", index=False)

summary = build_summary(result)
with open("reports/anomaly_summary.md", "w") as f:
    f.write(summary)

# Histogram of amounts by category, flagged transactions highlighted
result_sorted = result.sort_values("date")
fig, ax = plt.subplots(figsize=(9, 5))
for cat in result_sorted["category"].unique():
    subset = result_sorted[result_sorted["category"] == cat]
    ax.scatter(
        subset["date"], subset["amount"],
        s=10, alpha=0.3, label=None,
    )
flagged = result_sorted[result_sorted["flag_any"]]
ax.scatter(flagged["date"], flagged["amount"], s=25, color="red", label="Flagged")
ax.set_xticks(ax.get_xticks()[::30])
plt.xticks(rotation=45, ha="right")
ax.set_title("Transaction amounts over time (flagged in red)")
ax.set_xlabel("date")
ax.set_ylabel("amount ($)")
ax.legend()
plt.tight_layout()
plt.savefig("reports/figures/amounts_over_time.png", dpi=160)

# Category flag-rate bar chart
flag_rate = result.groupby("category")["flag_any"].mean().sort_values(ascending=False) * 100
fig2, ax2 = plt.subplots(figsize=(7, 4))
flag_rate.plot(kind="bar", ax=ax2, color="#4C72B0")
ax2.set_title("Flag rate by category (%)")
ax2.set_ylabel("% of transactions flagged")
plt.tight_layout()
plt.savefig("reports/figures/flag_rate_by_category.png", dpi=160)

print(f"Reviewed {len(result):,} transactions")
print(f"Flagged (either method): {result['flag_any'].sum():,}")
print(f"Flagged (both methods): {result['flag_both'].sum():,}")
print("Wrote reports/tables/anomalies_full.csv, anomalies_flagged.csv,")
print("  reports/anomaly_summary.md, and two figures in reports/figures/")
