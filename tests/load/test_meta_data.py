from pprint import pprint
from typing import List, Dict

import requests

from ukpn.load import (
    GetCenterCoordinatesGSP,
    construct_url,
    get_metadata_from_ukpn_api,
    get_gsp_names,
)


def test_metadata_api():
    # Testing if the constructed url is callable
    url = construct_url(get_complete_records = True)
    # Testing url resposne
    url_resposne = requests.get(url)

    assert url_resposne.status_code == 200

# def test_get_url_gsp_names():
#     gsp_names = get_gsp_names()
#     for gsp_name in gsp_names:
#         gsp_name = gsp_name.split(' ')
#         gsp_name = '+'.join(gsp_name)
#         api_url = construct_url(gsp_names = gsp_name)

#         url_resposne = requests.get(api_url)

#         assert url_resposne.status_code == 200


def test_coords_from_csv_files():
    # Testing for all files
    folder_destination = "/home/raj/ocf/pv-solar-farm-forecasting/tests/local_data/ukpn_dashboard_data"
    data = GetCenterCoordinatesGSP(folder_destination = folder_destination)
    data = next(iter(data))
    assert data is not None

# def test_get_all_the_records():
#     # Testing to get the entire ECR dataset
#     api_url = construct_url()
#     data = get_metadata_from_ukpn_api(api_url = api_url)
#     if isinstance(data, Dict):
#         total_records = data["nhits"]
#         # Total GSP records with PV Solar output
#         assert total_records == 419
#     else:
#         return AssertionError

#     assert data is not None

# def test_get_gsp_names():
#     # Testing to get the GSP names from UKPN ECR
#     folder_destimation = "/home/raj/ocf/pv-solar-farm-forecasting/tests/local_data/ukpn_dashboard_data"
#     data = get_gsp_names(folder_destination = folder_destimation)
#     assert data is not None

# def test_get_gsp_coords():
#     # Testing to get the coords for GSPs
#     folder_destimation = "/home/raj/ocf/pv-solar-farm-forecasting/tests/local_data/ukpn_dashboard_data"
#     data = GetCenterCoordinatesGSP(
#         folder_destination = folder_destimation
#     )
#     data = next(iter(data))



