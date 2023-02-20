"""Datapipe to downalod UKPN GSP Solar data"""
import logging
import os
import shutil
from glob import glob
from typing import Optional

from torchdata.datapipes import functional_datapipe
from torchdata.datapipes.iter import IterDataPipe

from ukpn.grafana.grafana_side_panel import download_data

logger = logging.getLogger(__name__)


@functional_datapipe("download_grafana_data")
class DownloadGrafanaDataIterDataPipe(IterDataPipe):
    """Automatically download data drom UKPN grafana dashboard

    For reference, please open this link of the dasboard panel
    URL - https://dsodashboard.ukpowernetworks.co.uk/
    """

    def __init__(
        self,
        download_directory: str = os.getcwd(),
        new_directory: str = None,
        required_data: str = "Solar",
        gsp_name: str = None,
        commence_download: Optional[bool] = False,
    ):
        """Set the download directory

        Args:
            download_directory: Set the folder destination for downloads
            new_directory: Move files from main project folder to 'test/data'
            required_data: The data that is required to download
            gsp_name: Download for a single GSP, if None, downloads for all available GSP's
            commence_download: Download the data
        """
        self.download_directory = download_directory
        self.new_directory = new_directory
        self.required_data = required_data
        self.gsp_name = gsp_name
        self.commence_download = commence_download

    def __iter__(self):
        """Downloading the data for each gsp"""
        if self.gsp_name is None:
            # Getting the list of gsp names
            gsp_names_list = get_gsp_names()
            gsp_names_list = list(reversed(gsp_names_list))
            logger.debug(f"{gsp_names_list[-1]} GSP is not able be selected!")
            logger.debug("The problem is with the dashboard, not the code")
        else:
            gsp_names_list = [self.gsp_name]

        # Initalise chrome
        grafana = download_data(download_directory=self.download_directory)
        grafana.Initialise_chrome()
        status = []
        for gsp_name in gsp_names_list:
            # Getting the gsp names in lower case format
            # In order to reqrite saved csv file names
            seperator = "_"
            gsp_name_lcase = gsp_name.lower()
            if len(gsp_name_lcase.split()) > 1:
                gsp_name_lcase = gsp_name_lcase.split()
                gsp_name_lcase = seperator.join(gsp_name_lcase)

            # Workflow
            status.append(grafana.click_on_gsp_box())
            status.append(grafana.search_for_dropdown())
            status.append(grafana.select_a_gsp(gsp_name=self.gsp_name))
            status.append(grafana.scroll_to_element_and_click())
            status.append(grafana.click_dataoptions_side_panel())
            status.append(grafana.click_on_data_dialog())
            status.append(grafana.check_and_download_data())

            if self.commence_download:
                if all(element == status[0] for element in status):
                    set_csv_filenames(
                        download_directory=self.download_directory,
                        new_directory=self.new_directory,
                        gsp_name=gsp_name_lcase,
                    )
            if gsp_name == gsp_names_list[-1]:
                grafana.close_browser()
            yield status


def get_gsp_names():
    """Function to get all the GSP names from dashboard"""

    logger.info("Browser opened to get GSP names")
    grafana = download_data()
    grafana.Initialise_chrome()
    names = grafana.get_gsp_names_from_dashbaord()
    assert names is not None
    return names


def set_csv_filenames(download_directory: str, new_directory: str, gsp_name: str):
    """Function to rewrite the csv file name

    Args:
        download_directory: The download directory for the downloads
        new_directory: Move files from main folder to 'tests/data' folder
        gsp_name: Each GSP name of the UKPN dashboard
    """

    # Get the file and renaming to the gsp name
    file_type = "/*.csv"
    files = glob(download_directory + file_type)
    data_file = max(files, key=os.path.getctime)
    if os.path.isfile(data_file):
        new_filename = os.path.join(download_directory, (gsp_name + ".csv"))
        new_location = os.path.join(new_directory, (gsp_name + ".csv"))
        # Remove the file if it already exists
        if os.path.isfile(new_filename):
            os.remove(new_filename)
        if os.path.isfile(new_location):
            os.remove(new_location)
        filepath = os.rename(data_file, new_filename)
        shutil.move(new_filename, new_location)
        return filepath
    else:
        logger.info(f"The filepath {filepath} does not exist!")
        return None
