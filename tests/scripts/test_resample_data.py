import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ukpn.scripts import resample_dataframe


def test_resample_data():
    csv_path = "/home/raj/ocf/pv-solar-farm-forecasting/tests/data/test.csv"
    original_df = resample_dataframe(path_to_file=csv_path)
    resampled_df = resample_dataframe(path_to_file=csv_path, resample=True)
    resampled_df["minutes"] = resampled_df["date_time"].dt.minute % 5

    # Checking if the time-seires contains only 5 minute
    # intervals
    assert (resampled_df["minutes"] == 0).all() == True

    # Checking if there are any NaN's
    assert (resampled_df["date_time"] == np.nan).any() == False
    assert (resampled_df["bad_data"] == np.nan).any() == False
