
path = "/sciclone/home20/cbaehr/cambodia/eba/inputData"

import pandas as pd

grid = pd.read_csv(path+"/full_grid2.csv").reset_index(drop=True)
#print(grid.shape)
drop_cols = ["treatment1000_"+str(i) for i in range(1999, 2019)]+["treatment2000_"+str(i) for i in range(1999, 2019)]+["treatment3000_"+str(i) for i in range(1999, 2019)]+["treatment4000_"+str(i) for i in range(1999, 2019)]+["treatment5000_"+str(i) for i in range(1999, 2019)]
grid.drop(drop_cols, axis=1, inplace=True)

gov_grid = pd.read_csv(path+"/adm_grid.csv").reset_index(drop=True).drop(["cell_id"], axis=1)
#print(gov_grid.shape)

trt_irrigation = pd.read_csv(path+"/roadsandbridges_grid.csv").reset_index(drop=True).drop(["cell_id"], axis=1)
#print(trt_irrigation.shape)

grid = pd.concat([grid, gov_grid, trt_irrigation], axis=1)

del gov_grid, trt_irrigation

grid.to_csv(path+"/full_grid_roads.csv", index=False)

#################################################################################

names_order = ["cell_id", "lon", "lat", "GID_1", "NAME_1", "GID_2", "NAME_2", "GID_3", "NAME_3", "distance_to_city", "distance_to_road", "gpw_density_2000", "plantation", "concession", "protected_area"]


for i in ["tc", "ndvi", "temp_", "precip_", "treatment_roadsandbridges1000_", "treatment_roadsandbridges2000_", "treatment_roadsandbridges3000_", "treatment_roadsandbridges4000_", "treatment_roadsandbridges5000_"]:
	for j in range(1999, 2019):
		names_order = names_order + [i+str(j)]
		if i+str(j) not in grid.columns:
			grid[i+str(j)] = "NA"
grid = grid[names_order]

#new_names = ["cell_id", "longitude", "latitude", "province_number", "province_name", "district_number", "district_name", "commune_number", "commune_name"]
new_names = ["cell_id", "longitude", "latitude", "province_number", "province_name", "district_number", "district_name", "commune_number", "commune_name", "distance_to_city", "distance_to_road", "GPWdensity2000", "plantation", "concession", "protected_area"]

for i in ["treecover", "ndvi", "temperature", "precip", "trt_roads1km", "trt_roads2km", "trt_roads3km", "trt_roads4km", "trt_roads5km"]:
	for j in range(1999, 2019):
		new_names = new_names + [i+str(j)]

names_dict = {}
for i in range(0, len(names_order)):
	names_dict[names_order[i]] = new_names[i]
grid.rename(columns=names_dict, inplace=True)

grid.dropna(axis=0, subset=["cell_id"], inplace=True)

#grid.to_csv(path+"/pre_panel.csv", index=False, encoding="utf-8")
grid.to_csv(path+"/pre_panel_roads.csv", index=False, encoding="utf-8")

###

headers = [str(i) for i in range(1999, 2019)]
treecover_idx = ["treecover" in i for i in grid.columns]
ndvi_idx = ["ndvi" in i for i in grid.columns]
temperature_idx = ["temperature" in i for i in grid.columns]
precip_idx = ["precip" in i for i in grid.columns]

trtrd1km_idx = ["trt_roads1km" in i for i in grid.columns]
trtrd2km_idx = ["trt_roads2km" in i for i in grid.columns]
trtrd3km_idx = ["trt_roads3km" in i for i in grid.columns]
trtrd4km_idx = ["trt_roads4km" in i for i in grid.columns]
trtrd5km_idx = ["trt_roads5km" in i for i in grid.columns]

del grid

with open(path+"/pre_panel_roads.csv") as f, open(path+"/panel_roads.csv", "w") as f2:
	a=f2.write("cell_id,year,longitude,latitude,province_number,province_name,district_number,district_name,commune_number,commune_name,distance_to_city,distance_to_road,GPWdensity2000,plantation,concession,protected_area,treecover,ndvi,temperature,precip,trt_roads1km,trt_roads2km,trt_roads3km,trt_roads4km,trt_roads5km\n")
	for i, line in enumerate(f):
		if i>0:
			x = line.strip().split(",")
			cell, longitude, latitude, province_number, province_name, district_number, district_name, commune_number, commune_name, city_dist, road_dist, pop, plantation, concession, pa = x[0:15]
			treecover = list(itertools.compress(x, treecover_idx))
			ndvi = list(itertools.compress(x, ndvi_idx))
			temperature = list(itertools.compress(x, temperature_idx))
			precip = list(itertools.compress(x, precip_idx))
			trtrd1km = list(itertools.compress(x, trtrd1km_idx))
			trtrd2km = list(itertools.compress(x, trtrd2km_idx))
			trtrd3km = list(itertools.compress(x, trtrd3km_idx))
			trtrd4km = list(itertools.compress(x, trtrd4km_idx))
			trtrd5km = list(itertools.compress(x, trtrd5km_idx))
			for year, tc_out, ndvi_out, temperature_out, precip_out, trtrd1km_out, trtrd2km_out, trtrd3km_out, trtrd4km_out, trtrd5km_out in zip(headers, treecover, ndvi, temperature, precip, trtrd1km, trtrd2km, trtrd3km, trtrd4km, trtrd5km):
				a=f2.write(",".join([cell, year, longitude, latitude, province_number, province_name, district_number, district_name, commune_number, commune_name, city_dist, road_dist, pop, plantation, concession, pa, tc_out, ndvi_out, temperature_out, precip_out, trtrd1km_out, trtrd2km_out, trtrd3km_out, trtrd4km_out, trtrd5km_out])+'\n')


