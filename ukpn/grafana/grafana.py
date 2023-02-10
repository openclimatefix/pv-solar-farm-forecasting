import os
from glob import glob
import logging
from typing import List

from ukpn.grafana.grafana_data_download import automate_csv_download
from torchdata.datapipes import functional_datapipe
from torchdata.datapipes.iter import IterDataPipe

logger = logging.getLogger(__name__)

@functional_datapipe("download_grafana_data")
class DownloadGrafanaDataIterDataPipe(IterDataPipe):
    """Automatically download data drom UKPN grafana dashboard

    For reference, please open this link of the dasboard panel
    URL - https://dsodashboard.ukpowernetworks.co.uk/
    """
    def __init__(
        self,
        download_directory: str,
        gsp_name: str = None):
        """Set the download directory
        
        Args:
            download_directory: Set the folder destination for downloads
        """
        self.download_directory = download_directory
        self.gsp_name = gsp_name

    def __iter__(self):
        """Downloading the data for each gsp"""
        if self.gsp_name is None:
            # Getting the list of gsp names
            gsp_names_list = get_gsp_names()
            gsp_names_list = list(reversed(gsp_names_list))   
        else:
            gsp_names_list = [self.gsp_name]

        for gsp_name in gsp_names_list:

            # Initalise chrome
            grafana = automate_csv_download(
                download_directory = self.download_directory)
            grafana.Initialise_chrome()

            # Getting the gsp names in lower case format
            # In order to reqrite saved csv file names
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
                yield status
                
            else:
                filepath = set_csv_filenames(
                    download_directory = self.download_directory,
                    gsp_name = gsp_name_lcase)
                yield status

def get_gsp_names():
    """Function to get all the GSP names from dashboard"""

    logger.info("Browser opened to get GSP names")
    grafana = automate_csv_download()
    grafana.Initialise_chrome()
    names = grafana.get_gsp_names_from_dashbaord()
    assert names is not None
    return names

def set_csv_filenames(
    download_directory: str,
    gsp_name:str):
    """Function to rewrite the csv file name
    
    Args:
        download_directory: The download directory for the downloads
        gsp_name: Each GSP name of the UKPN dashboard
    """

    # Get the file and renaming to the gsp name
    file_type = "/*.csv"
    files = glob(download_directory+file_type)
    data_file = max(files, key = os.path.getctime)
    if os.path.isfile(data_file):
        new_filename = os.path.join(download_directory, (gsp_name+'.csv'))
        # Remove the file if it already exists
        if os.path.isfile(new_filename):
            os.remove(new_filename)
        filepath = os.rename(data_file, new_filename)
        return filepath
    else:
        logger.info(f"The filepath {filepath} doesnot exist!")
        return None
    
