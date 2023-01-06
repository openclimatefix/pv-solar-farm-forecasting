"""This class is ued to retrieve data through API calls"""
import json
import logging
from pprint import pprint

import requests

logger = logging.getLogger(__name__)


class DownloadMetadata:
    """Downloading the metadata using api requests"""

    def __init__(self, api_url: str, print_data: bool = False) -> None:
        """
        This function retrievs metadata through api calls

        Args:
            api_url: The api url link that emiits json format data
            print_data: Optional to choose printing the data
        """

        self.api_url = api_url
        self.print_data = print_data

        self.response_api = requests.get(self.api_url)
        while True:
            if self.response_api == 200:
                logger.info(f"The api resposne {self.response_api} is successful")
            else:
                logger.warning(f"The api resposne {self.response_api} is unsuccessul")
                logger.info(f"Please enter the correct {'url'}")
                break

    def get_data(self) -> None:
        """Loads the data into the JSON format"""

        # Get the data from the resposne
        self.raw_data = self.response_api.text

        # Parse the data into json format
        data_json = json.loads(self.raw_data)
        data_first_record = data_json["records"][0]

        if self.print_data:
            pprint(data_first_record)
