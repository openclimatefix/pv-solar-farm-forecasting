import requests
import json
from pprint import pprint
import logging

logger = logging.getLogger(__name__)

class DownloadMetadata():

    def __init__(
        self,
        api_url: str,
        print_data:bool = False) -> None:

        self.api_url = api_url
        self.print_data = print_data
        
        self.response_api = requests.get(self.api_url)
        while True:
            if self.response_api == 200:
                logger.info(f"The api resposne is successful")
            else:
                logger.warning(f"The api resposne is unsuccessul, please insert correct url")
                break
    
    def get_data(self)-> None:
             
        # Get the data from the resposne
        self.raw_data = self.response_api.text

        # Parse the data into json format
        data_json = json.loads(self.raw_data)
        data_first_record = data_json['records'][0]

        if self.print_data:
            pprint(data_first_record)