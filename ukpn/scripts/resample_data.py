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

    # Set index of original data frame as date_time
    df = df.set_index("date_time")

    return df


def interpolation_pandas(
    original_df: pd.DataFrame,
    start_date: str = "2017-11-25",
    end_date: str = "2018-01-13",
    freq: str = "5Min",
) -> pd.DataFrame:
    """Interpolating the irregular frequency time series data

    Args:
        original_df: The data frame after loading csv file
        start_date: Start date of interpolated time series
        end_date: End date of interpolated time series
        freq: Frequency of the time series intended
    """

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
    original_df: pd.DataFrame, interpolated_df: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Selecting a random date out of the series and slicing the dataframe

    Args:
        original_df : Original dataframe before resampling
        interpolated_df : Resampled dataframe after resampling
    """
    df_dates = original_df.index.values
    df_date = random.choice(df_dates)
    df_date = pd.to_datetime(df_date)
    df_date = df_date.date()
    original_sliced_df = original_df.loc[str(df_date)]
    interpolated_sliced_df = interpolated_df.loc[str(df_date)]
    return [original_sliced_df, interpolated_sliced_df]


def plot_before_after_resampling(original_df: pd.DataFrame, interpolated_df=pd.DataFrame):
    # If you want to plot this, you need to use
    # '#%%' at the first line of the .py file in VScode
    # that will convert the file into a cell and displays
    # a plot

    # create timeseries plot
    """This function is soley used to plot the files in VScode

    Args:
        original_df: Dataframe before resampling
        interpolated_df: Dataframe after resampling
    """
    original_df.plot(y="test", use_index=True)
    plt.xlabel("Date Range")
    plt.ylabel("Bad data")
    plt.title("Time series bad data before interpolation")
    plt.show()

    # create timeseries plot
    interpolated_df.plot(y="test", use_index=True)
    plt.xlabel("Date Range")
    plt.ylabel("Bad data")
    plt.title("Time series bad data after interpolation")
    plt.show()
