import numpy as np
from pathlib import Path
from ukpn.load import OpenGSPData
from ukpn.load.gsp.gsp_netcdf import get_gsp_into_xarray, convert_xarray_to_netcdf

def test_open_gsp_data():
    path_to_file = r"/home/raj/ocf/pv-solar-farm-forecasting/tests/data/ukpn_dashboard_data/canterbury_north.csv"
    path_to_file = Path(path_to_file)
    data = get_gsp_into_xarray(path_to_file = path_to_file)
    
    folder_path = "/home/raj/ocf/pv-solar-farm-forecasting/tests/data/ukpn_netcdf"
    nc_file = convert_xarray_to_netcdf(
        xarray_dataarray = data,
        folder_to_save = folder_path)