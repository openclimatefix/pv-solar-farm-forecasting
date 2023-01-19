"""Function to resample the irreggular time series data into regular"""
import os
import random
from glob import glob
from typing import Tuple
import logging

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

def load_csv_to_pandas(path_to_file: str) -> pd.DataFrame:
    """This function resamples a time series into regular intervals

    Args:
        path_to_file: Enter the absolute path to the csv file

    """
    # Getting the file name
    file_name = [os.path.basename(x).rsplit(".", 1)[0] for x in glob(path_to_file)]

    # Reading the csv data from the path
    df = pd.read_csv(path_to_file, names=["date_time", file_name[0]], sep=",", skiprows=1)

    if isinstance(df[df.columns[1]][0], str):
        # Convert data values from str into int
        df[file_name[0]] = pd.to_numeric(df[file_name[0]], errors="coerce")

        # Interpolate with padding
        df[file_name[0]] = df[file_name[0]].interpolate(method="pad", limit=2)        
    else:
        pass

    # Converting into datetime format
    df["date_time"] = pd.to_datetime(df["date_time"])

    # Reset index
    df = df.reset_index(drop=True)

    # Set index of original data frame as date_time
    df = df.set_index("date_time")

    return df

def count_total_gsp_solar(
    folder_destination: str,
    required_file_format: str = "*.csv",
    get_gsp_dataframe_dict: bool = False
    ):
    """This function counts the total number of GSP solar data 

    Args:
        folder_destination: The destionation folder where are the files are
    """
    # Getting the file names and the corresponsing dataframes
    file_paths = os.path.join(folder_destination, required_file_format)
    file_paths = [x for x in glob(file_paths)]

    # Declaring a dictionary
    gsp_count_dict = {}
    gsp_dataframe_dict = {}

    # Getting the count of all the dataframes
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        pandas_df = load_csv_to_pandas(path_to_file = file_path)
        pandas_df_shape = pandas_df.shape[0]
        gsp_count_dict[file_name] = pandas_df_shape
        gsp_dataframe_dict[file_name] = pandas_df

    if get_gsp_dataframe_dict:
        return gsp_dataframe_dict
    else:
        return gsp_count_dict

def check_for_negative_data(
    original_df: pd.DataFrame,
    replace_with_nan: bool = False
    ):
    """This function helps in indentifying if there are any neagtive values

    Args:
        original_df: Loaded dataframe from the csv file
        replace_with_nan: If truem it replaces negative values with NaN's
    """
    # Check for the negative values
    check_non_negative = (original_df < 0).any()
    if not check_non_negative[0]:
        logger.info(f"The CSV file does contain the negative values {check_for_negative_data}")
    else:
        # Filtering the dataframe which has negative values
        negative_df = original_df.iloc[np.where(original_df[original_df.columns[0]].values < 0.)]
        print(negative_df)       
        if not replace_with_nan:
            # Returns index values where there are negative numbers
            return negative_df.index
        else:     
            # Replacing negative values with NaN's
            original_df.loc[negative_df.index] = np.nan
            # Returns original dataframe with negative values replaced with NaN's
            return original_df
      

def interpolation_pandas(
    original_df: pd.DataFrame,
    start_date: str = "2017-11-25",
    end_date: str = "2018-01-13",
    freq: str = "5Min",
    drop_last_row: bool = False
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

    if drop_last_row:
        interpolated_data_frame.drop(interpolated_data_frame.tail(1).index,inplace=True)

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


def plot_before_after_interpolating(
    original_df: pd.DataFrame,
    interpolated_df: pd.DataFrame,
    regular_plot: bool = False,
    cumsum_plot: bool = False,
):
    # If you want to plot this, you need to use
    # '#%%' at the first line of the .py file in VScode
    # that will convert the file into a cell and displays
    # a plot

    # create timeseries plot
    """This function is soley used to plot the files in VScode

    Args:
        original_df: Dataframe before resampling
        interpolated_df: Dataframe after resampling
        regular_plot: Plotting without any operations
        cumsum_plot: Plotting with Cummulative sum over time
    """
    if regular_plot:
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

    if cumsum_plot:
        df = original_df.cumsum()
        df.plot(y="test", use_index=True)
        plt.title("Cummulative plot over a single day before interpolation")
        plt.show()

        df = interpolated_df.cumsum()
        df.plot(y="test", use_index=True)
        plt.title("Cummulative plot over a single day after interpolation")
        plt.show()