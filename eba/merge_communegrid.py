
### SWITCH ###
path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"
#path = "/sciclone/home20/cbaehr/cambodia/eba/inputData"

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

### SWITCH ###
grid = pd.read_csv(path+"/full_grid_new_test.csv")
#grid = pd.read_csv(path+"/full_grid_new.csv")

grid.drop(["lon", "lat", "GID_1", "NAME_1", "GID_2", "NAME_2", "NAME_3", "gpw_density_2005", "gpw_density_2010", "gpw_density_2015", "gpw_density_2020"], axis=1, inplace=True)

for i in range(1999, 2019):
	grid.loc[grid["ndvi"+str(i)]<=0, "ndvi"+str(i)] = np.nan

### NEED TO DO THE REGULAR PRE PANEL PROCESSING FOR THIS FINAL DATASET
for i in range(2001, 2018):
	grid.loc[grid["temp_"+str(i)]<=0, "temp_"+str(i)] = np.nan

for i in range(2000, 2017):
	grid.loc[(grid["precip_"+str(i)]<=0) | (grid["precip_"+str(i)]>1000), "precip_"+str(i)] = np.nan

grid["plantation"] = grid["plantation"] * 1
grid["concession"] = grid["concession"] * 1
grid["protected_area"] = grid["protected_area"] * 1

grid_commune = grid.groupby("GID_3").agg(["mean"])

grid["count_var"]=1
temp = grid[["GID_3", "count_var"]].groupby("GID_3").agg(["count"])

del grid

grid_commune.columns = grid_commune.columns.get_level_values(0)
grid_commune["cell_id"] = grid_commune.index
grid_commune["count"] = temp[["count_var"]]
grid_commune = grid_commune.reset_index(drop=True)

del temp

grid_commune.to_csv(path+"/grid_commune_placeholder.csv", index=False, encoding="utf-8")










