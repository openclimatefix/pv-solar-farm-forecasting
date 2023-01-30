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

from ukpn.load.gsp import (
    get_gsp_data_in_dict,
    check_for_negative_data,
    bst_to_utc,
    drop_duplicates_and_fill_missing_time_intervals,
    interpolation_pandas,
    convert_xarray_to_netcdf)

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
        freq: str = "10Min",
        folder_to_save: Optional[str] = None,
        file_name: Optional[str] = None,
        interpolation: Optional[bool] = False,
        drop_duplicates: Optional[bool] = False,      
        write_as_netcdf: bool = False):
        """This function reads the csv data into a dataframe

        Args:
            path_to_file: Enter the absolute path to the csv file

        """

        self.folder_destination = folder_destination
        self.freq = freq
        self.folder_to_save = folder_to_save
        self.file_name = file_name
        self.interpolation = interpolation
        self.drop_duplicates = drop_duplicates
        self.write_as_netcdf = write_as_netcdf

    def __iter__(self) -> xr.DataArray:
        """This returns the xarray Dataarray"""
        # File path as posix for Windows users
        folder_destination = Path(self.folder_destination).as_posix()

        # Loading every csv file from the path into a dataframe
        gsp_data_in_dict = get_gsp_data_in_dict(folder_destination = folder_destination)
        
        # Declaring final dataframe
        gsp_dataframe = pd.DataFrame()

        # Pre-processing every data frame
        for gsp_name, data_frame in gsp_data_in_dict.items():
            
            # Check for negative data and replace with NaN's
            non_negative_df = check_for_negative_data(
                original_df = data_frame,
                replace_with_nan = True)
            
            # Converting to UTC
            non_negative_df = bst_to_utc(original_df = non_negative_df)

            # Check duplicates
            check = non_negative_df.index.duplicated().any()
            if check:
                # Drop duplicates
                non_negative_df = non_negative_df[~non_negative_df.index.duplicated(keep = 'last')] 
            
            # Filling missing intervals
            non_negative_df = non_negative_df.asfreq(self.freq)
            
            # Getting each df into a single big dataframe
            gsp_dataframe = pd.concat([gsp_dataframe, non_negative_df], axis = 1, join = "outer")

            print(f"\nPre-processing for {gsp_name} has completed")
        
        # Metered power values into an array
        gsp_metered_power_values = gsp_dataframe.to_numpy()
        # GSP names
        gsp_names = gsp_dataframe.columns
        # Datetime values
        gsp_datetimes = gsp_dataframe.index.values

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

        return final_dataset