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
