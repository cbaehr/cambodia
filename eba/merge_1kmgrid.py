
### SWITCH ###
#path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"
path = "/sciclone/home20/cbaehr/cambodia/eba/inputData"

import fiona
import pandas as pd
import geopandas as gpd
from shapely.geometry import shape, Point, MultiPoint, MultiPolygon
from shapely.prepared import prep
import numpy as np
from osgeo import gdal, ogr
import re
import itertools

#######################################

grid = pd.read_csv(path+"/merging_grid_1km.csv")

### SWITCH ###
#full_grid = pd.read_csv(path+"/full_grid_new_test.csv")
full_grid = pd.read_csv(path+"/full_grid_new.csv")

full_grid.drop(["lon", "lat", "GID_1", "NAME_1", "GID_2", "NAME_2", "GID_3", "NAME_3", "gpw_density_2005", "gpw_density_2010", "gpw_density_2015", "gpw_density_2020"], axis=1, inplace=True)

full_grid = pd.concat([grid, full_grid], axis=1)
full_grid.drop(["cell_id_y", "cell_id"], axis=1, inplace=True)

full_grid = full_grid.loc[~full_grid["cell_id_x"].isnull(), ]

del grid

for i in range(1999, 2019):
	full_grid.loc[full_grid["ndvi"+str(i)]<=0, "ndvi"+str(i)] = np.nan

### NEED TO DO THE REGULAR PRE PANEL PROCESSING FOR THIS FINAL DATASET
for i in range(2001, 2018):
	full_grid.loc[full_grid["temp_"+str(i)]<=0, "temp_"+str(i)] = np.nan

for i in range(2000, 2017):
	full_grid.loc[(full_grid["precip_"+str(i)]<=0) | (full_grid["precip_"+str(i)]>1000), "precip_"+str(i)] = np.nan

full_grid["plantation"] = full_grid["plantation"] * 1
full_grid["concession"] = full_grid["concession"] * 1
full_grid["protected_area"] = full_grid["protected_area"] * 1

grid_1km = full_grid.groupby("cell_id_x").agg(["mean"])

full_grid["count_var"]=1
temp = full_grid[["cell_id_x", "count_var"]].groupby("cell_id_x").agg(["count"])

del full_grid

grid_1km.columns = grid_1km.columns.get_level_values(0)
grid_1km["cell_id"] = grid_1km.index
grid_1km["count"] = temp[["count_var"]]
grid_1km = grid_1km.reset_index(drop=True)

del temp

grid_1km.to_csv(path+"/grid_1km_placeholder.csv", index=False, encoding="utf-8")

















