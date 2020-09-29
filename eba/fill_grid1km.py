
path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"
#path = "/sciclone/home20/cbaehr/cambodia/eba/inputData"

import pandas as pd
import geopandas as gpd
from shapely.geometry import shape, Point, MultiPoint, MultiPolygon
import numpy as np
from osgeo import gdal, ogr
import re
import itertools


pre_panel = pd.read_csv(path+"/pre_panel.csv")

pre_panel = pre_panel[["cell_id", "longitude", "latitude"]]

pre_panel_geometry = [Point(xy) for xy in zip(pre_panel.longitude, pre_panel.latitude)]
pre_panel.drop(["longitude", "latitude"], axis=1, inplace=True)
pre_panel_geo = gpd.GeoDataFrame(pre_panel, crs='epsg:4326', geometry=pre_panel_geometry)

del pre_panel, pre_panel_geometry

###

empty_grid_1km = gpd.read_file(path+"/empty_grid_1km.geojson")
empty_grid_1km.crs = "epsg:4326"

empty_grid_1km.drop(["lon", "lat"], axis=1, inplace=True)

grid = gpd.sjoin(empty_grid_1km, pre_panel_geo, how="right", op="intersects")
grid.drop(["index_left", "geometry"], axis=1, inplace=True)

del empty_grid_1km

pre_panel = pd.read_csv(path+"/pre_panel.csv")
drop_names = ["longitude", "latitude", "province_number", "province_name", "district_number", "district_name", "commune_number", "commune_name"]
pre_panel.drop(drop_names, axis=1, inplace=True)

full_grid = grid.merge(pre_panel, left_on="cell_id_y", right_on="cell_id")
full_grid.drop(["cell_id_y", "cell_id"], axis=1, inplace=True)

del pre_panel

for i in range(1999, 2019):
	full_grid.loc[full_grid["ndvi"+str(i)]<=0, "ndvi"+str(i)] = np.nan
	full_grid.loc[full_grid["temperature"+str(i)]<=0, "temperature"+str(i)] = np.nan
	full_grid.loc[(full_grid["precip"+str(i)]<=0) | (full_grid["precip"+str(i)]>1000), "precip"+str(i)] = np.nan

grid_1km = full_grid.groupby("cell_id_x").agg(["mean"])

full_grid["count_var"]=1
temp = full_grid[["cell_id_x", "count_var"]].groupby("cell_id_x").agg(["count"])

del full_grid

grid_1km.columns = grid_1km.columns.get_level_values(0)
grid_1km["cell_id"] = grid_1km.index
grid_1km["count"] = temp[["count_var"]]

empty_grid_1km = gpd.read_file(path+"/empty_grid_1km.geojson")
empty_grid_1km.crs = "epsg:4326"

grid_1km_data = grid_1km.merge(empty_grid_1km, left_on='cell_id', right_on='cell_id')

#for i in grid_1km_data.columns:
#	print(i)

grid = grid_1km_data

del grid_1km_data

grid["lat"] = grid.geometry.centroid.y
grid["lon"] = grid.geometry.centroid.x

gpd.GeoDataFrame(grid_1km_data, crs="epsg:4326", geometry=grid_1km_data["geometry"]).to_file(path+"/grid_1km.geojson", driver="GeoJSON")
grid_1km_data.drop(["geometry"], axis=1).to_csv(path+"/grid_1km.csv", index=False)

###########################################################################



def getValuesAtPoint(indir, rasterfileList, pos, lon, lat, cell_id):
    #gt(2) and gt(4) coefficients are zero, and the gt(1) is pixel width, and gt(5) is pixel height.
    #The (gt(0),gt(3)) position is the top left corner of the top left pixel of the raster.
    for i, rs in enumerate(rasterfileList):
        presValues = []
        gdata = gdal.Open('{}/{}'.format(indir,rs))
        gt = gdata.GetGeoTransform()
        band = gdata.GetRasterBand(1)
        nodata = band.GetNoDataValue()
        x0, y0 , w , h = gt[0], gt[3], gt[1], gt[5]
        data = band.ReadAsArray().astype(np.float)
        params = data.shape
        #free memory
        del gdata
        if i == 0:
            #iterate through the points
            for p in pos.iterrows():
                x = int((p[1][lon] - x0)/w)
                y = int((p[1][lat] - y0)/h)
                if y < params[0] and x < params[1]:
                    val = data[y,x]
                else:
                    val = -9999
                presVAL = [p[1][cell_id], p[1][lon], p[1][lat], val]
                presValues.append(presVAL)
            df = pd.DataFrame(presValues, columns=['cell_id', 'x', 'y', re.sub(".tif", "", rs)])
        else:
            #iterate through the points
            for p in pos.iterrows():
                x = int((p[1][lon] - x0)/w)
                y = int((p[1][lat] - y0)/h)
                if y < params[0] and x < params[1]:
                    val = data[y,x]
                else:
                    val = -9999
                presValues.append(val)
            df[re.sub(".tif", "", rs)] = pd.Series(presValues)
    del data, band
    return df


