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
        path_to_file: Path[Union, str],
        datetime_index_name: str = "time_utc",
        eastings: np.int64 = 615378,
        northings: np.int64 = 165525):
        """This function reads the csv data into a dataframe

        Args:
            path_to_file: Enter the absolute path to the csv file

        """

        self.path_to_file = path_to_file
        self.datetime_index_time = datetime_index_name
        self.eastings = eastings
        self.northings = northings

    def __iter__(self) -> xr.DataArray:
        """This returns the xarray Dataarray"""
        # File path as posix for Windows users
        self.path_to_file = Path(self.path_to_file).as_posix()

        # Loading the csv file from the path into a dataframe
        original_df = load_csv_to_pandas(path_to_file = self.path_to_file)

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
            dims = [self.datetime_index_time],
            coords = {
                self.datetime_index_time : xarray_coords_values,
                'eastings' : self.eastings,
                'northings': self.northings}
        )

        return iter(final_data_array)