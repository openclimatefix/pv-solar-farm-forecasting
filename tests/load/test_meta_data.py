import requests
from typing import List
from pprint import pprint
from ukpn.load import construct_url, get_metadata_from_ukpn_api, get_metadata_from_ukpn_xlsx
from ukpn.load import GetCenterCoordinatesGSP


def test_metadata_api():
    # Testing if the constructed url is callable
    refiners = ["grid_supply_point"]
    refine_values = ["canterbury north"]

    url = construct_url(refiners=refiners, refine_values=refine_values)

    # Testing url resposne
    url_resposne = requests.get(url)

    assert url_resposne.status_code == 200

def test_json_data_from_url():
    # Constructin the url
    refiners = ["grid_supply_point", "energy_conversion_technology_1"]
    refine_values = ["canterbury north", "Photovoltaic"]

    data = GetCenterCoordinatesGSP(
        refiners=refiners,
        refine_values=refine_values
    )
    data = iter(data)

    assert data is not None
