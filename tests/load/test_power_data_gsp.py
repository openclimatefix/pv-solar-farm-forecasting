import os
from pathlib import Path

import xarray as xr

from ukpn.load import OpenGSPData, check_for_negative_data, get_gsp_data_in_dict


def test_write_netcdf():
    folder_destination = "tests/data"
    folder_to_save = "tests/data"
    file_name = "ukpn_gsp.nc"

    # check if file exists
    file_path = os.path.join(folder_to_save, file_name)
    check_file = os.path.isfile(file_path)
    if not check_file:
        xr_data = OpenGSPData(
            folder_destination=folder_destination,
            folder_to_save=folder_to_save,
            file_name=file_name,
            write_as_netcdf=True,
        )

        xr_data = iter(xr_data)
        if xr_data is not None:
            print("\nWriting data into NetCDF is successful")
        else:
            print("\nWriting data into NetCDF is unsuccessful")

    else:
        xr_data = xr.open_dataset(file_path, engine="h5netcdf")

    data_coords = list(xr_data.coords)

    assert len(data_coords) == 2


def test_check_non_negative_valus():
    """Testing if any gsp's has negative values"""
    # Declaring the destination folder of all the files
    folder_destination = Path("tests/data")
    # Getting the data into dictionary format
    dataframe_dict = get_gsp_data_in_dict(folder_destination=folder_destination)
    # For every dataframe in dict
    for _, data_frame in dataframe_dict.items():
        # Check negative values and replace with NaN
        non_negative_df = check_for_negative_data(original_df=data_frame, replace_with_nan=True)

        # If false, means it has no negative values
        assert (non_negative_df < 0.0).any().any() == False
