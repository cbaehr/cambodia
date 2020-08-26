
path = "/Users/christianbaehr/Downloads"

import itertools
import pandas as pd

grid = pd.read_csv(path+"/full_grid.csv")

###

for i in grid.columns:
	print(i)

names_order = ["cell_id", "lon", "lat", "GID_1", "NAME_1", "GID_2", "NAME_2", "GID_3", "NAME_3"]

for i in ["tc", "ndvi", "treatment1000_", "treatment2000_", "treatment3000_", "treatment4000_", "treatment5000_", "temp_", "precip_"]:
	for j in range(1999, 2019):
		names_order = names_order + [i+str(j)]
		if i+str(j) not in grid.columns:
			grid[i+str(j)] = "NA"
grid = grid[names_order]

new_names = ["cell_id", "longitude", "latitude", "province_number", "province_name", "district_number", "district_name", "commune_number", "commune_name"]
for i in ["treecover", "ndvi", "trt1km", "trt2km", "trt3km", "trt4km", "trt5km", "temperature", "precip"]:
	for j in range(1999, 2019):
		new_names = new_names + [i+str(j)]
names_dict = {}
for i in range(0, len(names_order)):
	names_dict[names_order[i]] = new_names[i]
grid.rename(columns=names_dict, inplace=True)

grid.dropna(axis=0, subset=["cell_id"], inplace=True)

grid.to_csv(path+"/pre_panel.csv", index=False, encoding="utf-8")

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


with open(path+"/pre_panel.csv") as f, open(path+"/panel.csv", "w") as f2:
	a=f2.write("cell_id,year,longitude,latitude,province_number,province_name,district_number,district_name,commune_number,commune_name,treecover,ndvi,trt1km,trt2km,trt3km,trt4km,trt5km,temperature,precip\n")
	for i, line in enumerate(f):
		if i>0:
			x = line.strip().split(",")
			cell, longitude, latitude, province_number, province_name, district_number, district_name, commune_number, commune_name = x[0:9]
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
				a=f2.write(",".join([cell, year, longitude, latitude, province_number, province_name, district_number, district_name, commune_number, commune_name, tc_out, ndvi_out, trt1km_out, trt2km_out, trt3km_out, trt4km_out, trt5km_out, temperature_out, precip_out])+'\n')










