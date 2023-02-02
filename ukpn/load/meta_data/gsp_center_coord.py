"""Datapipe to extract the meta data for each GSP"""
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union

from shapely.geometry import Polygon
from torchdata.datapipes import functional_datapipe
from torchdata.datapipes.iter import IterDataPipe

from ukpn.load.meta_data.utils import construct_url, get_metadata_from_ukpn_api

logger = logging.getLogger(__name__)


@functional_datapipe("get_center_coordinates_gsp")
class GetCenterCoordinatesGSPIterDataPipe(IterDataPipe):
    """This Data pipe gives a dictionary of a GSP locations"""

    def __init__(
        self,
        refine_facet: List = None, 
        refine_facet_values: List = None):
        """Construct the url and derive JSON data
        
        Args:
            folder_destination: Folder that contains GSP csv files
            refiner_facet: List of refiners that needs to be included in the JSON data
            refine_facet_values: List of refine values of the refiners
        """

        # Declaring the variables
        self.refiners = refine_facet
        self.refine_facet_values = refine_facet_values

    def __iter__(self):
        """Getting the Geom center of the coordinates"""
        # Constructing the url
        api_url = construct_url(
            refine_facet = self.refiners, 
            refine_facet_values=self.refine_facet_values)
        # Getting the data
        data_json = get_metadata_from_ukpn_api(api_url=api_url)

        # Getting the records
        data_records = data_json["records"]

        # Getting the coordinates
        coords_list = []
        for item in data_records:
            if isinstance(item, Dict):
                coordinates = item["geometry"]["coordinates"]
                coords_list.append(coordinates)
        polygon_geom = Polygon(coords_list)
        gsp_center = list(polygon_geom.centroid.coords)

        return gsp_center
