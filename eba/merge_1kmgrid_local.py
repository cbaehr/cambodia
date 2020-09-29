
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

grid_1km = pd.read_csv(path+"/grid_1km_placeholder.csv")

empty_grid_1km = gpd.read_file(path+"/empty_grid_1km.geojson")
empty_grid_1km.crs = "epsg:4326"

grid = grid_1km.merge(empty_grid_1km.drop(["lon", "lat"], axis=1), left_on='cell_id', right_on='cell_id')
grid = gpd.GeoDataFrame(grid, crs="epsg:4326", geometry=grid.geometry)

grid["lon"] = grid["geometry"].centroid.x
grid["lat"] = grid["geometry"].centroid.y

grid_geometry = [Point(xy) for xy in zip(grid.lon, grid.lat)]
grid_geo = gpd.GeoDataFrame(grid['cell_id'], crs='epsg:4326', geometry=grid_geometry)

###

adm = gpd.read_file(path+"/gadm36_KHM_3.geojson")
adm_grid = gpd.sjoin(grid_geo, adm[["GID_1", "NAME_1", "GID_2", "NAME_2", "GID_3", "NAME_3", "geometry"]], how='left', op='intersects')
grid = pd.concat([grid, adm_grid.drop(["cell_id", "geometry", "index_right"], axis=1)], axis=1)

###

grid_1km_minecasualty = pd.read_csv(path+"/grid_1km_minecasualty.csv")

grid = pd.concat([grid, grid_1km_minecasualty.drop(["cell_id"], axis=1)], axis=1)

###




###

#grid.drop(["geometry"], axis=1).to_csv(path+"/grid_1km.csv", index=False, encoding="utf-8")
#grid.to_file(path+"/grid_1km.geojson", driver="GeoJSON")
























