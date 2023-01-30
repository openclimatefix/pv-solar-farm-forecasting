import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import xarray as xr

from ukpn.load.gsp import (
    get_gsp_data_in_dict,
    drop_duplicates_and_fill_missing_time_intervals)

def test_check_frequency():
    """Testing if all the gsp has the same number of datetime values"""
    # Declaring the destination folder of all the files
    folder_destination = Path("/home/raj/ocf/pv-solar-farm-forecasting/tests/data/ukpn_dashboard_data")
    # Getting the data into dictionary format
    dataframe_dict = get_gsp_data_in_dict(folder_destination = folder_destination)
    # dataframe after filling in time intervals
    final_df = drop_duplicates_and_fill_missing_time_intervals(
        dataframe_dict = dataframe_dict,
        get_complete_dataframe = True
    )
    assert final_df.index.freq == pd.tseries.offsets.Minute(n = 10)

def test_compare_gsp_pvlib():
    path_to_file = "/home/raj/ocf/pv-solar-farm-forecasting/tests/data/gcp_gsp_zarr/pv_gsp.zarr"
    gsp_data_pvlib = xr.open_zarr(path_to_file)
    print(list(gsp_data_pvlib.coords))

    
# def test_check_non_negative_valus():
#     """Testing if any gsp's has negative values"""
#     # Declaring the destination folder of all the files
#     folder_destination = Path("/home/raj/ocf/pv-solar-farm-forecasting/tests/data/ukpn_dashboard_data")
#     # Getting the data into dictionary format
#     dataframe_dict = get_gsp_data_in_dict(folder_destination = folder_destination)
#     # For every dataframe in dict
#     for _, data_frame in dataframe_dict.items():
#         # Check negative values and replace with NaN
#         non_negative_df = check_for_negative_data(
#             original_df = data_frame,
#             replace_with_nan = True)  

#         # If false, means it has no negative values
#         assert (non_negative_df < 0.).any().any() == False

# def check_interpolation():
#     # Getting the file path
#     path_to_file = Path(r"/home/raj/ocf/pv-solar-farm-forecasting/tests/data/ukpn_dashboard_data/canterbury_north.csv")
#     # Loading into pandas
#     original_df = load_csv_to_pandas(path_to_file = path_to_file)  
    
# def test_write_data_into_xarray():
#     # Declaring the destination folder of all the files
#     folder_destination = Path("/home/raj/ocf/pv-solar-farm-forecasting/tests/data/ukpn_dashboard_data")
#     folder_to_save = "/home/raj/ocf/pv-solar-farm-forecasting/tests/data/ukpn_netcdf"
#     file_name = "ukpn_gsp_power.nc"

#     # convertng into xarray
#     data = OpenGSPData(
#         folder_destination = folder_destination,
#         folder_to_save = folder_to_save,
#         file_name = file_name,
#         write_as_netcdf = True)
#     data = next(iter(data))

#     # Check if the file is written
#     file_path = os.path.join(folder_to_save, file_name)
#     check = os.path.isfile(file_path)
#     if check:
#         print(f"Test to write the data into NetCDF is successful")
#     else:
#         print(f"Test to write the data into NetCDF Unsuccessful")
