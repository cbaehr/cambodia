
#path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"
path = "/sciclone/home20/cbaehr/cambodia/eba/inputData"

import pandas as pd
from shapely.geometry import shape, Point, MultiPoint, MultiPolygon
import numpy as np
from osgeo import gdal, ogr
import geopandas as gpd
import re
import itertools

empty_grid = pd.read_csv(path+"/empty_grid.csv").reset_index(drop=True)
empty_grid.shape

###

treatment_grid = pd.read_csv(path+"/treatment_grid.csv").reset_index(drop=True).drop(["cell_id"], axis=1)
treatment_grid.shape

temperature_grid = pd.read_csv(path+"/temperature_grid.csv").reset_index(drop=True).drop(["cell_id"], axis=1)
temperature_grid.shape

precip_grid = pd.read_csv(path+"/precip_grid.csv").reset_index(drop=True).drop(["cell_id"], axis=1)
precip_grid.shape

adm_grid = pd.read_csv(path+"/adm_grid.csv").reset_index(drop=True).drop(["cell_id"], axis=1)
adm_grid.shape

hansen_grid = pd.read_csv(path+"/hansen_grid.csv").reset_index(drop=True).drop(["cell_id"], axis=1)
hansen_grid.shape

ndvi_grid = pd.read_csv(path+"/ndvi_grid.csv").reset_index(drop=True).drop(["cell_id"], axis=1)
ndvi_grid.shape

governance_grid = pd.read_csv(path+"/governance_grid.csv").reset_index(drop=True).drop(["cell_id"], axis=1)
governance_grid.shape

misc_grid = pd.read_csv(path+"/misc_grid.csv").reset_index(drop=True).drop(["cell_id"], axis=1)
misc_grid.shape

grid = pd.concat([empty_grid, treatment_grid, temperature_grid, precip_grid, adm_grid, hansen_grid, ndvi_grid, governance_grid, misc_grid], axis=1)

del empty_grid, treatment_grid, temperature_grid, precip_grid, adm_grid, hansen_grid, ndvi_grid, governance_grid, misc_grid

grid.to_csv(path+"/full_grid_new.csv", index=False, encoding="utf-8")

###

for i in grid.columns:
	print(i)

names_order = ["cell_id", "lon", "lat", "GID_1", "NAME_1", "GID_2", "NAME_2", "GID_3", "NAME_3", "plantation", "concession", "protected_area", "distance_to_city", "distance_to_road", "gpw_density_2000"]

for i in ["tc", "ndvi", "treatment1000_", "treatment2000_", "treatment3000_", "treatment4000_", "treatment5000_", "temp_", "precip_"]:
	for j in range(1999, 2019):
		names_order = names_order + [i+str(j)]
		if i+str(j) not in grid.columns:
			grid[i+str(j)] = "NA"
grid = grid[names_order]

new_names = ["cell_id", "longitude", "latitude", "province_number", "province_name", "district_number", "district_name", "commune_number", "commune_name", "plantation", "concession", "protected_area", "dist_to_city", "dist_to_road", "popdensity2000"]
for i in ["treecover", "ndvi", "trt1km", "trt2km", "trt3km", "trt4km", "trt5km", "temperature", "precip"]:
	for j in range(1999, 2019):
		new_names = new_names + [i+str(j)]
names_dict = {}
for i in range(0, len(names_order)):
	names_dict[names_order[i]] = new_names[i]
grid.rename(columns=names_dict, inplace=True)

grid.dropna(axis=0, subset=["cell_id"], inplace=True)

grid.to_csv(path+"/pre_panel_new.csv", index=False, encoding="utf-8")

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

with open(path+"/pre_panel_new.csv") as f, open(path+"/panel_new.csv", "w") as f2:
	a=f2.write("cell_id,year,longitude,latitude,province_number,province_name,district_number,district_name,commune_number,commune_name,plantation,concession,protected_area,dist_to_city,dist_to_road,popdensity2000,treecover,ndvi,trt1km,trt2km,trt3km,trt4km,trt5km,temperature,precip\n")
	for i, line in enumerate(f):
		if i>0:
			x = line.strip().split(",")
			cell, longitude, latitude, province_number, province_name, district_number, district_name, commune_number, commune_name, plantation, concession, pa, city, road, pop = x[0:15]
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
				a=f2.write(",".join([cell, year, longitude, latitude, province_number, province_name, district_number, district_name, commune_number, commune_name, plantation, concession, pa, city, road, pop, tc_out, ndvi_out, trt1km_out, trt2km_out, trt3km_out, trt4km_out, trt5km_out, temperature_out, precip_out])+'\n')

