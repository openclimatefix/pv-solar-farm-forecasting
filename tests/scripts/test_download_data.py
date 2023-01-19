from pathlib import Path
from pprint import pprint

from ukpn.scripts import (
    construct_url,
    get_metadata_from_ukpn_api,
    get_metadata_from_ukpn_xlsx,
    metadata_df_to_netcdf,
)


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
    data = get_metadata_from_ukpn_api(api_url=url, eastings="615378", northings="165525")


def test_metadata_from_xlsx():
    url = "https://media.umbraco.io/uk-power-networks/0dqjxaho/embedded-capacity-register.xlsx"
    test_path = "/home/raj/ocf/pv-solar-farm-forecasting/tests/data/test.csv"
    local_path = Path(r"/home/raj/ocf/pv-solar-farm-forecasting/tests/data")
    df = get_metadata_from_ukpn_xlsx(
        link_of_ecr_excel=url, local_path=local_path, eastings="615378", northings="165525"
    )
    ncxr = metadata_df_to_netcdf(path_to_ukpn_timeseries=test_path)
