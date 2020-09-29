
import pandas as pd
from shapely.geometry import shape, Point, MultiPoint, MultiPolygon
import geopandas as gpd

dat = pd.read_csv("/Users/christianbaehr/Downloads/1km_grid_mine.csv")
dat.drop([73186], axis=0, inplace=True)
dat.drop(["v2"], axis=1, inplace=True)
for i in dat.columns:
	print(i)

dat2 = pd.read_csv("/Users/christianbaehr/Downloads/grid_1km_ancillary.csv")
for i in dat2.columns:
	print(i)

dat3 = dat.merge(dat2, left_on="cell_id_x", right_on="cell_id_x")
dat3.drop(["cell_id", "cell_id_y"], axis=1, inplace=True)
for i in dat3.columns:
	print(i)


empty_grid = gpd.read_file("/Users/christianbaehr/Box Sync/cambodia/eba/inputData/empty_grid_1k.geojson")

dat4 = dat3.merge(empty_grid, left_on="cell_id_x", right_on="cell_id")
#for i in dat4.columns:
#	print(i)

dat4.drop(["cell_id", "geometry"], axis=1, inplace=True)

grid_geometry = [Point(xy) for xy in zip(dat4.lon, dat4.lat)]
grid_geo = gpd.GeoDataFrame(dat4['cell_id_x'], crs='epsg:4326', geometry=grid_geometry)


###

path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"

adm = gpd.read_file(path+"/gadm36_KHM_3.geojson")

adm_grid = gpd.sjoin(grid_geo, adm[["GID_1", "NAME_1", "GID_2", "NAME_2", "GID_3", "NAME_3", "geometry"]], how='left', op='intersects')

dat5 = pd.concat([dat4, adm_grid.drop(["cell_id_x", "geometry", "index_right"], axis=1)], axis=1)

###

dat5.to_csv("/Users/christianbaehr/Downloads/pre_panel_1km.csv", index=False)




