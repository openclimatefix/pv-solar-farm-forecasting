### UKPN PV Live data

This folder consists of utility functions and `datapipes` that configure a given GSP PV data into a required format. The configuration involves pre-processing steps of the data, for example, such as checking for negative PV generation values, missing time intervals etc.

### Usage

Some of the pre-processing steps in the `datapipeline` consist of are as follows:

1. Checking for the negative data
```python
import pandas as pd
from ukpn.load import check_for_negative_data

# Load the csv file with the path
path_to_file = "~/home/...../*.csv"
data = pd.read_csv(path_to_file, sep = ",")

# Check for negative data and replace with NaN's
non_negative_df = check_for_negative_data(original_df=data_frame, replace_with_nan=True)
```

2. Check the duplicated and missing time intervals:
Missing time intervals would be the rows with NaN values in the below `non_negative_df` data frame
```python
# Check duplicates
check = non_negative_df.index.duplicated().any()

if check:
    # Drop duplicates
    non_negative_df = non_negative_df[~non_negative_df.index.duplicated(keep="last")]

# Filling missing intervals
# Frequency of the given CSV file
freq = "10Min"
non_negative_df = non_negative_df.asfreq(freq)
```

To write all the CSV files into a single NetCDF file:
```python
import os
from pathlib import Path
import pandas as pd
import xarray as xr

from ukpn.load import OpenGSPData

folder_destination = "tests/data/grafana_dashboard"
file_name = "ukpn_gsp.nc"

# check if file exists
file_path = os.path.join(folder_destination, file_name)
check_file = os.path.isfile(file_path)

if check_file:
    os.remove(file_path)
else:
    data = OpenGSPData(
        folder_destination = folder_destination,
        freq: str = "10Min",
        folder_to_save = folder_destination,
        file_name = file_name,
        write_as_netcdf = True      
    )

print(data)
```