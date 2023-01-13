import os
import random
from glob import glob

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import interpolate

from ukpn.scripts import interpolation_pandas, load_csv_to_pandas, select_random_date


def test_resample_data():
    csv_path = "/home/raj/ocf/pv-solar-farm-forecasting/tests/data/test.csv"
    file_name = [os.path.basename(x).rsplit(".", 1)[0] for x in glob(csv_path)]
    original_df = load_csv_to_pandas(path_to_file=csv_path)
    interpolated_df = interpolation_pandas(
        original_df=original_df, start_date="2017-11-25", end_date="2018-01-13"
    )
    interpolated_df["minutes"] = interpolated_df.index.values

    # Checking if the time-seires contains only 5 minute
    # intervals
    assert (interpolated_df["minutes"].dt.minute % 5 == 0).all() == True

    # Checking if there are any NaN's
    assert np.isnan(interpolated_df.index.values).any() == False
    assert (interpolated_df[file_name[0]] == np.nan).any() == False