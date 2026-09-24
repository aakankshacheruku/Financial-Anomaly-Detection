# Transaction Anomaly Summary

Reviewed **12,000** transactions. **264** (2.2%) were flagged as unusual by at least one detection method; **152** were flagged by both methods, which is the strongest signal of a real irregularity.

## Where the flags are concentrated

- **food**: 44 flagged transaction(s)
- **entertainment**: 41 flagged transaction(s)
- **other**: 41 flagged transaction(s)
- **retail**: 36 flagged transaction(s)
- **gas**: 35 flagged transaction(s)
- **utilities**: 35 flagged transaction(s)
- **travel**: 32 flagged transaction(s)

## Highest-value flagged transactions

| Transaction | Category | Amount | Flagged by |
|---|---|---|---|
| a101 | travel | $10,551.15 | z-score, IQR |
| a153 | travel | $10,218.44 | z-score, IQR |
| a21 | travel | $10,132.48 | z-score, IQR |
| a235 | travel | $9,736.77 | z-score, IQR |
| a28 | travel | $7,852.04 | z-score, IQR |

## What this means

Transactions flagged by both methods are the highest-confidence candidates for review, they're unusual relative to their own category's typical spending, not just unusual in the dataset overall. Single-method flags are worth a lighter second look, since z-score and IQR occasionally disagree on borderline cases.