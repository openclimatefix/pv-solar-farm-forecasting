import logging

from ukpn import DownloadGrafanaData, main_panel, open_webpage

logger_webdriver = logging.getLogger("selenium.webdriver.remote.remote_connection")
logger_webdriver.setLevel(logging.WARNING)

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s : %(levelname)s : %(message)s ")
logger = logging.getLogger(__name__)


def test_open_webpage():
    """Testing if the webpage has been opened successfully"""
    grafana = open_webpage()
    status_load = grafana.Initialise_chrome()
    status_close = grafana.close_or_refresh(close_browser=True)
    assert status_load and status_close == 1


def test_get_all_gsp_names():
    """Testing to retreive all GSP names"""
    grafana = main_panel()
    grafana.Initialise_chrome()
    gsp_names = grafana.get_gsp_names_from_dashbaord()
    grafana.close_or_refresh(close_browser=True)
    for gsp in gsp_names:
        # All the GSPS
        assert gsp.isupper() is True


def test_non_solar_gsp():
    """Testing automatic download of single gsp
    which does not have Solar data"""
    gsp_name = "LODGE ROAD"
    data = DownloadGrafanaData(gsp_name=gsp_name)
    status = next(iter(data))
    # If false, there is no data to be downloaded
    assert all(element == status[0] for element in status) == False


def test_automatic_download_solar_gsp():
    download_directory = "/home/vardh/ocf/pv-solar-farm-forecasting/tests/data"
    gsp_name = "SELLINDGE"
    data = DownloadGrafanaData(gsp_name=gsp_name, new_directory=download_directory)
    status = next(iter(data))
    # If True, data is present and downloaded
    assert all(element == status[0] for element in status) == True
