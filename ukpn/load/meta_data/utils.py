"""This class is ued to retrieve data through API calls"""
import json
import logging
from typing import Dict, Optional

import requests

logger = logging.getLogger(__name__)

FACETS = [
    "grid_supply_point",
    "licence_area",
    "energy_conversion_technology_1",
    "flexible_connection_yes_no",
    "connection_status",
    "primary_resource_type_group",
]

REFINE_FACETS = ["energy_conversion_technology_1", "grid_supply_point"]


def get_metadata_from_ukpn_api(api_url: str):
    """Function to get the metadata from url api call

    This function retrievs metadata through api calls
    from the constructed url below

    Args:
        api_url: The api url link that emiits json format data
    """

    response_api = requests.head(api_url)
    if not response_api.status_code == 200:
        logger.info(f"The response from the link {api_url} is unsuccessful")
        return None
    else:
        logger.info(f"The resposne from the link {api_url} is successful")

        # Get the data from the resposne
        response_api = requests.get(api_url)
        raw_data = response_api.text

        # Parse the data into json format
        data_json = json.loads(raw_data)
        return data_json


def construct_url(
    dataset_name: str = "embedded-capacity-register",
    gsp_names: str = None,
    number_of_records: str = "5000",
    get_complete_records: Optional[bool] = False,
):
    """This function constructs a downloadable url of UKPN PV JSON data

    For more information, please visit
    - https://ukpowernetworks.opendatasoft.com/pages/home/

    Args:
        dataset_name: Name of the dataset that needs to be downloaded, defined by UKPN
        gsp_names: The data needed for the GSPs
        number_of_records: Number of records needed to be extracted
        get_complete_records: If yes, gets the link to extract entire ukpn api records

    Retunrs:
        final_url:
            Base url:
            <https://ukpowernetworks.opendatasoft.com/api/records/1.0/search/?dataset=embedded-capacity-register&q=>

            facets_str:
            <&facet=grid_supply_point&facet=licence_area>
            <&facet=energy_conversion_technology_1>
            <&facet=flexible_connection_yes_no>
            <&facet=connection_status>
            <&facet=primary_resource_type_group>

            refiners:
            <&refine.energy_conversion_technology_1=Photovoltaic>
            <&refine.grid_supply_point=CANTERBURY+NORTH> # Syntax GSP name
    """
    REFINE_FACET_VARIABLES = ["Photovoltaic"]

    # Constructing a base url
    base_url = "https://ukpowernetworks.opendatasoft.com/api/records/1.0/search/?dataset="
    base_url = base_url + dataset_name

    # A seperator in the url
    seperator = "&"

    # A questionare in the url
    questionare = "q="

    # Number of records needed to be extracted
    total_rows = str("&rows=" + number_of_records)

    # A facet questionare in the url
    facet_questionare = "facet="

    # Constructing a facet string from the list of facets
    facet_str = [facet_questionare + x for x in FACETS]
    facet_str = seperator.join(facet_str)
    facet_str = str(questionare + total_rows + seperator + facet_str)

    # Get the entire records
    if get_complete_records:
        final_url = [base_url, facet_str]
        final_url = seperator.join(final_url)
        return final_url
    else:
        # Adding gsp name to the list
        REFINE_FACET_VARIABLES.append(gsp_names)

        # Sanity checs
        sanity_check = len(REFINE_FACETS) == len(REFINE_FACET_VARIABLES)
        if not sanity_check:
            logger.info("The URL will be invalid")
            logger.debug(f"total {REFINE_FACETS} should be equal to {REFINE_FACET_VARIABLES}")
            return None

        refine_questionare = "refine."
        refine_facets = [refine_questionare + x for x in REFINE_FACETS]
        refiners = list(map(lambda x, y: x + str("=") + y, refine_facets, REFINE_FACET_VARIABLES))
        refiners = seperator.join(refiners)

        # Getting the entire UKPN records
        final_url = [base_url, facet_str, refiners]
        final_url = seperator.join(final_url)

        return final_url


def get_gsp_names():
    """This function extracts all the Syntaxed GSP names from the api

    Returns:
        ['BRAMFORD GRID 132kV',
        'WALPOLE GIS 132KV',
        'NORWICH MAIN 132kV',
        'SUNDON 132kV',
        'RAYLEIGH MAIN 132KV'
        ...]
    """
    # Getting all the records
    api_url = construct_url(get_complete_records=True)
    data_json = get_metadata_from_ukpn_api(api_url=api_url)

    # Getting all the gsp_names
    if isinstance(data_json, Dict):
        gsp_facet_group = data_json["facet_groups"]
    else:
        return None

    # Getting the Grid supply point group
    for group in gsp_facet_group:
        if group["name"] == "grid_supply_point":
            gsp_group = group["facets"]

    # Getting the GSP names
    gsp_names = []
    for each_gsp in gsp_group:
        gsp_names.append(each_gsp["name"])
    return gsp_names
