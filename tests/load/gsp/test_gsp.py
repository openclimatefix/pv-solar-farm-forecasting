import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from ukpn.load import OpenGSPData
from ukpn.load.gsp.gsp_netcdf import get_gsp_into_xarray, convert_xarray_to_netcdf
from ukpn.load.gsp.gsp_power_data_utils import *

def test_check_frequency():
    """Testing if all the gsp has the same number of datetime values"""
    # Declaring the destination folder of all the files
    folder_destination = Path("/home/raj/ocf/pv-solar-farm-forecasting/tests/data/ukpn_dashboard_data")
    # Getting the data into dictionary format
    dataframe_dict = get_gsp_data_in_dict(folder_destination = folder_destination)
    # dataframe after filling in time intervals
    final_df_dict = drop_duplicates_and_fill_missing_time_intervals(
        dataframe_dict = dataframe_dict
    )
    df_shape = []
    # Check that shape of each dataframe matches with one another
    for _, data_frame in final_df_dict.items():
        df_shape.append(data_frame.shape[0])

    assert df_shape.count(df_shape[0]) == len(df_shape)

def test_check_non_negative_valus():
    """Testing if any gsp's has negative values"""
    # Declaring the destination folder of all the files
    folder_destination = Path("/home/raj/ocf/pv-solar-farm-forecasting/tests/data/ukpn_dashboard_data")
    # Getting the data into dictionary format
    dataframe_dict = get_gsp_data_in_dict(folder_destination = folder_destination)
    # For every dataframe in dict
    for _, data_frame in dataframe_dict.items():
        # Check negative values and replace with NaN
        non_negative_df = check_for_negative_data(
            original_df = data_frame,
            replace_with_nan = True)  

        # If false, means it has no negative values
        assert (non_negative_df < 0.).any().any() == False

def check_interpolation():
    # Getting the file path
    path_to_file = Path(r"/home/raj/ocf/pv-solar-farm-forecasting/tests/data/ukpn_dashboard_data/canterbury_north.csv")
    # Loading into pandas
    original_df = load_csv_to_pandas(path_to_file = path_to_file)  
    
def test_write_data_into_xarray():
    # Declaring the destination folder of all the files
    folder_destination = Path("/home/raj/ocf/pv-solar-farm-forecasting/tests/data/ukpn_dashboard_data")
    # Getting the data into dictionary format
    dataframe_dict = get_gsp_data_in_dict(folder_destination = folder_destination)
    # convertng into xarray
    data = get_gsp_into_xarray(folder_destination = folder_destination)
    print(data)