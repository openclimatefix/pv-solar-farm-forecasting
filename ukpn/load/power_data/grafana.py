from grafana_data_download import automate_csv_download
import os
import glob

def gsp_names():
    """FUnction to get all the GSP names from dashboard"""
    grafana = automate_csv_download()
    grafana.Initialise_chrome()
    names = grafana.get_gsp_names_in_dashbaord()
    return names