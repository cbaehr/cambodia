
path = "/sciclone/home20/cbaehr/cambodia/eba/inputData"

import numpy as np
import pandas as pd
import itertools

#grid = pd.read_csv(path+"/full_grid.csv")
grid = pd.read_csv(path+"/full_grid.csv")

for i in grid.columns:
	print(i)

###

pa_grid_temp = grid["pa_activedate"]

for i in range(1993, 1999):
	pa_grid_temp[pa_grid_temp==str(i)] = "1999"

#def build(year_str):
#    j = year_str.split('|')
#    return {i:j.count(i) for i in set(j)}

def build(year):
	return{str(year): 1}

test = list(map(build, pa_grid_temp))

pa_grid_temp = pd.DataFrame(test)

for i in range(1999, 2019):
	if str(i) not in pa_grid_temp.columns:
		pa_grid_temp[str(i)] = 0

keep_cols = [str(i) for i in range(1999, 2019)]

pa_grid_temp = pa_grid_temp[keep_cols]

pa_grid_temp = pa_grid_temp.fillna(0)

pa_grid_temp = pa_grid_temp.apply(np.cumsum, axis=1)

pa_grid_temp.columns = ["protected_area_"+str(i) for i in range(1999, 2019)]

grid.drop(labels="pa_activedate", axis=1, inplace=True)

grid = pd.concat([grid.reset_index(drop=True), pa_grid_temp], axis=1)

del pa_grid_temp, test

###

grid.loc[grid["elc_active_date"]=="NaT", "elc_active_date"] = grid.loc[grid["elc_active_date"]=="NaT", "elc_change_date"]

elc_grid_temp = grid["elc_active_date"]

for i in range(1996, 1999):
	elc_grid_temp[elc_grid_temp==str(i)] = "1999"

test = list(map(build, elc_grid_temp))

elc_grid_temp = pd.DataFrame(test)

elc_grid_temp.drop(labels="NaT", axis=1, inplace=True)

for i in range(1999, 2019):
	if str(i) not in elc_grid_temp.columns:
		elc_grid_temp[str(i)] = 0

keep_cols = [str(i) for i in range(1999, 2019)]

elc_grid_temp = elc_grid_temp[keep_cols]

elc_grid_temp = elc_grid_temp.fillna(0)

elc_grid_temp = elc_grid_temp.apply(np.cumsum, axis=1)

elc_grid_temp.columns = ["land_concession_"+str(i) for i in range(1999, 2019)]

grid.drop(labels=["elc_active_date", "elc_change_date"], axis=1, inplace=True)

grid = pd.concat([grid.reset_index(drop=True), elc_grid_temp], axis=1)

del elc_grid_temp, test

###

grid["plantation_dummy"] = ~grid["plantation_type"].isnull() * 1

###

#names_order = ["cell_id", "longitude", "latitude", "GID_1", "NAME_1", "GID_2", "NAME_2", "GID_3", "NAME_3"]
names_order = ["cell_id", "longitude", "latitude", "GID_1", "NAME_1", "GID_2", "NAME_2", "GID_3", "NAME_3", "plantation_type", "plantation_dummy", "elc_adjustment"]
for i in ["ndvi_landsat_", "Rural Transport", "Irrigation", "Rural Domestic Water Supplies", "Urban transport", "Education", "other", "precip_", "temp_", "protected_area_", "land_concession_"]:
	for j in range(1999, 2019):
		names_order = names_order + [i+str(j)]
		if i+str(j) not in grid.columns:
			grid[i+str(j)] = "NA"
grid = grid[names_order]

#new_names = ["cell_id", "longitude", "latitude", "province_number", "province_name", "district_number", "district_name", "commune_number", "commune_name"]
new_names = ["cell_id", "longitude", "latitude", "province_number", "province_name", "district_number", "district_name", "commune_number", "commune_name", "plantation_type", "plantation_dummy", "elc_adjustment"]
for i in ["ndvi", "trt_rural_transport", "trt_irrigation", "trt_rural_domestic_water_supply", "trt_urban_transport", "trt_education", "trt_other", "precip", "temperature", "protected_area", "land_concession"]:
	for j in range(1999, 2019):
		new_names = new_names + [i+str(j)]
names_dict = {}
for i in range(0, len(names_order)):
	names_dict[names_order[i]] = new_names[i]
grid.rename(columns=names_dict, inplace=True)

grid.dropna(axis=0, subset=["cell_id"], inplace=True)

grid.to_csv(path+"/pre_panel.csv", index=False)
#grid.to_csv(path+"/pre_panel_test.csv", index=False)

headers = [str(i) for i in range(1999, 2019)]
ndvi_idx = ["ndvi" in i for i in grid.columns]
trt_rural_transport_idx = ["trt_rural_transport" in i for i in grid.columns]
trt_irrigation_idx = ["trt_irrigation" in i for i in grid.columns]
trt_rural_domestic_water_supply_idx = ["trt_rural_domestic_water_supply" in i for i in grid.columns]
trt_urban_transport_idx = ["trt_urban_transport" in i for i in grid.columns]
trt_education_idx = ["trt_education" in i for i in grid.columns]
trt_other_idx = ["trt_other" in i for i in grid.columns]
precip_idx = ["precip" in i for i in grid.columns]
temperature_idx = ["temperature" in i for i in grid.columns]
protected_area_idx = ["protected_area" in i for i in grid.columns]
land_concession_idx = ["land_concession" in i for i in grid.columns]


del grid


with open(path+"/pre_panel.csv") as f, open(path+"/panel.csv", "w") as f2:
	a=f2.write("cell_id,year,longitude,latitude,province_number,province_name,district_number,district_name,commune_number,commune_name,plantation_type,plantation_dummy,elc_adjustment,ndvi,trt_rural_transport,trt_irrigation,trt_rural_domestic_water_supply,trt_urban_transport,trt_education,trt_other,precip,temperature,protected_area,land_concession\n")
	for i, line in enumerate(f):
		if i>0:
			x = line.strip().split(",")
			cell, longitude, latitude, province_number, province_name, district_number, district_name, commune_number, commune_name, plantation_type, plantation_dummy, elc_adjustment = x[0:12]
			ndvi = list(itertools.compress(x, ndvi_idx))
			trt1 = list(itertools.compress(x, trt_rural_transport_idx))
			trt2 = list(itertools.compress(x, trt_irrigation_idx))
			trt3 = list(itertools.compress(x, trt_rural_domestic_water_supply_idx))
			trt4 = list(itertools.compress(x, trt_urban_transport_idx))
			trt5 = list(itertools.compress(x, trt_education_idx))
			trt6 = list(itertools.compress(x, trt_other_idx))
			precip = list(itertools.compress(x, precip_idx))
			temperature = list(itertools.compress(x, temperature_idx))
			protected_area = list(itertools.compress(x, protected_area_idx))
			land_concession = list(itertools.compress(x, land_concession_idx))
			for year, ndvi_out, trt1_out, trt2_out, trt3_out, trt4_out, trt5_out, trt6_out, precip_out, temperature_out, pa_out, lc_out in zip(headers, ndvi, trt1, trt2, trt3, trt4, trt5, trt6, precip, temperature, protected_area, land_concession):
				a=f2.write(",".join([cell, year, longitude, latitude, province_number, province_name, district_number, district_name, commune_number, commune_name, plantation_type, plantation_dummy, elc_adjustment, ndvi_out, trt1_out, trt2_out, trt3_out, trt4_out, trt5_out, trt6_out, precip_out, temperature_out, pa_out, lc_out])+'\n')







