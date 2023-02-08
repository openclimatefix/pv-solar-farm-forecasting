from ukpn.load import automate_csv_download

def test_grafana_dashboard():
    download_directory = "/home/vardh/ocf/pv-solar-farm-forecasting/tests/local_data"
    grafana = automate_csv_download(
        download_directory = download_directory
    )
    grafana.set_gsp_name_in_dashboard(gsp_name = "RAYLEIGH")