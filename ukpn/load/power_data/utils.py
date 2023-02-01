"""Function needed to load the data into the IterDatapipe"""
import logging
import os
from glob import glob
from pathlib import Path
from typing import Dict, Union

import numpy as np
import pandas as pd
import pytz
import xarray as xr
from pandas import DatetimeIndex

logger = logging.getLogger(__name__)


def load_csv_to_pandas(
    path_to_file: Path[Union, str], datetime_index_name: str = "time_utc"
) -> pd.DataFrame:
    """This function resamples a time series into regular intervals

    Args:
        path_to_file: Enter the absolute path to the csv file
        datetime_index_name: An appropriate index name for DateTimes

    """
    # Path file converted to posix() for a Windows folder path
    path_to_file = path_to_file.as_posix()

    # Getting the file name
    file_name = [os.path.basename(x).rsplit(".", 1)[0] for x in glob(path_to_file)]

    # Reading the csv data from the path
    df = pd.read_csv(path_to_file, names=[datetime_index_name, file_name[0]], sep=",", skiprows=1)

    if isinstance(df[df.columns[1]][0], str):
        # Convert data values from str into int
        df[file_name[0]] = pd.to_numeric(df[file_name[0]], errors="coerce")
    else:
        pass

    # Converting into datetime format
    df[datetime_index_name] = pd.to_datetime(df[datetime_index_name])

    # Reset index
    df = df.reset_index(drop=True)

    # Set index of original data frame as date_time
    df = df.set_index(datetime_index_name)

    return df


def bst_to_utc(original_df: pd.DataFrame, time_zone: str = "Europe/London") -> pd.DataFrame:
    """Function converts a datetimeindex localtime to UTC

    Args:
        original_df: Dataframe loaded from the csv file
        time_zone: Local time zone of the dataset
    """
    # Declaring the time zone
    local_standard_time = pytz.timezone(time_zone)

    # Getting the datetimes
    original_df.reset_index(inplace=True)
    original_df["time_utc"] = original_df["time_utc"].apply(lambda x: x.to_pydatetime())

    # Localise datetimes to timezone
    original_df["time_utc"] = original_df["time_utc"].apply(
        lambda x: local_standard_time.localize(x).astimezone(pytz.utc)
    )

    # Changing to pandas datetime
    original_df["time_utc"] = pd.to_datetime(original_df["time_utc"])

    # Set back as index
    original_df = original_df.set_index("time_utc")

    return original_df


def get_gsp_data_in_dict(
    folder_destination: str, required_file_format: str = "*.csv", count_gsp_data: bool = False
) -> Union[pd.DataFrame, Dict]:
    """This function counts the total number of GSP solar data

    Args:
        folder_destination: The destionation folder where are the files are
        required_file_format: The format of the UKPN power data files, usually .csv
        count_gsp_data: If true, returns a dictionary with total data points for each gsp
    """
    # Getting the file names and the corresponsing dataframes
    file_paths = os.path.join(folder_destination, required_file_format)
    file_paths = [x for x in glob(file_paths)]

    # Declaring a dictionary
    gsp_count_dict = {}
    gsp_dataframe_dict = {}

    # Getting the count of all the dataframes
    for file_path in file_paths:
        base_name = os.path.basename(file_path)
        file_name = os.path.splitext(base_name)[0]
        pandas_df = load_csv_to_pandas(path_to_file=Path(file_path))
        pandas_df_shape = pandas_df.shape[0]

        # Getiing the count of all the solar data from the GSP's
        gsp_count_dict[file_name] = pandas_df_shape

        # Getting the pandas dataframes of corresponding GSP's
        gsp_dataframe_dict[file_name] = pandas_df

    if count_gsp_data:
        return gsp_count_dict
    else:
        return gsp_dataframe_dict


def check_for_negative_data(
    original_df: pd.DataFrame, replace_with_nan: bool = False
) -> Union[DatetimeIndex, pd.DataFrame]:
    """This function helps in identifying if there are any negative values

    Args:
        original_df: Loaded dataframe from the csv file
        replace_with_nan: If true it replaces negative values with NaN's
    """
    # Check for the negative values
    check_non_negative = (original_df < 0).any()

    if not check_non_negative[0]:
        logger.info(f"The CSV file does contain the negative values {check_for_negative_data}")
        return original_df
    else:
        # Filtering the dataframe which has negative values
        negative_df = original_df.iloc[np.where(original_df[original_df.columns[0]].values < 0.0)]

        if not replace_with_nan:
            # Returns index values where there are negative numbers
            return negative_df.index
        else:
            # Replacing negative values with NaN's
            original_df.loc[negative_df.index] = np.nan
            # Returns original dataframe with negative values replaced with NaN's
            return original_df


def convert_xarray_to_netcdf(
    xarray_dataarray: xr.Dataset, folder_to_save: str, file_name: str = "canterbury_north.nc"
) -> None:
    """This function saves the xarray dataarray in netcdf file

    Args:
        xarray_dataarray: The dataarray that needs to be saved
        folder_to_save: Path of the destination folder
        file_name: Name of the file to be saved
    """

    # Define the path
    file_path = os.path.join(folder_to_save, file_name)

    # Check if the file exists
    check_file = os.path.isfile(file_path)

    if not check_file:
        # Saving the xarray
        xarray_dataarray.to_netcdf(path=file_path, engine="h5netcdf")

        # Close the data array
        xarray_dataarray.close()
