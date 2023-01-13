"""This class is ued to retrieve data through API calls"""
import json
import logging
from pprint import pprint

import requests

logger = logging.getLogger(__name__)


def get_metadata(api_url: str, print_data: bool = False):
    """
    This function retrievs metadata through api calls

    Args:
        api_url: The api url link that emiits json format data
        print_data: Optional to choose printing the data
    """

    response_api = requests.get(api_url)
    while True:
        if response_api == 200:
            logger.info(f"The api resposne {response_api} is successful")
        else:
            logger.warning(f"The api resposne {response_api} is unsuccessul")
            logger.info(f"Please enter the correct {'url'}")
            break

    # Get the data from the resposne
    raw_data = response_api.text

    # Parse the data into json format
    data_json = json.loads(raw_data)
    data_first_record = data_json["records"][0]

    if print_data:
        pprint(data_first_record)


def construct_url(
    dataset_name: str = "embedded-capacity-register",
    list_of_facets=None,
    refiners=None,
    refine_values=None,
):
    """This function constructs a downloadble url of JSON data

    For more information, please visit
    - https://ukpowernetworks.opendatasoft.com/pages/home/

    Args:
        dataset_name: Name of the dataset that needs to be downloaded, defined by UKPN
        list_of_facets: List of facets that needs to be included in the JSON data
        refiners: list of refiner terms that needs to refined from the JSON data
        refine_values: List of refine values of the refiners

    Note:
        refiners and refine values needs to be exactly mapped
    """
    # Constructing a base url
    base_url = "https://ukpowernetworks.opendatasoft.com/api/records/1.0/search/?dataset="
    base_url = base_url + dataset_name

    # A seperator in the url
    seperator = "&"

    # A questionare in the url
    questionare = "q="

    # A facet questionare in the url
    facet_questionare = "facet="

    # Constructing a facet string from the list of facets
    facet_str = [facet_questionare + x for x in list_of_facets]
    facet_str = seperator.join(facet_str)
    facet_str = str(questionare + seperator + facet_str)

    # Constructing a refiner string to refine the JSON data
    refine_questionare = "refine."
    refiners = [refine_questionare + x for x in refiners]
    refiners = list(map(lambda x, y: x + str("=") + y, refiners, refine_values))
    refiners = seperator.join(refiners)

    # Constructing the final url
    final_url = [base_url, facet_str, refiners]
    final_url = seperator.join(final_url)
    return final_url
