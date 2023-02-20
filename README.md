# PV Solar Farm Forecasting

Forecasting for individual solar farms

# Description

This repository consists of Pytorch `datapipes` and functions to automate the download, configure and pre-process of the meta-data and PVLive data from the [`UKPN`](https://www.ukpowernetworks.co.uk/)(UK Power Networks). `UKPN` covers London, South East and East of England. Please click [here](https://www.ukpowernetworks.co.uk/about-us/areas-we-cover) to see the map of `UKPN` coverage. `UKPN` GSP (Grid Supply Point) meta-data is acquired from their ECR (Embedded Capacity Register) [data catalogue](https://ukpowernetworks.opendatasoft.com/explore/dataset/embedded-capacity-register/information/?disjunctive.licence_area). Along with ECR, various other types of meta-data also can be [downloaded](https://ukpowernetworks.opendatasoft.com/explore/?disjunctive.theme&disjunctive.keyword&sort=explore.popularity_score) manually. The meta-data download is automated through scripts, you can see the scripts if you follow the path below.

## Grafana data download

`UKPN` provides their live data through a dashboard(please click the link [here](https://dsodashboard.ukpowernetworks.co.uk/) to open the dashboard) the open-source data visualization tool called [Grafana](https://grafana.com/). The visualization tool offers to categorize, filter, and visualize the data as the user desire. It also provides an option to download the live data for their given GSPs. Follow this [link](https://innovation.ukpowernetworks.co.uk/wp-content/uploads/2021/02/DSO-Dashboard-guide-February-2021.pdf) to get the guide to use the dashboard.

.
└── pv-solar-farm-forecasting/
    ├── grafana/
    │   └── .......
    │   └── .......        
    ├── ukpn/
    │   └── load
    │      └── meta_data/
    │      └── power_data/     

