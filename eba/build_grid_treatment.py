
#path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"
path="/sciclone/home20/cbaehr/cambodia/eba/inputData"

import geopandas as gpd
import itertools
import numpy as np
import pandas as pd
import rasterio
from rasterstats import zonal_stats
from shapely.geometry import Point


empty_grid = pd.read_csv(path+"/empty_grid.csv")

########

def build(year_str):
    j = year_str.split('|')
    return {i:j.count(i) for i in set(j)}

treatment = gpd.read_file(path+"/pid/pid2003-18.geojson")

grid_geometry = [Point(xy) for xy in zip(empty_grid.longitude, empty_grid.latitude)]
empty_grid_geo = gpd.GeoDataFrame(empty_grid['cell_id'], crs={'init': 'epsg:4326'}, geometry=grid_geometry)

activity_types = ["Rural Transport", "Irrigation", "Rural Domestic Water Supplies", "Urban transport", "Education", "other"]

for i in activity_types:
	if i=="other":
		treatment_temp = treatment[~treatment.activity_type.isin(["Rural Transport", "Irrigation", "Rural Domestic Water Supplies", "Urban transport", "Education"])]
	else:
		treatment_temp = treatment[treatment.activity_type==i]
	treatment_temp = gpd.sjoin(empty_grid_geo, treatment_temp[['end_year', 'geometry']], how='left', op='intersects')
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
	treatment_grid_temp.columns = [i+str(j) for j in range(1999, 2019)]
	if i=="Rural Transport":
		treatment_grid = pd.concat([empty_grid.reset_index(drop=True), treatment_grid_temp.reset_index(drop=True)], axis=1)
	else:
		treatment_grid = pd.concat([treatment_grid.reset_index(drop=True), treatment_grid_temp.reset_index(drop=True)], axis=1)

treatment_grid.to_csv(path+"/treatment_grid.csv",index=False)
