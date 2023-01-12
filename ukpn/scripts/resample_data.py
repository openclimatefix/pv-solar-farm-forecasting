"""Function to resample the irreggular time series data into regular"""
import os
import random
from glob import glob
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def load_csv_to_pandas(path_to_file: str) -> pd.DataFrame:
    """This function resamples a time series into regular intervals

    Args:
        path_to_file: Enter the absolute path to the csv file

    """
    # Getting the file name
    file_name = [os.path.basename(x).rsplit(".", 1)[0] for x in glob(path_to_file)]

    # Reading the csv data from the path
    df = pd.read_csv(path_to_file, header=None, names=["date_time", file_name[0]], sep=",")

    # Convert data values from str into int
    df[file_name[0]] = pd.to_numeric(df[file_name[0]], errors="coerce")

    # Interpolate with padding
    df[file_name[0]] = df[file_name[0]].interpolate(method="pad", limit=2)

    # Converting into datetime format
    df["date_time"] = pd.to_datetime(df["date_time"])

    # Reset index
    df = df.reset_index(drop=True)

    return df


def interpolation_pandas(
    original_df: pd.DataFrame, start_date: str, end_date: str, freq: str = "5Min"
) -> pd.DataFrame:
    """Interpolating the irregular frequency time series data

    Args:
        original_df: The data frame after loading csv file
        start_date: Start date of interpolated time series
        end_date: End date of interpolated time series
        freq: Frequency of the time series intended
    """

    # Set index of original data frame as date_time
    original_df = original_df.set_index("date_time")

    # Create date range with proper minute frequency that needs to be interpolated
    interpolate_time_series = pd.date_range(start=start_date, end=end_date, freq=freq)

    # Creating an empty data frame with Nan's of that date range
    interpolated_data_frame = pd.Series(
        np.tile(np.nan, len(interpolate_time_series)), index=interpolate_time_series
    )

    # Interpolate between original irregular intervaled df and reggular created df
    final_data_frame = pd.concat([original_df, interpolated_data_frame]).sort_index().interpolate()
    common_df = final_data_frame.index.intersection(interpolated_data_frame.index)
    final_data_frame = final_data_frame.loc[common_df]

    # Drop the column with all NaN's
    final_data_frame = final_data_frame.dropna(axis=1, how="all")

    return final_data_frame


def select_random_date(
    original_df: pd.DataFrame, resampled_df: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Selecting a random date out of the series and slicing the dataframe

    Args:
        original_df : Original dataframe before resampling
        resampled_df : Resampled dataframe after resampling
    """
    df_dates = original_df["date_time"].dt.date.to_list()
    df_date = random.choice(df_dates)
    original_sliced_df = original_df[original_df["date_time"].dt.date == df_date]
    resampled_sliced_df = resampled_df[resampled_df["date_time"].dt.date == df_date]
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
