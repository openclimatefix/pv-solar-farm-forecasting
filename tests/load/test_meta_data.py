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
    refiners = ["grid_supply_point"]
    refine_values = ["canterbury north"]

    url = construct_url(
        refine_facet = refiners, 
        refine_facet_values = refine_values)

    # Testing url resposne
    url_resposne = requests.get(url)

    assert url_resposne.status_code == 200


def test_json_data_from_url():
    # Constructin the url
    refiners = ["grid_supply_point", "energy_conversion_technology_1"]
    refine_values = ["canterbury north", "Photovoltaic"]

    data = GetCenterCoordinatesGSP(
        refine_facet = refiners, 
        refine_facet_values = refine_values)
    data = iter(data)

    assert data is not None

def test_get_all_the_records():
    # Testing to get the entire ECR dataset
    api_url = construct_url()
    data = get_metadata_from_ukpn_api(api_url = api_url)
    if isinstance(data, Dict):
        total_records = data["nhits"]
        # Total GSP records with PV Solar output
        assert total_records == 419
    else:
        return AssertionError

    assert data is not None

def test_get_gsp_names():
    # Testing to get the GSP names from UKPN ECR
    folder_destimation = "/home/raj/ocf/pv-solar-farm-forecasting/tests/local_data/ukpn_dashboard_data"
    data = get_gsp_names(folder_destination = folder_destimation)
    pprint(data)
    assert data is not None
