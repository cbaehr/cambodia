
path="/sciclone/home20/cbaehr/cambodia/eba/inputData"

import pandas as pd
from shapely.geometry import Point
import geopandas

empty_grid = pd.read_csv(path+"/empty_grid.csv")

#def build(year_str):
#    j = year_str.split('|')
#    return {i:j.count(i) for i in set(j)}

grid_geometry = [Point(xy) for xy in zip(empty_grid.longitude, empty_grid.latitude)]
#empty_grid_geo = geopandas.GeoDataFrame(empty_grid['cell_id'], crs='epsg:4326', geometry=grid_geometry)
empty_grid_geo = geopandas.GeoDataFrame(empty_grid['cell_id'], crs={'init': 'epsg:4326'}, geometry=grid_geometry)

adm = geopandas.read_file(path+"/gadm36_KHM_3.geojson")

adm_grid = geopandas.sjoin(empty_grid_geo, adm[["GID_1", "NAME_1", "GID_2", "NAME_2", "GID_3", "NAME_3", "geometry"]], how='left', op='intersects')

#adm_grid['lon'] = adm_grid.geometry.x
#adm_grid['lat'] = adm_grid.geometry.y
adm_grid.drop(["geometry", "index_right"], axis=1, inplace=True)

adm_grid.to_csv(path+"/adm_grid.csv",index=False, encoding="utf-8")
