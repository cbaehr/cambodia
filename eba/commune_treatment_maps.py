
path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"

out_path = "/Users/christianbaehr/Box Sync/cambodia/eba/new_results"

import pandas as pd
import geopandas as gpd
import rasterio
from rasterstats import zonal_stats, raster_stats

#########

geometry = gpd.read_file(path+"/gadm36_KHM_3.geojson")

pid = gpd.read_file(path+"/pid/pid2003-18_trimmed.geojson")
pid["geometry"] = pid["geometry"].centroid

pid_tight = pid.loc[pid["end_year"]<2004]
test = gpd.sjoin(geometry, pid_tight, how="right")
test2 = test[["end_year", "GID_3", "geometry"]]
test3 = test2.groupby("GID_3").agg("count")
test3["id"] = test3.index
test3.rename(columns={"end_year":"projectcount2003"}, inplace=True)
geometry = geometry.merge(test3.drop(["geometry"],axis=1), how="left", left_on="GID_3", right_on="id")

pid_tight = pid.loc[pid["end_year"]<2009]
test = gpd.sjoin(geometry, pid_tight, how="right")
test2 = test[["end_year", "GID_3", "geometry"]]
test3 = test2.groupby("GID_3").agg("count")
test3["id"] = test3.index
test3.rename(columns={"end_year":"projectcount2008"}, inplace=True)
geometry = geometry.merge(test3.drop(["geometry"],axis=1), how="left", left_on="GID_3", right_on="id")

pid_tight = pid.loc[pid["end_year"]<2014]
test = gpd.sjoin(geometry, pid_tight, how="right")
test2 = test[["end_year", "GID_3", "geometry"]]
test3 = test2.groupby("GID_3").agg("count")
test3["id"] = test3.index
test3.rename(columns={"end_year":"projectcount2013"}, inplace=True)
geometry = geometry.merge(test3.drop(["geometry"],axis=1), how="left", left_on="GID_3", right_on="id")

pid_tight = pid.loc[pid["end_year"]<2019]
test = gpd.sjoin(geometry, pid_tight, how="right")
test2 = test[["end_year", "GID_3", "geometry"]]
test3 = test2.groupby("GID_3").agg("count")
test3["id"] = test3.index
test3.rename(columns={"end_year":"projectcount2018"}, inplace=True)
geometry = geometry.merge(test3.drop(["geometry"],axis=1), how="left", left_on="GID_3", right_on="id")

a = gpd.read_file(path+"/gadm36_KHM_3.geojson")

geometry_out = geometry[["GID_3", "projectcount2003", "projectcount2008", "projectcount2013", "projectcount2018"]]

out = gpd.GeoDataFrame(geometry_out, crs="epsg:4326", geometry=a["geometry"])

pop = rasterio.open(path+"/2000populationcountGPW.tif")
array = pop.read(1)
affine = pop.transform

a = zonal_stats(out, array, affine=affine, stats=['sum'], nodata=-9999)
b = pd.DataFrame(a)
b.columns = ["treecover2000"]

for i in [2003, 2008, 2013, 2018]:
	out.loc[out["projectcount"+str(i)].isnull(), "projectcount"+str(i)] = 0
	out["projectcount_pk"+str(i)] = out["projectcount"+str(i)]/out["geometry"].area
	out["projectcount_pc"+str(i)] = out["projectcount"+str(i)]/b["treecover2000"]

out.to_file(out_path+"/commune_map_data.geojson", driver="GeoJSON")


























