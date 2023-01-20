"""Function needed to load the data into the IterDatapipe"""
import os
from pathlib import Path
from glob import glob
from typing import Union, Dict 
import logging

import numpy as np
import pandas as pd
from pandas import DatetimeIndex

logger = logging.getLogger(__name__)

def load_csv_to_pandas(
    path_to_file: Path[Union, str],
    datetime_index_name: str = "time_utc") -> pd.DataFrame:
    """This function resamples a time series into regular intervals

    Args:
        path_to_file: Enter the absolute path to the csv file

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

        # Interpolate with padding
        df[file_name[0]] = df[file_name[0]].interpolate(method="pad", limit=2)        
    else:
        pass

    # Converting into datetime format
    df[datetime_index_name] = pd.to_datetime(df[datetime_index_name])

    # Reset index
    df = df.reset_index(drop=True)

    # Set index of original data frame as date_time
    df = df.set_index(datetime_index_name)

    return df

def get_gsp_data_in_dict(
    folder_destination: str,
    required_file_format: str = "*.csv",
    count_gsp_data: bool = False
    ) -> Union[pd.DataFrame, Dict]:
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

        # Getiing the count of all the solar data from the GSP's
        gsp_count_dict[file_name] = pandas_df_shape

        # Getting the pandas dataframes of corresponding GSP's
        gsp_dataframe_dict[file_name] = pandas_df

    if count_gsp_data:
        return gsp_count_dict
    else:
        return gsp_dataframe_dict

def check_for_negative_data(
    original_df: pd.DataFrame,
    replace_with_nan: bool = False
    )-> Union[DatetimeIndex, pd.DataFrame]:
    """This function helps in indentifying if there are any neagtive values

    Args:
        original_df: Loaded dataframe from the csv file
        replace_with_nan: If true it replaces negative values with NaN's
    """
    # Check for the negative values
    check_non_negative = (original_df < 0).any()
    if not check_non_negative[0]:
        logger.info(f"The CSV file does contain the negative values {check_for_negative_data}")
    else:
        # Filtering the dataframe which has negative values
        negative_df = original_df.iloc[np.where(original_df[original_df.columns[0]].values < 0.)]      
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