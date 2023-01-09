from ukpn.scripts import get_metadata


def test_download_metadata():
    cantubry_api_url = "https://ukpowernetworks.opendatasoft.com/api/records/1.0/search/?dataset=embedded-capacity-register&q=&facet=grid_supply_point&facet=licence_area&facet=energy_conversion_technology_1&facet=flexible_connection_yes_no&facet=connection_status&facet=primary_resource_type_group&refine.grid_supply_point=CANTERBURY+NORTH&refine.energy_conversion_technology_1=Photovoltaic"
    download = get_metadata(api_url=cantubry_api_url, print_data=True)
