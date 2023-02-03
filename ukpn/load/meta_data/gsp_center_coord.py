"""Datapipe to extract the meta data for each GSP"""
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union
from pprint import pprint

from shapely.geometry import Polygon
from torchdata.datapipes import functional_datapipe
from torchdata.datapipes.iter import IterDataPipe

from ukpn.load.meta_data.utils import (
    construct_url, 
    get_metadata_from_ukpn_api,
    get_gsp_names)

logger = logging.getLogger(__name__)


@functional_datapipe("get_center_coordinates_gsp")
class GetCenterCoordinatesGSPIterDataPipe(IterDataPipe):
    """This Data pipe gives a dictionary of a GSP locations"""

    def __init__(
        self,
        folder_destination:str = None,
        refine_facet: List = None, 
        refine_facet_values: List = None):
        """Construct the url and derive JSON data
        
        Args:
            folder_destination: Folder that contains GSP csv files
            refiner_facet: List of refiners that needs to be included in the JSON data
            refine_facet_values: List of refine values of the refiners
        """

        # Declaring the variables
        self.folder_destination = folder_destination
        self.refine_facet = refine_facet
        self.refine_facet_values = refine_facet_values

    def __iter__(self):
        """Getting the geom center of the coordinates"""
        # Getting the refine_facet and refine_facet_values
        self.refine_facet = ["grid_supply_point"]
        ukpn_gsp_names = get_gsp_names(
            folder_destination = self.folder_destination
        )
        # Iterating through each_gsp
        gsp_coords = {}
        for _,gsp_name in ukpn_gsp_names.items():

            # Getting the gsp_names
            # Constructing the url
            api_url = construct_url(
                refine_facet = self.refine_facet,
                refine_facet_values = list(gsp_name)
            )
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
            gsp_coords[gsp_name] = gsp_center
        pprint(gsp_coords)
        return gsp_coords
