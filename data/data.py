#script to load all data

import pandas as pd
import xarray as xr
import os

data_path = "example_github_data"
base_url = "https://raw.githubusercontent.com/OMS-NetZero/FAIR/master/tests/test_data"

df_climate = pd.read_csv(os.path.join(base_url, "4xCO2_cummins_ebm3.csv"))
df_climate.to_csv(os.path.join(data_path, 'climate_models_data.csv'))

df_volcanic = pd.read_csv(os.path.join(base_url, "volcanic_ERF_monthly_175001-201912.csv"), on_bad_lines='skip')
df_volcanic.to_csv(os.path.join(data_path, 'volcano_forcing_data.csv'))


# Net CDF files downloaded from github: https://github.com/OMS-NetZero/FAIR/tree/master/tests/test_data

emissions = xr.open_dataset(os.path.join(data_path, "ssp_co2_conc_2100.nc"))
forcing = xr.open_dataset(os.path.join(data_path, "ssp_run_forcing_2100.nc"))
temperature = xr.open_dataset(os.path.join(data_path, "ssp_run_temp_2100.nc"))
print(emissions.to_dataframe().head())




# save ssp scenarios in Fair 1.6.4 for use in fair 2.1
data_path = "fair_ssp_scenarios"
import requests
from bs4 import BeautifulSoup
from fair.SSPs import ssp126, ssp245, ssp370, ssp585
scenarios = {"ssp126": ssp126, "ssp245": ssp245, "ssp370": ssp370, "ssp585": ssp585}
url = "https://docs.fairmodel.net/en/v1.6.4_a/examples.html"
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")

table1, table2, table3 = soup.find_all("table")
emission_labels = {}
for tr in table1.find_all('tr')[1:]:
    index, species, unit = tr.find_all('td')
    emission_labels[int(index.text)] = species.text + " (" + unit.text + ")"
emission_labels[0] = "Year"
    
concentration_labels = {}
for tr in table2.find_all('tr')[1:]:
    index, species, unit = tr.find_all('td')
    concentration_labels[int(index.text)] = species.text + " (" + unit.text + ")"

forcing_labels = {}
for tr in table3.find_all('tr')[1:]:
    index, species = tr.find_all('td')
    forcing_labels[int(index.text)] = species.text


os.makedirs(data_path)
for name, scenario in scenarios.items():
    data = {}
    for key, var in emission_labels.items():
        data[var] = scenario.Emissions.emissions[:, key]
    df = pd.DataFrame(data)
    path = os.path.join(data_path, name + "_emissions.csv")
    df.to_csv(path)
    
    data = {'Year' : scenario.Concentrations.concentrations[:,0]} # labels do not include year
    for key, var in concentration_labels.items():
        data[var] = scenario.Concentrations.concentrations[:, key+1]
    df = pd.DataFrame(data)
    path = os.path.join(data_path, name + "_concentrations.csv")
    df.to_csv(path)