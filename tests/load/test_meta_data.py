import requests

from ukpn.load import construct_url, get_metadata_from_ukpn_api, get_metadata_from_ukpn_xlsx


def test_metadata_api():
    # Testing if the constructed url is callable
    refiners = ["grid_supply_point"]
    refine_values = ["canterbury north"]

    url = construct_url(refiners=refiners, refine_values=refine_values)

    # Testing url resposne
    url_resposne = requests.get(url)

    assert url_resposne.status_code == 200
