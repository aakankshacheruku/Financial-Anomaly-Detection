"""
Turn flagged anomaly output into a short plain-language summary,
the kind that would actually go to a non-technical stakeholder
rather than a raw table of z-scores.
"""

import pandas as pd


def build_summary(df: pd.DataFrame) -> str:
    total = len(df)
    flagged = df[df["flag_any"]]
    both = df[df["flag_both"]]
    pct_flagged = 100 * len(flagged) / total if total else 0

    by_category = (
        flagged.groupby("category")
        .size()
        .sort_values(ascending=False)
    )

    top_flagged = flagged.sort_values("amount", ascending=False).head(5)

    lines = []
    lines.append("# Transaction Anomaly Summary\n")
    lines.append(f"Reviewed **{total:,}** transactions. "
                  f"**{len(flagged):,}** ({pct_flagged:.1f}%) were flagged as unusual "
                  f"by at least one detection method; **{len(both):,}** were flagged by "
                  f"both methods, which is the strongest signal of a real irregularity.\n")

    lines.append("## Where the flags are concentrated\n")
    for cat, count in by_category.items():
        lines.append(f"- **{cat}**: {count} flagged transaction(s)")
    lines.append("")

    lines.append("## Highest-value flagged transactions\n")
    lines.append("| Transaction | Category | Amount | Flagged by |")
    lines.append("|---|---|---|---|")
    for _, row in top_flagged.iterrows():
        methods = []
        if row["flag_zscore"]:
            methods.append("z-score")
        if row["flag_iqr"]:
            methods.append("IQR")
        lines.append(f"| {row['txn_id']} | {row['category']} | ${row['amount']:,.2f} | {', '.join(methods)} |")
    lines.append("")

    lines.append("## What this means\n")
    lines.append(
        "Transactions flagged by both methods are the highest-confidence candidates "
        "for review, they're unusual relative to their own category's typical spending, "
        "not just unusual in the dataset overall. Single-method flags are worth a lighter "
        "second look, since z-score and IQR occasionally disagree on borderline cases."
    )

    return "\n".join(lines)
