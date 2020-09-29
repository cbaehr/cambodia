
#path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"
path = "/sciclone/home20/cbaehr/cambodia/eba/inputData"

import pandas as pd
from shapely.geometry import Point
import geopandas as gpd

empty_grid = pd.read_csv(path+"/empty_grid.csv").reset_index(drop=True)

empty_grid_geometry = [Point(xy) for xy in zip(empty_grid.lon, empty_grid.lat)]
empty_grid_geo = gpd.GeoDataFrame(empty_grid['cell_id'], crs='epsg:4326', geometry=empty_grid_geometry)

del empty_grid_geometry

adm = gpd.read_file(path+"/gadm36_KHM_3.geojson")
adm.crs = "epsg:4326"
adm_grid = gpd.sjoin(empty_grid_geo, adm[["GID_1", "NAME_1", "GID_2", "NAME_2", "GID_3", "NAME_3", "geometry"]], how='left', op='intersects')

adm_grid.drop(["geometry", "index_right"], axis=1, inplace=True)

adm_grid.to_csv(path+"/adm_grid.csv", index=False, encoding="utf-8")

