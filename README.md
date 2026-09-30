# Financial Anomaly Detection

**Result:** Out of 12,000 transactions, two statistical methods flagged 264 as unusual, and 152 were flagged by both. Those 152 are the short list a reviewer should check first!

<!-- Drag a chart from reports/figures/ here, then delete this line. -->

## The Problem

A reviewer can't check thousands of transactions by hand, and a simple rule like "anything over $500" misses what is actually unusual. A $900 travel charge is normal, while a $900 food charge is not. This project finds the transactions that are unusual for their own category and explains the results in plain language so a non-technical reader can act on them.

## How It Works

- Every transaction is compared against others in the same category rather than the whole dataset.
- The z-score method flags amounts more than `k` standard deviations from the category mean. It is simple and fast, but the outliers themselves can inflate the standard deviation.
- The IQR method flags amounts outside `Q1 - 1.5*IQR` and `Q3 + 1.5*IQR`. It holds up better on skewed data, which matters because transaction amounts are naturally right-skewed.
- Transactions flagged by both methods are treated as the highest-confidence anomalies.
- The pipeline writes a plain-language summary directly from the flagged data, not just a column of scores.

## Results

| measure | value |
|---|---|
| Transactions reviewed | 12,000 |
| True anomalies injected during generation | About 240 |
| Flagged by at least one method | 264 (2.2%) |
| Flagged by both methods | 152 |
| Highest flag rate by category | Travel |
| Lowest flag rate by category | Food |

The full writeup is in [`reports/anomaly_summary.md`](reports/anomaly_summary.md), and the charts are in [`reports/figures/`](reports/figures/).

## What I Learned

- A single global baseline understates risk in low-spend categories and overstates it in high-spend ones, so category-level baselines fixed that.
- When the two methods disagree at the margins, that disagreement is useful, because agreement is a stronger signal than either method alone.
- Writing the plain-language summary from the start pushed the detection logic to produce output people can actually interpret.

## Next Steps

- I'd add rolling time-window baselines to catch sudden changes in one account's spending, not only category-wide outliers.
- I'd compare the results against an isolation forest as a third method.
- I'd inject more realistic fraud patterns, such as several transactions just under a reporting threshold.

## Tools

| category | tools |
|---|---|
| Programming | Python and pandas. |
| Testing and Automation | pytest and Make. |

## Run It Yourself

```bash
python3 -m venv .venv && source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

python src/generate_data.py   # generates data/sample/transactions.csv
make quickstart               # runs detection, writes reports
make test                     # runs the test suite
```

<details>
<summary>Project Structure</summary>
