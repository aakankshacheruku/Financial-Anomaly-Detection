# Financial Anomaly Detection

Flags unusual transactions in a 12,000-row synthetic transaction dataset using two
complementary statistical methods, then turns the results into a plain-language
summary a non-technical reader could act on, not just a table of z-scores.

## Why two detection methods
A single global z-score treats a $900 travel charge and a $900 food charge as
equally unusual, which they aren't. Both methods here are computed **within
category** instead of globally:

- **Z-score**: flags transactions more than `k` standard deviations from their
  category mean. Simple and fast, but sensitive to the outliers themselves
  inflating the standard deviation.
- **IQR (interquartile range)**: flags transactions outside
  `Q1 - 1.5*IQR` / `Q3 + 1.5*IQR`. More robust to skewed distributions, which
  matters here since transaction amounts are naturally right-skewed.

Transactions flagged by **both** methods are the highest-confidence anomalies.

## Quickstart
```bash
python3 -m venv .venv && source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

python src/generate_data.py   # generates data/sample/transactions.csv
make quickstart                # runs detection, writes reports
make test                      # runs the test suite
```

## Results (current dataset)
- 12,000 transactions reviewed, ~240 true anomalies injected during generation
- 264 transactions flagged by at least one method (2.2%)
- 152 flagged by both methods (highest-confidence anomalies)
- Travel had the highest flag rate by category; food had the lowest

See `reports/anomaly_summary.md` for the full plain-language writeup and
`reports/figures/` for the visualizations.

## Project structure
```
src/
  generate_data.py   # builds the synthetic transaction dataset
  detect.py           # z-score and IQR detection, computed per category
  report.py           # turns flagged output into a plain-language summary
scripts/
  run.py               # runs the full pipeline end to end
tests/
  test_detect.py       # unit tests for both detection methods
reports/
  tables/               # full and flagged-only CSVs
  figures/              # amounts-over-time and flag-rate-by-category charts
  anomaly_summary.md    # plain-language summary of findings
```

## What I learned building this
- A global baseline understates risk in low-spend categories and overstates it
  in naturally high-spend ones — category-level baselines fixed that.
- Z-score and IQR occasionally disagree at the margins, which is itself a
  useful signal: agreement between methods is a stronger confidence marker
  than either method alone.
- Writing the plain-language summary directly from the flagged data (rather
  than as an afterthought) forced the detection logic to produce genuinely
  interpretable output, not just a numeric flag column.

## Next steps
- Rolling time-window baselines, to catch a sudden change in a single
  member's spending pattern rather than only category-wide outliers.
- Compare against a simple isolation forest as a third method.
- Expand categories and inject more realistic fraud patterns (e.g.
  structuring: several transactions just under a reporting threshold).
