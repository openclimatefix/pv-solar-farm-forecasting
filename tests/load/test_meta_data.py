from typing import Dict

import requests

from ukpn.load import (
    GetCenterCoordinatesGSP,
    construct_url,
    get_gsp_names,
    get_metadata_from_ukpn_api,
)


def test_metadata_api():
    # Testing if the constructed url is callable
    url = construct_url(get_complete_records=True)
    # Testing url resposne
    url_resposne = requests.get(url)

    assert url_resposne.status_code == 200


def test_get_url_gsp_names():
    # Testing the url api resposne for each GSP location
    gsp_names = get_gsp_names()
    for gsp_name in gsp_names:
        gsp_name = gsp_name.split(" ")
        gsp_name = "+".join(gsp_name)
        api_url = construct_url(gsp_names=gsp_name)

        url_resposne = requests.get(api_url)

        assert url_resposne.status_code == 200


def test_coords_from_csv_files():
    # Testing to check
    # Testing for all files
    folder_destination = "tests/data"
    data = GetCenterCoordinatesGSP(folder_destination=folder_destination)
    data = next(iter(data))

    assert data is not None


def test_get_all_the_records():
    # Testing to get the entire UKPN ECR (Embedded Capacity Register) dataset
    api_url = construct_url(get_complete_records=True)
    data = get_metadata_from_ukpn_api(api_url=api_url)
    if isinstance(data, Dict):
        total_records = data["nhits"]
        # Total GSP records including PV Solar output, wind, biofuel etc.
        assert total_records == 1040
    else:
        return AssertionError

    assert data is not None


def test_get_gsp_names():
    # Testing to ge the gsp names
    gsp_names = get_gsp_names()
    assert gsp_names is not None
