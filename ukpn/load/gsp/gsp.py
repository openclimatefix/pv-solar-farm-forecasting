"""GSP Loader"""
import os
from pathlib import Path
from glob import glob
from typing import Union, Optional
import logging
from datetime import datetime, time, timedelta

import numpy as np
import pandas as pd
import xarray as xr

from ukpn.load import *

from torchdata.datapipes import functional_datapipe
from torchdata.datapipes.iter import IterDataPipe

logger = logging.getLogger(__name__)

@functional_datapipe("open_gsp_data")
class OpenGSPDataIterDataPipe(IterDataPipe):
    """This method loads GSP power data from .csv files
    and the metadata, stores in an xarray Dataarray
    """

    def __init__(
        self,
        folder_destination: Path[Union, str],
        folder_to_save: Optional[str] = None,
        file_name: Optional[str] = None,      
        write_as_netcdf: bool = False):
        """This function reads the csv data into a dataframe

        Args:
            path_to_file: Enter the absolute path to the csv file

        """

        self.folder_destination = folder_destination
        self.folder_to_save = folder_to_save
        self.file_name = file_name
        self.write_as_netcdf = write_as_netcdf

    def __iter__(self) -> xr.DataArray:
        """This returns the xarray Dataarray"""
        # File path as posix for Windows users
        folder_destination = Path(self.folder_destination).as_posix()

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
        final_dataset = xr.Dataset(
            data_vars = dict(
                power = (["time_utc", "gsp_id"], gsp_metered_power_values)),
            coords = dict(
                time_utc = gsp_datetimes,
                gsp_id = gsp_names
            ),
            attrs = dict(description = "Metered power generation (MW) of GSP's")
        )

        if self.write_as_netcdf:
            convert_xarray_to_netcdf(
                xarray_dataarray = final_dataset,
                folder_to_save = self.folder_to_save,
                file_name = self.file_name
            )

        return iter(final_dataset)