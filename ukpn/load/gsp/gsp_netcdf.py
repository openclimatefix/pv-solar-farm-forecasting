"""GSP Loader"""
import os
from pathlib import Path
from glob import glob
from typing import Union
import logging
from datetime import datetime, time, timedelta

import numpy as np
import pandas as pd
import xarray as xr

from ukpn.load.gsp.gsp_power_data_utils import *
from ukpn.load.gsp.gsp_meta_data_utils import *

logger = logging.getLogger(__name__)

def get_gsp_into_xarray(
    folder_destination: Path[Union, str]
    )-> xr.DataArray:
    """This method loads GSP power data from .csv files
    and the metadata, stores in an xarray Dataarray

    Args:
        path_to_file: Enter the absolute path to the csv file

    """

    # File path as posix for Windows users
    folder_destination = Path(folder_destination).as_posix()

    # Loading every csv file from the path into a dataframe
    gsp_data_in_dict = get_gsp_data_in_dict(folder_destination = folder_destination)
    
    # After interpolation dictionary
    gsp_interpolated_dict = {}

    # Pre-processing every data frame
    for gsp_name, data_frame in gsp_data_in_dict.items():
        
        # Check for negative data and replace with NaN's
        non_negative_df = check_for_negative_data(
            original_df = data_frame,
            replace_with_nan = True)

        # Interpolating the missing values
        start_date = non_negative_df.first_valid_index().strftime("%Y-%m-%d")
        end_date = non_negative_df.last_valid_index().strftime("%Y-%m-%d")
        interpolated_df = interpolation_pandas(
            original_df = non_negative_df, 
            start_date = start_date,
            end_date = end_date,
            freq = "10Min",
            drop_last_row = True)
   
        # Dropping the duplicates
        interpolated_df = interpolated_df[~interpolated_df.index.duplicated(keep = 'first')]

        # Writing new dictionary with interpolating
        gsp_interpolated_dict[gsp_name] = interpolated_df

    # Complete gsp dataframe after interpolation
    gsp_dataframe_after_dropping = drop_duplicates_and_fill_missing_time_intervals(
        dataframe_dict = gsp_interpolated_dict,
        get_complete_dataframe = True)
    
    # Metered power values into an array
    gsp_metered_power_values = gsp_dataframe_after_dropping.to_numpy()
    # GSP names
    gsp_names = gsp_dataframe_after_dropping.columns
    # Datetime values
    gsp_datetimes = gsp_dataframe_after_dropping.index
    
    # Creating an xarray dataset
    ds = xr.Dataset(
        data_vars = dict(
            power = (["time_utc", "gsp_id"], gsp_metered_power_values)),
        coords = dict(
            time_utc = gsp_datetimes,
            gsp_id = gsp_names
        ),
        attrs = dict(description = "Metered power generation (MW) of GSP's")
    )
    return ds

def convert_xarray_to_netcdf(
    xarray_dataarray: xr.DataArray,
    folder_to_save: str,
    file_name: str = "canterbury_north.nc"
    ):
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
        xarray_dataarray.to_netcdf(path = file_path)

        # Close the data array
        xarray_dataarray.close()
