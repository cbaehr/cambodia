
#path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"
path = "/sciclone/home20/cbaehr/cambodia/eba/inputData"

import pandas as pd
from shapely.geometry import shape, Point, MultiPoint, MultiPolygon
import numpy as np
import geopandas as gpd

###

#grid = pd.read_csv("/Users/christianbaehr/Downloads/empty_grid_test.csv").reset_index(drop=True)
grid = pd.read_csv(path+"/empty_grid.csv").reset_index(drop=True)

###

grid_geometry = [Point(xy) for xy in zip(grid.lon, grid.lat)]
grid_geo = gpd.GeoDataFrame(grid['cell_id'], crs='epsg:4326', geometry=grid_geometry)

del grid_geometry

###

def build(year_str):
    j = year_str.split('|')
    return {i:j.count(i) for i in set(j)}

irrigation_treatment = gpd.read_file(path+"/pid/pid_irrigation.geojson")
irrigation_treatment.crs = "epsg:4326"
irrigation_treatment = irrigation_treatment[["end_year", "mrb_dist", "geometry"]]
irrigation_treatment["mrb_dist"] = irrigation_treatment["mrb_dist"].astype(int)

###

for i in [1000, 2000, 3000, 4000, 5000]:
	temp = irrigation_treatment.loc[irrigation_treatment["mrb_dist"]==i]
	treatment_temp = gpd.sjoin(grid_geo, temp[['end_year', 'geometry']], how='left', op='intersects')
	treatment_temp = treatment_temp[['cell_id', 'end_year']]
	treatment_temp['end_year'] = treatment_temp['end_year'].astype('Int64').astype('str')
	treatment_grid_temp = treatment_temp.pivot_table(values='end_year', index='cell_id', aggfunc='|'.join)
	treatment_grid_temp = treatment_grid_temp['end_year'].tolist()
	treatment_grid_temp = list(map(build, treatment_grid_temp))
	treatment_grid_temp = pd.DataFrame(treatment_grid_temp)
	treatment_grid_temp = treatment_grid_temp.fillna(0)
	for j in range(1999, 2019):
		if str(j) not in treatment_grid_temp.columns:
			treatment_grid_temp[str(j)] = 0
	treatment_grid_temp = treatment_grid_temp.reindex(sorted(treatment_grid_temp.columns), axis=1)
	if '<NA>' in treatment_grid_temp.columns:
		treatment_grid_temp.drop(labels='<NA>', axis=1, inplace=True)
	if '2019' in treatment_grid_temp.columns:
		treatment_grid_temp.drop(labels='2019', axis=1, inplace=True)
	if "nan" in treatment_grid_temp.columns:
		treatment_grid_temp.drop(labels="nan", axis=1, inplace=True)
	treatment_grid_temp = treatment_grid_temp.apply(np.cumsum, axis=1)
	treatment_grid_temp.columns = ["treatment_irrigation"+str(i)+"_"+str(j) for j in range(1999, 2019)]
	if i==1000:
		treatment_grid = pd.concat([grid[["cell_id"]].reset_index(drop=True), treatment_grid_temp.reset_index(drop=True)], axis=1)
	else:
		treatment_grid = pd.concat([treatment_grid.reset_index(drop=True), treatment_grid_temp.reset_index(drop=True)], axis=1)

###

treatment_grid.reset_index(drop=True).to_csv(path+"/irrigation_grid.csv", index=False)













