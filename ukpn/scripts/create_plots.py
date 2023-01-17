import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr



def first_plot(
    original_df: pd.DataFrame
    ):

    # Creating a data array from the pandas dataframe
    data_array_coords = original_df.index.values
    data_array_values = original_df[original_df.columns[0]].values
    data_array = xr.DataArray(
        data = data_array_values,
        dims = "time_utc",
        coords = {"time_utc": data_array_coords}
    )

    # Trimming the insufficent data in the last day of the time series
