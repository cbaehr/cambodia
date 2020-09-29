

#path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"
path = "/sciclone/home20/cbaehr/cambodia/eba/inputData"

import pandas as pd
from shapely.geometry import shape, Point, MultiPoint, MultiPolygon
import numpy as np
from osgeo import gdal, ogr
import geopandas as gpd
import re
import itertools

grid = pd.read_csv(path+"/full_grid3.csv")

for i in grid.columns:
	print(i)

names_order = ["cell_id", "lon", "lat", "GID_1", "NAME_1", "GID_2", "NAME_2", "GID_3", "NAME_3", "distance_to_city", "distance_to_road", "gpw_density_2000", "plantation", "concession", "protected_area"]

for i in ["tc", "ndvi", "temp_", "precip_", "treatment_irrigation1000_", "treatment_irrigation2000_", "treatment_irrigation3000_", "treatment_irrigation4000_", "treatment_irrigation5000_"]:
	for j in range(1999, 2019):
		names_order = names_order + [i+str(j)]
		if i+str(j) not in grid.columns:
			grid[i+str(j)] = "NA"
grid = grid[names_order]

new_names = ["cell_id", "longitude", "latitude", "province_number", "province_name", "district_number", "district_name", "commune_number", "commune_name", "distance_to_city", "distance_to_road", "GPWdensity2000", "plantation", "concession", "protected_area"]

for i in ["treecover", "ndvi", "temperature", "precip", "trt_irrigation1km", "trt_irrigation2km", "trt_irrigation3km", "trt_irrigation4km", "trt_irrigation5km"]:
	for j in range(1999, 2019):
		new_names = new_names + [i+str(j)]

names_dict = {}
for i in range(0, len(names_order)):
	names_dict[names_order[i]] = new_names[i]
grid.rename(columns=names_dict, inplace=True)

grid.dropna(axis=0, subset=["cell_id"], inplace=True)

#grid.to_csv(path+"/pre_panel.csv", index=False, encoding="utf-8")
grid.to_csv(path+"/pre_panel_irrigation.csv", index=False, encoding="utf-8")



headers = [str(i) for i in range(1999, 2019)]
treecover_idx = ["treecover" in i for i in grid.columns]
ndvi_idx = ["ndvi" in i for i in grid.columns]
temperature_idx = ["temperature" in i for i in grid.columns]
precip_idx = ["precip" in i for i in grid.columns]

trtig1km_idx = ["trt_irrigation1km" in i for i in grid.columns]
trtig2km_idx = ["trt_irrigation2km" in i for i in grid.columns]
trtig3km_idx = ["trt_irrigation3km" in i for i in grid.columns]
trtig4km_idx = ["trt_irrigation4km" in i for i in grid.columns]
trtig5km_idx = ["trt_irrigation5km" in i for i in grid.columns]

del grid

new_names = ["cell_id", "longitude", "latitude", "province_number", "province_name", "district_number", "district_name", "commune_number", "commune_name", "distance_to_city", "distance_to_road", "GPWdensity2000", "plantation", "concession", "protected_area"]

#for i in ["treecover", "ndvi", "trt1km", "trt2km", "trt3km", "trt4km", "trt5km", "temperature", "precip"]:
#	for j in range(1999, 2019):
#		new_names = new_names + [i+str(j)]
for i in ["treecover", "ndvi", "trt1km", "trt2km", "trt3km", "trt4km", "trt5km", "temperature", "precip", "trt_irrigation1km", "trt_irrigation2km", "trt_irrigation3km", "trt_irrigation4km", "trt_irrigation5km", "trt_roads1km", "trt_roads2km", "trt_roads3km", "trt_roads4km", "trt_roads5km"]:
	for j in range(1999, 2019):
		new_names = new_names + [i+str(j)]


with open(path+"/pre_panel2.csv") as f, open(path+"/panel2.csv", "w") as f2:
	a=f2.write("cell_id,year,longitude,latitude,province_number,province_name,district_number,district_name,commune_number,commune_name,distance_to_city,distance_to_road,GPWdensity2000,plantation,concession,protected_area,treecover,ndvi,trt1km,trt2km,trt3km,trt4km,trt5km,temperature,precip,trt_irrigation1km,trt_irrigation2km,trt_irrigation3km,trt_irrigation4km,trt_irrigation5km,trt_roads1km,trt_roads2km,trt_roads3km,trt_roads4km,trt_roads5km\n")
	for i, line in enumerate(f):
		if i>0:
			x = line.strip().split(",")
			cell, longitude, latitude, province_number, province_name, district_number, district_name, commune_number, commune_name, city_dist, road_dist, pop, plantation, concession, pa = x[0:15]
			treecover = list(itertools.compress(x, treecover_idx))
			ndvi = list(itertools.compress(x, ndvi_idx))
			trt1km = list(itertools.compress(x, trt1km_idx))
			trt2km = list(itertools.compress(x, trt2km_idx))
			trt3km = list(itertools.compress(x, trt3km_idx))
			trt4km = list(itertools.compress(x, trt4km_idx))
			trt5km = list(itertools.compress(x, trt5km_idx))
			temperature = list(itertools.compress(x, temperature_idx))
			precip = list(itertools.compress(x, precip_idx))
			trtig1km = list(itertools.compress(x, trtig1km_idx))
			trtig2km = list(itertools.compress(x, trtig2km_idx))
			trtig3km = list(itertools.compress(x, trtig3km_idx))
			trtig4km = list(itertools.compress(x, trtig4km_idx))
			trtig5km = list(itertools.compress(x, trtig5km_idx))
			trtrd1km = list(itertools.compress(x, trtrd1km_idx))
			trtrd2km = list(itertools.compress(x, trtrd2km_idx))
			trtrd3km = list(itertools.compress(x, trtrd3km_idx))
			trtrd4km = list(itertools.compress(x, trtrd4km_idx))
			trtrd5km = list(itertools.compress(x, trtrd5km_idx))
			for year, tc_out, ndvi_out, trt1km_out, trt2km_out, trt3km_out, trt4km_out, trt5km_out, temperature_out, precip_out, trtig1km_out, trtig2km_out, trtig3km_out, trtig4km_out, trtig5km_out, trtrd1km_out, trtrd2km_out, trtrd3km_out, trtrd4km_out, trtrd5km_out in zip(headers, treecover, ndvi, trt1km, trt2km, trt3km, trt4km, trt5km, temperature, precip, trtig1km, trtig2km, trtig3km, trtig4km, trtig5km, trtrd1km, trtrd2km, trtrd3km, trtrd4km, trtrd5km):
				a=f2.write(",".join([cell, year, longitude, latitude, province_number, province_name, district_number, district_name, commune_number, commune_name, city_dist, road_dist, pop, plantation, concession, pa, tc_out, ndvi_out, trt1km_out, trt2km_out, trt3km_out, trt4km_out, trt5km_out, temperature_out, precip_out, trtig1km_out, trtig2km_out, trtig3km_out, trtig4km_out, trtig5km_out, trtrd1km_out, trtrd2km_out, trtrd3km_out, trtrd4km_out, trtrd5km_out])+'\n')















