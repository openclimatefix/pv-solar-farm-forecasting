"""Datapipes"""
from ukpn.grafana.chrome import open_webpage
from ukpn.grafana.grafana import DownloadGrafanaDataIterDataPipe as DownloadGrafanaData
from ukpn.grafana.grafana import get_gsp_names, set_csv_filenames
from ukpn.grafana.grafana_data_download import automate_csv_download
from ukpn.grafana.grafana_main_panel import main_panel
import ukpn.load
