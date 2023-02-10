import os
from glob import glob
import logging
from typing import List

from grafana_data_download import automate_csv_download

logger = logging.getLogger(__name__)

def get_gsp_names():
    """Function to get all the GSP names from dashboard"""
    grafana = automate_csv_download()
    grafana.Initialise_chrome()
    names = grafana.get_gsp_names_from_dashbaord()
    assert names is not None
    return names

def get_dropdown_text(gsp_name:str):
    """Check the type of data in dropdown"""
    grafana = automate_csv_download()
    grafana.Initialise_chrome()
    grafana.set_gsp_name_in_dashboard(gsp_name = gsp_name)
    grafana.scroll_to_element_and_click()
    grafana.download_from_side_panel(close_browser = True)

def download_solar_data(
    download_directory: str,
    gsp_names_list = List
    ):
    """Downloading the data for each gsp"""
    # Getting the list of gsp names
    gsp_names_list = list(reversed(gsp_names_list))   

    for gsp_name in gsp_names_list:
        # Initalise chrome
        grafana = automate_csv_download(
            download_directory = download_directory)
        grafana.Initialise_chrome()

        # Getting the gsp names in lower case format
        seperator = "_"
        gsp_name_lcase = gsp_name.lower()
        if len(gsp_name_lcase.split()) > 1:
            gsp_name_lcase = gsp_name_lcase.split()
            gsp_name_lcase = seperator.join(gsp_name_lcase)

        # Setting the gsp name in the dashboard  
        grafana.set_gsp_name_in_dashboard(gsp_name = gsp_name)
        # Scroll to the panel
        grafana.scroll_to_element_and_click()
        # Download the data
        status = grafana.download_from_side_panel(close_browser = True)

        if status is None:
            continue
        else:
            # Get the file and renaming to the gsp name
            file_type = "/*.csv"
            files = glob(download_directory+file_type)
            data_file = max(files, key = os.path.getctime)
            if os.path.isfile(data_file):
                new_filename = os.path.join(download_directory, (gsp_name_lcase+'.csv'))
                # Remove the file if it already exists
                if os.path.isfile(new_filename):
                    os.remove(new_filename)
                os.rename(data_file, new_filename)
            else:
                logger.info("The file did not get downloaded")

if __name__ == "__main__":
    download_directory = "/home/vardh/ocf/pv-solar-farm-forecasting/tests/data/grafana_dashboard_ukpn"
    gsp_name = "WARLEY"
    gsp_names = get_gsp_names()
    download_solar_data(
        download_directory = download_directory,
        gsp_names_list = gsp_names
    )