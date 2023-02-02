"""DataPipe to get the names of the GSPs"""
import logging
import os
import glob
from typing import Union
from pathlib import Path

from ukpn.load.meta_data.utils import(
    construct_url,
    get_metadata_from_ukpn_api
)

from torchdata.datapipes import functional_datapipe
from torchdata.datapipes.iter import IterDataPipe

logger = logging.getLogger(__name__)

@functional_datapipe("get_gsp_names")
class GetGSPNamesIterDataPipe(IterDataPipe):
    """This method extracts GSP names from UKPN dashboard"""
    
    def __init__(
        self,
        folder_destination: Union[Path, str]):
        """
        This methods takes all the csv file names and gives their
        respective GSP names from the UKPN dashboard
        
        Args:
            folder_destination: The destination folder that has all the csv files
        """
        # Declaring variables
        self.folder_destination = folder_destination
    
    def __iter__(self):
        
        pass