rasters = ["distance_to_city.tif"]

new_grid = getValuesAtPoint(indir=path, rasterfileList=rasters, pos=grid, lon="lon", lat="lat", cell_id="cell_id")

grid = pd.concat([grid, new_grid.reset_index(drop=True).drop(["cell_id", "x", "y"], axis=1)], axis=1)


###########################################################################



grid_geometry = [Point(xy) for xy in zip(grid.lon, grid.lat)]
grid_geo = gpd.GeoDataFrame(grid['cell_id'], crs='epsg:4326', geometry=grid_geometry)

###

adm = gpd.read_file(path+"/gadm36_KHM_3.geojson")

adm_grid = gpd.sjoin(grid_geo, adm[["GID_1", "NAME_1", "GID_2", "NAME_2", "GID_3", "NAME_3", "geometry"]], how='left', op='intersects')

grid = pd.concat([grid, adm_grid.drop(["cell_id", "geometry", "index_right"], axis=1)], axis=1)

###

variable_order = ["cell_id", "lon", "lat", "count", "GID_1", "NAME_1", "GID_2", "NAME_2", "GID_3", "NAME_3", "geometry"]

for i in ["treecover", "ndvi", "trt1km", "trt2km", "trt3km", "trt4km", "trt5km", "temperature", "precip"]:
	for j in range(1999, 2019):
		variable_order = variable_order + [i+str(j)]
		if i+str(j) not in grid.columns:
			grid[i+str(j)] = "NA"

grid = grid[variable_order]

grid.dropna(axis=0, subset=["cell_id"], inplace=True)

grid.to_file(path+"/pre_panel_1km.geojson", driver="GeoJSON")

grid.drop(["geometry"], axis=1, inplace=True)
grid.to_csv(path+"/pre_panel_1km.csv", index=False)

###

headers = [str(i) for i in range(1999, 2019)]
treecover_idx = ["treecover" in i for i in grid.columns]
ndvi_idx = ["ndvi" in i for i in grid.columns]
trt1km_idx = ["trt1km" in i for i in grid.columns]
trt2km_idx = ["trt2km" in i for i in grid.columns]
trt3km_idx = ["trt3km" in i for i in grid.columns]
trt4km_idx = ["trt4km" in i for i in grid.columns]
trt5km_idx = ["trt5km" in i for i in grid.columns]
temperature_idx = ["temperature" in i for i in grid.columns]
precip_idx = ["precip" in i for i in grid.columns]

del grid

with open(path+"/pre_panel_1km.csv") as f, open(path+"/panel_1km.csv", "w") as f2:
	a=f2.write("cell_id,year,longitude,latitude,count,province_id,province_name,district_id,district_name,commune_id,commune_name,treecover,ndvi,trt1km,trt2km,trt3km,trt4km,trt5km,temperature,precip\n")
	for i, line in enumerate(f):
		if i>0:
			x = line.strip().split(",")
			cell, longitude, latitude, count, province_id, province_name, district_id, district_name, commune_id, commune_name = x[0:10]
			treecover = list(itertools.compress(x, treecover_idx))
			ndvi = list(itertools.compress(x, ndvi_idx))
			trt1km = list(itertools.compress(x, trt1km_idx))
			trt2km = list(itertools.compress(x, trt2km_idx))
			trt3km = list(itertools.compress(x, trt3km_idx))
			trt4km = list(itertools.compress(x, trt4km_idx))
			trt5km = list(itertools.compress(x, trt5km_idx))
			temperature = list(itertools.compress(x, temperature_idx))
			precip = list(itertools.compress(x, precip_idx))
			for year, tc_out, ndvi_out, trt1km_out, trt2km_out, trt3km_out, trt4km_out, trt5km_out, temperature_out, precip_out in zip(headers, treecover, ndvi, trt1km, trt2km, trt3km, trt4km, trt5km, temperature, precip):
				a=f2.write(",".join([cell, year, longitude, latitude, count, province_id, province_name, district_id, district_name, commune_id, commune_name, tc_out, ndvi_out, trt1km_out, trt2km_out, trt3km_out, trt4km_out, trt5km_out, temperature_out, precip_out])+'\n')


























