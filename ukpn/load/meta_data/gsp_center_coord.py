"""Datapipe to extract the meta data for each GSP"""
import logging
from pathlib import Path
from typing import Optional, Union, List, Dict
from shapely.geometry import Polygon
from ukpn.load.meta_data.utils import (
    construct_url,
    get_metadata_from_ukpn_api)

from torchdata.datapipes import functional_datapipe
from torchdata.datapipes.iter import IterDataPipe

logger = logging.getLogger(__name__)
@functional_datapipe("get_center_coordinates_gsp")
class GetCenterCoordinatesGSPIterDataPipe(IterDataPipe):
    """This Data pipe gives a dictionary of a GSP locations"""

    def __init__(
        self,
        refiners: List = None,
        refine_values: List = None):
        """Construct the url and derive JSON data"""

        # Declaring the variables
        self.refiners = refiners
        self.refine_values = refine_values
    
    def __iter__(self):
        """Getting the Geom center of the coordinates"""
        # Constructing the url
        api_url = construct_url(
            refiners = self.refiners,
            refine_values = self.refine_values)
        # Getting the data
        data_records = get_metadata_from_ukpn_api(api_url = api_url)

        # Getting the coordinates
        coords_list = []
        for item in data_records:
            if isinstance(item, Dict):
                coordinates = item['geometry']['coordinates']
                coords_list.append(coordinates)
        polygon_geom = Polygon(coords_list)
        gsp_center = list(polygon_geom.centroid.coords)
        
        return gsp_center
