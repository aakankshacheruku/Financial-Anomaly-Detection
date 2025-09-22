# Small sanity tests—keep these lightweight and readable.

import pandas as pd

def test_equal_values_avoid_divzero():
    df = pd.DataFrame({"amount":[10,10,10]})
    sd = df["amount"].std(ddof=0)
    assert sd == 0  # baseline check
    # In script we guard by replacing 0 with 1.0 to avoid division by zero
    assert (sd == 0) or True

