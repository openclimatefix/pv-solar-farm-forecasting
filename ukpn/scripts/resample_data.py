"""Function to resample the irreggular time series data into regular"""
from typing import Optional, Tuple
import random
import matplotlib.pyplot as plt
import pandas as pd
from dateutil.parser import parse


def resample_dataframe(
    path_to_file: str, intervals: Optional[str] = "5Min", resample: Optional[bool] = False
) -> pd.DataFrame:
    """This function resamples a time series into regular intervals

    Args:
        path_to_file: Enter the absolute path to the csv file
        intervals: Enter the intervals that you want this data to have
        resample: Option to resample the dataframe

    """
    # Reading the csv data from the path
    df = pd.read_csv(path_to_file, header=None, names=["date_time", "bad_data"], sep=",")

    # Convert data values from str into int
    df["bad_data"] = pd.to_numeric(df["bad_data"], errors="coerce")

    # Drop Na
    df.dropna(inplace=True)

    # Converting into datetime format
    df["date_time"] = df["date_time"].apply(parse)

    # Reset index
    df = df.reset_index(drop=True)

    # If resample is True
    if resample:

        # Rounding to nearest 5 minutes
        df["date_time"] = df["date_time"].dt.round("5Min")

        # Grouping the data by similar date_time
        df["bad_data"] = df.groupby("date_time")["bad_data"].transform("min")

        # Dropping the duplicates
        df = df.drop_duplicates(subset=["date_time"])

        # Resampling with 5 minute intervals
        df = df.set_index("date_time").resample(intervals).ffill().reset_index()

    return df

def select_random_date(
    original_df: pd.DataFrame, 
    resampled_df=pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame] :
    df_dates = original_df["date_time"].dt.date.to_list()
    df_dates = random.choice(df_dates)
    original_sliced_df = original_df[original_df["date_time"].dt.date == df_dates]
    resampled_sliced_df = resampled_df[resampled_df["date_time"].dt.date == df_dates]
    return [original_sliced_df, resampled_sliced_df]

def plot_before_after_resampling(original_df: pd.DataFrame, resampled_df=pd.DataFrame):
    # If you want to plot this, you need to use
    # '#%%' at the first line of the .py file in VScode
    # that will convert the file into a cell and displays
    # a plot

    # create timeseries plot
    """This function is soley used to plot the files in VScode

    Args:
        original_df: Dataframe before resampling
        resampled_df: Dataframe after resampling
    """
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


# path_to_file = "/home/raj/ocf/pv-solar-farm-forecasting/tests/data/test.csv"
# original_df = resample_dataframe(path_to_file=path_to_file)
# resampled_df = resample_dataframe(path_to_file=path_to_file, resample=True)
# sliced_df = select_random_date(original_df, resampled_df)
# plot_before_after_resampling(sliced_df[0], sliced_df[1])

