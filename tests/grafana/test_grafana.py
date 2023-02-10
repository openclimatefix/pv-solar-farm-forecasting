import os
import logging

from ukpn import automate_csv_download
from ukpn import DownloadGrafanaData
from ukpn import get_gsp_names, set_csv_filenames

logger_webdriver = logging.getLogger('selenium.webdriver.remote.remote_connection')
logger_webdriver.setLevel(logging.WARNING)

logging.basicConfig(
    level=logging.DEBUG,
    format = '%(asctime)s : %(levelname)s : %(message)s ')
logger = logging.getLogger(__name__)

def test_get_gsp_names():
    """Testing to get gsp names from the dashboard"""
    gsp_names = get_gsp_names()
    assert gsp_names is not None

def test_automatic_download_one_gsp_data():
    """Testing automatic download of single gsp
    which has Solar data"""
    download_directory = "tests/data/grafana_dashboard_ukpn"
    gsp_name = "SELLINDGE"
    data = DownloadGrafanaData(
        download_directory = download_directory,
        gsp_name = gsp_name
    )
    status = next(iter(data))
    # If downloaded, status will be one
    assert status == 1

def test_automatic_download_non_solar():
    """Testing download of GSP which does
    not have Solar data, but other data"""
    download_directory = "tests/data/grafana_dashboard_ukpn"
    gsp_name = "WARLEY"
    data = DownloadGrafanaData(
        download_directory = download_directory,
        gsp_name = gsp_name
    )
    status = next(iter(data))
    # If not downloaded, status will be None
    assert status is None  
