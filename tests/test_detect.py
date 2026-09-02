import pandas as pd
from src.detect import flag_zscore, flag_iqr, combined_flags


def _sample_df():
    return pd.DataFrame({
        "txn_id": ["t1", "t2", "t3", "t4", "t5"],
        "category": ["food", "food", "food", "food", "food"],
        "amount": [20.0, 21.0, 19.5, 22.0, 5000.0],  # last one is an obvious outlier
    })


def test_zscore_flags_extreme_value():
    df = _sample_df()
    out = flag_zscore(df, z_thresh=1.5)
    assert out.loc[out["txn_id"] == "t5", "flag_zscore"].iloc[0] == True
    assert out.loc[out["txn_id"] == "t1", "flag_zscore"].iloc[0] == False


def test_iqr_flags_extreme_value():
    df = _sample_df()
    out = flag_iqr(df, k=1.5)
    assert out.loc[out["txn_id"] == "t5", "flag_iqr"].iloc[0] == True


def test_combined_flags_agree_on_clear_outlier():
    df = _sample_df()
    out = combined_flags(df, z_thresh=1.5)
    assert out.loc[out["txn_id"] == "t5", "flag_both"].iloc[0] == True


def test_zero_variance_category_does_not_crash():
    df = pd.DataFrame({
        "txn_id": ["t1", "t2", "t3"],
        "category": ["food", "food", "food"],
        "amount": [10.0, 10.0, 10.0],
    })
    out = combined_flags(df)
    assert out["flag_zscore"].sum() == 0
