from ukpn.scripts import construct_url, get_metadata


def test_download_metadata():
    cantubry_api_url = "https://ukpowernetworks.opendatasoft.com/api/records/1.0/search/?dataset=embedded-capacity-register&q=&facet=grid_supply_point&facet=licence_area&facet=energy_conversion_technology_1&facet=flexible_connection_yes_no&facet=connection_status&facet=primary_resource_type_group&refine.grid_supply_point=CANTERBURY+NORTH&refine.energy_conversion_technology_1=Photovoltaic"
    download = get_metadata(api_url=cantubry_api_url, print_data=True)


def test_construct_url():
    url = construct_url(
        list_of_facets=[
            "grid_supply_point",
            "licence_area",
            "energy_conversion_technology_1",
            "flexible_connection_yes_no",
            "connection_status",
            "primary_resource_type_group",
        ],
        refiners=["grid_supply_point", "energy_conversion_technology_1"],
        refine_values=["CANTERBURY+NORTH", "Photovoltaic"],
    )
    search_url = get_metadata(api_url=url, print_data=True)
