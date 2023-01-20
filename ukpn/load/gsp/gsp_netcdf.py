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
    path_to_file: Path[Union, str],
    datetime_index_name: str = "time_utc",
    eastings: np.int64 = 615378,
    northings: np.int64 = 165525
    )-> xr.DataArray:
    """This method loads GSP power data from .csv files
    and the metadata, stores in an xarray Dataarray

    Args:
        path_to_file: Enter the absolute path to the csv file

    """

    # File path as posix for Windows users
    path_to_file = Path(path_to_file).as_posix()

    # Loading the csv file from the path into a dataframe
    original_df = load_csv_to_pandas(path_to_file = path_to_file)

    # Check for negative data and replace with NaN's
    non_negative_df = check_for_negative_data(
        original_df = original_df,
        replace_with_nan = True)
    
    # Interpolating the missing values
    start_date = non_negative_df.first_valid_index().strftime("%Y-%m-%d")
    end_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days = 1)).strftime("%Y-%m-%d")
    interpolated_df = interpolation_pandas(
        original_df = non_negative_df, 
        start_date = start_date,
        end_date = end_date,
        freq = "10Min",
        drop_last_row = True)

    # Dropping the duplicates
    interpolated_df = interpolated_df[~interpolated_df.index.duplicated(keep = 'first')]

    # define xarray data values, coordinates, variables
    xarray_data_values = interpolated_df[interpolated_df.columns[0]].values
    xarray_coords_values = interpolated_df.index

    # Creating the Xarray
    final_data_array = xr.DataArray(
        data = xarray_data_values,
        dims = [datetime_index_name],
        coords = {
            datetime_index_name : xarray_coords_values,
            'eastings' : eastings,
            'northings': northings}
    )

    return final_data_array

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

    # Saving the xarray
    xarray_dataarray.to_netcdf(path = file_path)

    # Close the data array
    xarray_dataarray.close()
