

### SWITCH ###
path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"
#path = "/sciclone/home20/cbaehr/cambodia/eba/inputData"


import pandas as pd
import geopandas as gpd
from shapely.geometry import shape, Point, MultiPoint, MultiPolygon
import numpy as np
from osgeo import gdal, ogr
import re
import itertools


### SWITCH ###
empty_grid = pd.read_csv(path+"/empty_grid_test.csv")
#empty_grid = pd.read_csv(path+"/empty_grid.csv")

empty_grid_geometry = [Point(xy) for xy in zip(empty_grid.lon, empty_grid.lat)]
empty_grid.drop(["lon", "lat"], axis=1, inplace=True)
empty_grid_geo = gpd.GeoDataFrame(empty_grid, crs='epsg:4326', geometry=empty_grid_geometry)

del empty_grid, empty_grid_geometry

###

empty_grid_1km = gpd.read_file(path+"/empty_grid_1km.geojson")
empty_grid_1km.crs = "epsg:4326"

empty_grid_1km.drop(["lon", "lat"], axis=1, inplace=True)

grid = gpd.sjoin(empty_grid_1km, empty_grid_geo, how="right", op="intersects")
grid.drop(["index_left", "geometry"], axis=1, inplace=True)

del empty_grid_1km

grid.to_csv(path+"/merging_grid_1km.csv", index=False)












