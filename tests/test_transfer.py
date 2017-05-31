import pytest

from boxcomtools.base.transfer_client import BoxToSmartsheet
from boxcomtools.box.client import Client as BoxClient
from boxcomtools.smartsheet.client import Client as SmartsheetClient

from .utils import * 

@pytest.mark.gen_test
def text_box_to_smartsheet_transfer():

    #  set up clients
    box_cli = BoxCLient()
    
    btm = BoxToSmartsheet()
