import logging
import os
from glob import glob

from ukpn import DownloadGrafanaData, automate_csv_download, get_gsp_names, set_csv_filenames

logger_webdriver = logging.getLogger("selenium.webdriver.remote.remote_connection")
logger_webdriver.setLevel(logging.WARNING)

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s : %(levelname)s : %(message)s ")
logger = logging.getLogger(__name__)


def test_get_gsp_names():
    """Testing to get gsp names from the dashboard"""
    gsp_names = get_gsp_names()
    assert gsp_names is not None


def test_automatic_download_one_gsp_data():
    """Testing automatic download of single gsp
    which has Solar data"""
    download_dir = "/home/vardh/ocf/pv-solar-farm-forecasting/tests/data/grafana_dashboard_ukpn"
    gsp_name = "CANTERBURY NORTH"
    data = DownloadGrafanaData(move_to_dir=download_dir, gsp_name=gsp_name)
    status = next(iter(data))
    # If downloaded, status will be one
    assert status == 1


def test_automatic_download_non_solar():
    """Testing download of GSP which does
    not have Solar data, but other data"""
    download_directory = (
        "/home/vardh/ocf/pv-solar-farm-forecasting/tests/data/grafana_dashboard_ukpn"
    )
    gsp_name = "WARLEY"
    data = DownloadGrafanaData(move_to_dir=download_directory, gsp_name=gsp_name)
    status = next(iter(data))
    # If not downloaded, status will be None
    assert status is None


def test_automatic_download_all_GSPs():
    """Testing download of all GSP which has
    Solar data"""
    gsp_names = list(reversed(get_gsp_names()))
    download_directory = (
        "/home/vardh/ocf/pv-solar-farm-forecasting/tests/data/grafana_dashboard_ukpn"
    )
    for gsp_name in gsp_names:
        data = DownloadGrafanaData(move_to_dir=download_directory, gsp_name=gsp_name)
        status = next(iter(data))

        # If status is None, there is no data downloaded, meaning GSP does not have Solar data
        if status is not None:
            file_path = os.path.join(download_directory, "*")
            latest_download = max(glob(file_path), key=os.path.getctime)
            latest_download_basename = os.path.basename(latest_download)
            latest_download_fname = os.path.splitext(latest_download_basename)[0]
            if len(latest_download_fname.split("_")) > 1:
                # Checking the download file name matches with GSP name
                assert latest_download_fname.split("_")[0] in gsp_name.lower()
            else:
                assert latest_download_fname == gsp_name.lower()
