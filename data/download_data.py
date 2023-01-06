import requests
import json
from pprint import pprint
import logging

logger = logging.getLogger(__name__)

class download_metadata():

    def __init__(
        self,
        api_url: str) -> None:
        self.api_url = api_url
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
        pprint(data_first_record)

if __name__ == "__main__":
    cantubry_api_url = 'https://ukpowernetworks.opendatasoft.com/api/records/1.0/search/?dataset=embedded-capacity-register&q=&facet=grid_supply_point&facet=licence_area&facet=energy_conversion_technology_1&facet=flexible_connection_yes_no&facet=connection_status&facet=primary_resource_type_group&refine.grid_supply_point=CANTERBURY+NORTH&refine.energy_conversion_technology_1=Photovoltaic'
    download = download_metadata(api_url=cantubry_api_url)
    download.get_data()