import matplotlib.pyplot as plt
import numpy as np

from ukpn.scripts import resample_data


def test_resample_data():
    csv_path = "/home/raj/ocf/pv-solar-farm-forecasting/tests/data/test.csv"
    df = resample_data(path_to_file=csv_path)
    df["minutes"] = df["date_time"].dt.minute % 5
    assert (df["minutes"] == 0).all() == True
    assert (df["date_time"] == np.nan).any() == False
    assert (df["bad_data"] == np.nan).any() == False
