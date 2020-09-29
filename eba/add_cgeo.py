
path1 = "/sciclone/home20/cbaehr/cambodia/eba/inputData"

path2 = "/sciclone/scr20/cbaehr"

import fiona
from shapely.geometry import shape, Point, MultiPoint, MultiPolygon
from shapely.prepared import prep
import pandas as pd
import itertools


empty_grid = pd.read_csv(path1+"/empty_grid.csv")

bombings = fiona.open(path1+"/cgeo_bombings.geojson")
bombings = bombings[0]
bombings = shape(bombings['geometry'])
prep_bombings = prep(bombings)

burials = fiona.open(path1+"/cgeo_burials.geojson")
burials = burials[0]
burials = shape(burials['geometry'])
prep_burials = prep(burials)

memorials = fiona.open(path1+"/cgeo_memorials.geojson")
memorials = memorials[0]
memorials = shape(memorials['geometry'])
prep_memorials = prep(memorials)

prisons = fiona.open(path1+"/cgeo_prisons.geojson")
prisons = prisons[0]
prisons = shape(prisons['geometry'])
prep_prisons = prep(prisons)

bombings_col = []
burials_col = []
memorials_col = []
prisons_col = []

for _, row in empty_grid.iterrows():
    c = Point(row['lon'], row['lat'])
    bombings_col.append(prep_bombings.intersects(c))
    burials_col.append(prep_burials.intersects(c))
    memorials_col.append(prep_memorials.intersects(c))
    prisons_col.append(prep_prisons.intersects(c))

cgeo = pd.DataFrame()
cgeo.insert(loc=0, column="cell_id", value=empty_grid["cell_id"])
cgeo.insert(loc=1, column="bombings", value=bombings_col)
cgeo.insert(loc=2, column="burials", value=burials_col)
cgeo.insert(loc=3, column="memorials", value=memorials_col)
cgeo.insert(loc=4, column="prisons", value=prisons_col)

del bombings_col, burials_col, memorials_col, prisons_col

cgeo = cgeo*1
cgeo.to_csv(path2+"/cgeo_grid.csv", index=False)

###

pre_panel = pd.read_csv(path1+"/pre_panel_corrected.csv")

grid = pd.concat([pre_panel, cgeo.drop(["cell_id"], axis=1)], axis=1)

names_order = ["cell_id", "longitude", "latitude", "province_number", "province_name", "district_number", "district_name", "commune_number", "commune_name", "plantation", "concession", "protected_area", "dist_to_city", "dist_to_road", "popdensity2000", "bombings", "burials", "memorials", "prisons"]
for i in ["treecover", "ndvi", "trt1km", "trt2km", "trt3km", "trt4km", "trt5km", "temperature", "precip"]:
	for j in range(1999, 2019):
		names_order = names_order + [i+str(j)]

grid = grid[names_order]

grid.to_csv(path2+"/pre_panel_corrected_cgeo.csv", index=False)

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

del pre_panel, grid, cgeo

with open(path2+"/pre_panel_corrected_cgeo.csv") as f, open(path2+"/panel_corrected_cgeo.csv", "w") as f2:
	a=f2.write("cell_id,year,longitude,latitude,province_number,province_name,district_number,district_name,commune_number,commune_name,plantation,concession,protected_area,dist_to_city,dist_to_road,popdensity2000,bombings,burials,memorials,prisons,treecover,ndvi,trt1km,trt2km,trt3km,trt4km,trt5km,temperature,precip\n")
	for i, line in enumerate(f):
		if i>0:
			x = line.strip().split(",")
			cell, longitude, latitude, province_number, province_name, district_number, district_name, commune_number, commune_name, plantation, concession, pa, city, road, pop, bombings, burials, memorials, prisons = x[0:19]
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
				a=f2.write(",".join([cell, year, longitude, latitude, province_number, province_name, district_number, district_name, commune_number, commune_name, plantation, concession, pa, city, road, pop, bombings, burials, memorials, prisons, tc_out, ndvi_out, trt1km_out, trt2km_out, trt3km_out, trt4km_out, trt5km_out, temperature_out, precip_out])+'\n')





























