"""Function to resample the irreggular time series data into regular"""
import matplotlib.pyplot as plt
import pandas as pd
from dateutil.parser import parse


def resample_data(
    path_to_file: str, intervals: str = "5Min", resample: bool = True
) -> pd.DataFrame:
    """This function resamples a time series into regular intervals

    Args:
        path_to_file: Enter the absolute path to the csv file
        intervals: Enter the intervals that you want this data to have

    """
    # Reading the csv data from the path
    csv_data = pd.read_csv(path_to_file, header=None, names=["date_time", "bad_data"], sep=",")

    # Convert data values from str into int
    csv_data["bad_data"] = pd.to_numeric(csv_data["bad_data"], errors="coerce")

    # Drop Na
    csv_data.dropna(inplace=True)

    # Converting into datetime format
    csv_data["date_time"] = csv_data["date_time"].apply(parse)

    if resample:
        # 5min sampling
        csv_data = (
            csv_data.resample(intervals, on="date_time").mean().dropna().ffill().reset_index()
        )

    return csv_data


def plot_before_after_resampling():
    # If you want to plot this, you need to use
    # '#%%' at the first line of the .py file in VScode
    # that will convert the file into a cell and displays
    # a plot
    csv_path = "/home/raj/ocf/pv-solar-farm-forecasting/tests/data/test.csv"
    original_df = resample_data(path_to_file=csv_path, resample=False)
    resampled_df = resample_data(path_to_file=csv_path)

    # create timeseries plot
    original_df.plot(x="date_time", y="bad_data")
    plt.xlabel("Date Range")
    plt.ylabel("Bad data")
    plt.title("Time series bad data before resampling")
    plt.show()

    # create timeseries plot
    resampled_df.plot(x="date_time", y="bad_data")
    plt.xlabel("Date Range")
    plt.ylabel("Bad data")
    plt.title("Time series bad data after resampling")
    plt.show()
