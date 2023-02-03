"""Datapipe to extract the meta data for each GSP"""
import logging
import os
from glob import glob
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
        file_format: str = "*.csv"):
        """Construct the url and derive JSON data
        
        Args:
            folder_destination: Folder that contains GSP csv files
        """
        # Getting the file paths
        file_paths = os.path.join(folder_destination, file_format)
        file_paths = [x for x in glob(file_paths)]
        
        # Get all the gsp names
        gsp_names = get_gsp_names()
        self.gsp_name_dict = {}
        for file_path in file_paths:
            base_name = os.path.basename(file_path)
            file_name = os.path.splitext(base_name)[0]
            i = 0
            while i < len(gsp_names):
                if file_name.upper() in gsp_names[i]:
                    # Joining with + seperator
                    gsp_name = gsp_names[i].split(' ')
                    gsp_name = '+'.join(gsp_name)
                    self.gsp_name_dict[file_name] = gsp_name
                i+=1              

    def __iter__(self):
        """Getting the geom center of the coordinates"""

        # Iterating through each_gsp
        gsp_center_coords = {}
        for file_name ,gsp_name in self.gsp_name_dict.items():

            # Constructing the url
            api_url = construct_url(gsp_names = gsp_name)
            # Getting the data
            data_json = get_metadata_from_ukpn_api(api_url=api_url)

            # Getting the records
            data_records = data_json["records"]

            # Getting the coordinates
            coords_list = []
            for item in data_records:
                if isinstance(item, Dict):
                    try:
                        coordinates = item["geometry"]["coordinates"]
                    except KeyError:
                        pass
                    else:
                        if coordinates is None:
                            pass
                        else:
                            coords_list.append(coordinates)
            try:
                polygon_geom = Polygon(coords_list)
            except ValueError:
                pass
            else:
                gsp_center = list(polygon_geom.centroid.coords)
                gsp_center_coords[file_name] = gsp_center

        yield gsp_center_coords
