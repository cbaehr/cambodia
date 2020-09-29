
path = "/sciclone/home20/cbaehr/cambodia/eba/inputData"

output = "/sciclone/scr20/cbaehr"

import pandas as pd
import numpy as np
import itertools

gov_grid = pd.read_csv(path+"/governance_grid.csv")
print(gov_grid.shape)
gov_grid.drop(["cell_id"], axis=1, inplace=True)

mine_grid = pd.read_csv(path+"/mine_grid.csv")
print(mine_grid.shape)
mine_grid.drop(["cell_id"], axis=1, inplace=True)

main_grid = pd.read_csv(path+"/full_grid_new.csv")
print(main_grid.shape)
main_grid.drop(["plantation", "concession", "protected_area"], axis=1, inplace=True)
drop_cols = ["treatment1000_"+str(i) for i in range(1999, 2019)]+["treatment2000_"+str(i) for i in range(1999, 2019)]+["treatment3000_"+str(i) for i in range(1999, 2019)]+["treatment4000_"+str(i) for i in range(1999, 2019)]+["treatment5000_"+str(i) for i in range(1999, 2019)]
main_grid.drop(drop_cols, axis=1, inplace=True)

for i in range(1999, 2019):
	main_grid.loc[main_grid["ndvi"+str(i)]<=0, "ndvi"+str(i)] = np.nan
### NEED TO DO THE REGULAR PRE PANEL PROCESSING FOR THIS FINAL DATASET
for i in range(2001, 2018):
	main_grid.loc[main_grid["temp_"+str(i)]<=0, "temp_"+str(i)] = np.nan
for i in range(2000, 2017):
	main_grid.loc[(main_grid["precip_"+str(i)]<=0) | (main_grid["precip_"+str(i)]>1000), "precip_"+str(i)] = np.nan

treatment_grid = pd.read_csv(path+"/irrigation_grid.csv")
treatment_grid.drop(["cell_id"], axis=1, inplace=True)

grid = pd.concat([gov_grid, mine_grid, main_grid, treatment_grid], axis=1)

del gov_grid, mine_grid, main_grid, treatment_grid

###

names_order = ["cell_id", "lon", "lat", "GID_1", "NAME_1", "GID_2", "NAME_2", "GID_3", "NAME_3", "plantation", "concession", "protected_area", "distance_to_city", "distance_to_road", "gpw_density_2000", "distance_to_minecasualty"]

for i in ["tc", "ndvi", "treatment_irrigation1000_", "treatment_irrigation2000_", "treatment_irrigation3000_", "treatment_irrigation4000_", "treatment_irrigation5000_", "temp_", "precip_"]:
	for j in range(1999, 2019):
		names_order = names_order + [i+str(j)]
		if i+str(j) not in grid.columns:
			grid[i+str(j)] = "NA"
grid = grid[names_order]

new_names = ["cell_id", "longitude", "latitude", "province_number", "province_name", "district_number", "district_name", "commune_number", "commune_name", "plantation", "concession", "protected_area", "dist_to_city", "dist_to_road", "popdensity2000", "dist_to_minecasualty"]
for i in ["treecover", "ndvi", "trt1km_irrigation", "trt2km_irrigation", "trt3km_irrigation", "trt4km_irrigation", "trt5km_irrigation", "temperature", "precip"]:
	for j in range(1999, 2019):
		new_names = new_names + [i+str(j)]
names_dict = {}
for i in range(0, len(names_order)):
	names_dict[names_order[i]] = new_names[i]
grid.rename(columns=names_dict, inplace=True)

grid.dropna(axis=0, subset=["cell_id"], inplace=True)

grid.to_csv(output+"/pre_panel_corrected_irrigation.csv", index=False, encoding="utf-8")

###

headers = [str(i) for i in range(1999, 2019)]
treecover_idx = ["treecover" in i for i in grid.columns]
ndvi_idx = ["ndvi" in i for i in grid.columns]
trt1km_idx = ["trt1km" in i for i in grid.columns]
trt2km_idx = ["trt2km" in i for i in grid.columns]
trt3km_idx = ["trt3km" in i for i in grid.columns]
trt4km_idx = ["trt4km" in i for i in grid.columns]
trt5km_idx = ["trt5km" in i for i in grid.columns]
temperature_idx = ["temperature" in i for i in grid.columns]
precip_idx = ["precip" in i for i in grid.columns]

del grid

with open(output+"/pre_panel_corrected_irrigation.csv") as f, open(output+"/panel_corrected_irrigation.csv", "w") as f2:
	a=f2.write("cell_id,year,longitude,latitude,province_number,province_name,district_number,district_name,commune_number,commune_name,plantation,concession,protected_area,dist_to_city,dist_to_road,popdensity2000,dist_to_minecasualty,treecover,ndvi,trt1km_irrigation,trt2km_irrigation,trt3km_irrigation,trt4km_irrigation,trt5km_irrigation,temperature,precip\n")
	for i, line in enumerate(f):
		if i>0:
			x = line.strip().split(",")
			cell, longitude, latitude, province_number, province_name, district_number, district_name, commune_number, commune_name, plantation, concession, pa, city, road, pop, mine = x[0:16]
			treecover = list(itertools.compress(x, treecover_idx))
			ndvi = list(itertools.compress(x, ndvi_idx))
			trt1km = list(itertools.compress(x, trt1km_idx))
			trt2km = list(itertools.compress(x, trt2km_idx))
			trt3km = list(itertools.compress(x, trt3km_idx))
			trt4km = list(itertools.compress(x, trt4km_idx))
			trt5km = list(itertools.compress(x, trt5km_idx))
			temperature = list(itertools.compress(x, temperature_idx))
			precip = list(itertools.compress(x, precip_idx))
			for year, tc_out, ndvi_out, trt1km_out, trt2km_out, trt3km_out, trt4km_out, trt5km_out, temperature_out, precip_out in zip(headers, treecover, ndvi, trt1km, trt2km, trt3km, trt4km, trt5km, temperature, precip):
				a=f2.write(",".join([cell, year, longitude, latitude, province_number, province_name, district_number, district_name, commune_number, commune_name, plantation, concession, pa, city, road, pop, mine, tc_out, ndvi_out, trt1km_out, trt2km_out, trt3km_out, trt4km_out, trt5km_out, temperature_out, precip_out])+'\n')










