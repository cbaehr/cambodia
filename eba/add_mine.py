
path1 = "/sciclone/home20/cbaehr/cambodia/eba/inputData"

path2 = "/sciclone/scr20/cbaehr"

import fiona
from shapely.geometry import shape, Point, MultiPoint, MultiPolygon
from shapely.prepared import prep
import pandas as pd
import itertools

#mine_grid = pd.read_csv(path1+"/mine_grid.csv")
#print(mine_grid.shape)

#merging_grid = pd.read_csv(path1+"/merging_grid_1km.csv")
#print(merging_grid.shape)

#mine_grid = mine_grid.merge(merging_grid, left_on="cell_id", right_on="cell_id_y")
#print(mine_grid.shape)

#del merging_grid

#grid = pd.read_csv(path2+"/pre_panel_corrected_cgeo.csv")
#print(grid.shape)

#grid = pd.concat([grid, mine_grid], axis=1)

#names_order = ["cell_id", "longitude", "latitude", "province_number", "province_name", "district_number", "district_name", "commune_number", "commune_name", "plantation", "concession", "protected_area", "dist_to_city", "dist_to_road", "popdensity2000", "bombings", "burials", "memorials", "prisons", "distance_to_minecasualty", "cell_id_x"]
#for i in ["treecover", "ndvi", "trt1km", "trt2km", "trt3km", "trt4km", "trt5km", "temperature", "precip"]:
#	for j in range(1999, 2019):
#		names_order = names_order + [i+str(j)]

#grid = grid[names_order]

#grid.to_csv(path2+"/pre_panel_corrected_cgeo_mines.csv", index=False)

grid=pd.read_csv(path2+"/pre_panel_corrected_cgeo_mines.csv")
grid.drop(["cell_id.1"], axis=1, inplace=True)

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


grid.to_csv(path2+"/pre_panel_corrected_cgeo_mines.csv", index=False)
del grid


with open(path2+"/pre_panel_corrected_cgeo_mines.csv") as f, open(path2+"/panel_corrected_cgeo_mines.csv", "w") as f2:
	a=f2.write("cell_id,year,longitude,latitude,province_number,province_name,district_number,district_name,commune_number,commune_name,plantation,concession,protected_area,dist_to_city,dist_to_road,popdensity2000,bombings,burials,memorials,prisons,distance_to_minecasualty,cellid1km,treecover,ndvi,trt1km,trt2km,trt3km,trt4km,trt5km,temperature,precip\n")
	for i, line in enumerate(f):
		if i>0:
			x = line.strip().split(",")
			cell, longitude, latitude, province_number, province_name, district_number, district_name, commune_number, commune_name, plantation, concession, pa, city, road, pop, bombings, burials, memorials, prisons, mine, cellid1km = x[0:21]
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
				a=f2.write(",".join([cell, year, longitude, latitude, province_number, province_name, district_number, district_name, commune_number, commune_name, plantation, concession, pa, city, road, pop, bombings, burials, memorials, prisons, mine, cellid1km, tc_out, ndvi_out, trt1km_out, trt2km_out, trt3km_out, trt4km_out, trt5km_out, temperature_out, precip_out])+'\n')













