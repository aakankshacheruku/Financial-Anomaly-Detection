"""
Anomaly detection methods for transaction data.

Two methods are implemented, both computed *within category* rather than
globally — a $900 travel charge and a $900 food charge are not equally
unusual, so a single global baseline understates risk in low-spend
categories and overstates it in naturally high-spend ones.

- Z-score: flags transactions more than `z_thresh` standard deviations
  from their category mean. Simple, but sensitive to the outliers
  themselves inflating the standard deviation.
- IQR (interquartile range): flags transactions outside
  Q1 - k*IQR / Q3 + k*IQR. More robust to skewed distributions and to
  the anomalies themselves distorting the baseline, which matters here
  since transaction amounts are right-skewed by nature.
"""

import pandas as pd


def flag_zscore(df: pd.DataFrame, z_thresh: float = 3.0) -> pd.DataFrame:
    out = df.copy()
    stats = out.groupby("category")["amount"].agg(
        cat_mean="mean",
        cat_std=lambda s: s.std(ddof=0),
    )
    out = out.merge(stats, on="category", how="left")
    out["cat_std"] = out["cat_std"].replace(0, 1.0).fillna(1.0)
    out["zscore"] = (out["amount"] - out["cat_mean"]) / out["cat_std"]
    out["flag_zscore"] = out["zscore"].abs() >= z_thresh
    return out


def flag_iqr(df: pd.DataFrame, k: float = 1.5) -> pd.DataFrame:
    out = df.copy()
    q1 = out.groupby("category")["amount"].transform(lambda s: s.quantile(0.25))
    q3 = out.groupby("category")["amount"].transform(lambda s: s.quantile(0.75))
    iqr = q3 - q1
    out["iqr_lower"] = q1 - k * iqr
    out["iqr_upper"] = q3 + k * iqr
    out["flag_iqr"] = (out["amount"] < out["iqr_lower"]) | (out["amount"] > out["iqr_upper"])
    return out


def combined_flags(df: pd.DataFrame, z_thresh: float = 3.0, k: float = 1.5) -> pd.DataFrame:
    out = flag_zscore(df, z_thresh)
    out = flag_iqr(out, k)
    out["flag_any"] = out["flag_zscore"] | out["flag_iqr"]
    out["flag_both"] = out["flag_zscore"] & out["flag_iqr"]
    return out
