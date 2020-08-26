
path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"

import fiona
import itertools
import math
import numpy as np
import pandas as pd
from shapely.geometry import shape, Point, MultiPoint, MultiPolygon
from shapely.prepared import prep
import csv
import os
from osgeo import gdal, ogr
import sys
import errno
import geopandas as gpd
import rasterio
import re
from affine import Affine
from rasterstats.io import read_features
from rasterstats import zonal_stats, raster_stats


empty_grid = gpd.read_file(path+"/gadm36_KHM_3.geojson")

empty_grid["cell_id"] = empty_grid.index

#empty_grid["cell_id"] = range(1, 101)

temp = empty_grid.centroid
empty_grid["longitude"] = temp.x
empty_grid["latitude"] = temp.y
del temp

empty_grid = empty_grid[["cell_id", "longitude", "latitude", "geometry"]]

###

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

###

#temp = getValuesAtPoint(indir=path, rasterfileList=["Hansen_datamask_cambodia.tif"], pos=empty_grid, lon="longitude", lat="latitude", cell_id="cell_id")
#empty_grid = empty_grid[temp["Hansen_datamask_cambodia"]==1]
#del temp

###

#gain = rasterio.open(path+"/Hansen_gain_cambodia.tif")
#gain_array = gain.read(1)

mask = rasterio.open(path+"/Hansen_datamask_cambodia.tif")
mask_array = mask.read(1)
mask_array = (mask_array!=1) * 1

#pd.DataFrame(mask_array.flatten()).describe()
#main_array = ((gain_array+mask_array)>0) * 1
#main_array = (mask_array>0) * 1

treecover = rasterio.open(path+"/Hansen_treecover2000_cambodia.tif")
array = treecover.read(1)
array = (array>25) * 1
array[mask_array==1] = -9999
affine = treecover.transform

a = zonal_stats(empty_grid, array, affine=affine, stats=['mean'], nodata=-9999)
b = pd.DataFrame(a)
b.columns = ["treecover2000"]
grid = pd.concat([empty_grid.reset_index(drop=True), b], axis=1)

#grid.to_file("/Users/christianbaehr/Downloads/test.geojson", driver="GeoJSON")

#d = gpd.GeoDataFrame(c, geometry=c.geometry)
#d.to_file("/Users/christianbaehr/Downloads/test.geojson", driver="GeoJSON")

loss = rasterio.open(path+"/Hansen_lossyear_cambodia.tif")
loss_array = loss.read(1)

#loss_array_year = (loss_array==1) * 1
#loss_array_year[main_array==1] = -9999
loss_affine = loss.transform

for i in range(1, 18):
	loss_array_year = (loss_array==i) * 1
	loss_array_year[array==0] = 0
	loss_array_year[mask_array==1] = -9999
	#loss_affine = loss.transform
	a = zonal_stats(empty_grid, loss_array_year, affine=loss_affine, stats=["mean"], nodata=-9999)
	b = pd.DataFrame(a)
	c = grid["treecover"+str(1999+i)] - b["mean"]
	grid["treecover"+str(2000+i)] = c

##########

for i in range(2001, 2018):
	temperature = rasterio.open(path+"/temperature/temp_"+str(i)+".tif")
	temperature_array = temperature.read(1)
	temperature_affine = temperature.transform
	a = zonal_stats(empty_grid, temperature_array, affine=temperature_affine, stats=["mean"], nodata=-9999)
	b = pd.DataFrame(a)
	grid["temperature"+str(i)] = b


#rasters = ["temp_"+str(i)+".tif" for i in range(2001, 2018)]
#temp = getValuesAtPoint(indir=path+"/temperature", rasterfileList=rasters, pos=grid, lon="longitude", lat="latitude", cell_id="cell_id")
#temp = temp.drop(["cell_id", "x", "y"], axis=1)
#grid = pd.concat([grid, temp.reset_index(drop=True)], axis=1)


##########

#for i in range(1999, 2017):
#	precip = rasterio.open(path+"/precip/precip_"+str(i)+".tif")
#	precip_array = precip.read(1)
#	precip_affine = precip.transform
#	a = zonal_stats(empty_grid, precip_array, affine=precip_affine, stats=["mean"], nodata=-9999)
#	b = pd.DataFrame(a)
#	grid["precip"+str(i)] = b


rasters = ["precip_"+str(i)+".tif" for i in range(1999, 2017)]
temp = getValuesAtPoint(indir=path+"/precip", rasterfileList=rasters, pos=grid, lon="longitude", lat="latitude", cell_id="cell_id")
temp = temp.drop(["cell_id", "x", "y"], axis=1)
grid = pd.concat([grid, temp.reset_index(drop=True)], axis=1)

##########

grid_geometry = [Point(xy) for xy in zip(empty_grid.longitude, empty_grid.latitude)]
empty_grid_geo = gpd.GeoDataFrame(empty_grid['cell_id'], crs='epsg:4326', geometry=grid_geometry)

def build(year_str):
    j = year_str.split('|')
    return {i:j.count(i) for i in set(j)}

#treatment = gpd.read_file(path+"/pid/pid2003-18.geojson")
#treatment = gpd.read_file(path+"/pid/pid2003-18_trimmed.geojson")
treatment = pd.read_csv(path+"/pid/pid2003-18_trimmed.csv", encoding= 'unicode_escape')
#encoding= 'unicode_escape'
treatment_geometry = [Point(xy) for xy in zip(treatment.lon, treatment.lat)]
treatment_geo = gpd.GeoDataFrame(treatment, crs='epsg:4326', geometry=treatment_geometry)


activity_types = ["Rural Transport", "Irrigation", "Rural Domestic Water Supplies", "Urban transport", "Education", "other"]

for i in activity_types:
	if i=="other":
		treatment_temp = treatment_geo[~treatment_geo.activity_type.isin(["Rural Transport", "Irrigation", "Rural Domestic Water Supplies", "Urban transport", "Education"])]
	else:
		treatment_temp = treatment_geo[treatment_geo.activity_type==i].reset_index(drop=True)
	#treatment_temp = gpd.sjoin(empty_grid_geo, treatment_temp[['end_year', 'geometry']], how='left', op='intersects')
	treatment_temp = gpd.sjoin(empty_grid, treatment_temp[['end_year', 'geometry']], how='left', op='intersects')
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
		treatment_grid = pd.concat([empty_grid[["cell_id"]].reset_index(drop=True), treatment_grid_temp.reset_index(drop=True)], axis=1)
	else:
		treatment_grid = pd.concat([treatment_grid.reset_index(drop=True), treatment_grid_temp.reset_index(drop=True)], axis=1)

treatment_grid.drop(["cell_id"], axis=1, inplace=True)

grid = pd.concat([grid.reset_index(drop=True), treatment_grid.reset_index(drop=True)], axis=1)

#grid.to_file("/Users/christianbaehr/Downloads/test.geojson")



##########


adm = gpd.read_file(path+"/gadm36_KHM_3.geojson")

adm_grid = gpd.sjoin(empty_grid_geo, adm[["GID_1", "NAME_1", "GID_2", "NAME_2", "GID_3", "NAME_3", "geometry"]], how='left', op='intersects')

grid = pd.concat([grid, adm_grid[["GID_1", "NAME_1", "GID_2", "NAME_2", "GID_3", "NAME_3"]].reset_index(drop=True)], axis=1)

##########


pa = gpd.read_file(path+"/protected_areas.geojson")

#pa_grid = gpd.sjoin(pre_panel_centroid, pa[["issuedate", "geometry"]], how='left', op='intersects')
pa_grid = gpd.sjoin(empty_grid_geo, pa[["issuedate", "geometry"]], how='left', op='intersects')

pa_grid["issuedate"] = pd.to_datetime(pa_grid['issuedate'])

pa_grid = pa_grid.sort_values("issuedate", ascending=True).drop_duplicates("cell_id").sort_index()

pa_grid["pa_activedate"] = pa_grid["issuedate"].astype("str").str[:4]

#pa_grid.drop(["geometry", "index_right", "issuedate"], axis=1, inplace=True)

pa_grid = pa_grid.reset_index(drop=True)

###


elc = gpd.read_file(path+"/economic_land_concessions.geojson")

elc_grid = gpd.sjoin(empty_grid_geo, elc[["contract_0", "adjustment", "sub_decree", "last_updat", "geometry"]], how='left', op='intersects')

elc_grid["contract_0"] = pd.to_datetime(elc_grid["contract_0"], errors="coerce")
elc_grid["sub_decree"] = pd.to_datetime(elc_grid["sub_decree"], errors="coerce")

elc_grid1 = elc_grid.sort_values("contract_0", ascending=True).drop_duplicates("cell_id").sort_index()
elc_grid2 = elc_grid.sort_values("sub_decree", ascending=False).drop_duplicates("cell_id").sort_index()

elc_grid1.drop(["geometry", "index_right", "adjustment", "sub_decree", "last_updat"], axis=1, inplace=True)
elc_grid2.drop(["cell_id", "geometry", "index_right", "contract_0", "last_updat"], axis=1, inplace=True)

elc_grid_new = pd.concat([elc_grid1, elc_grid2], axis=1)

elc_grid_new["contract_0"] = elc_grid_new["contract_0"].astype("str").str[:4]
elc_grid_new["sub_decree"] = elc_grid_new["sub_decree"].astype("str").str[:4]

elc_grid_new.columns = ["cell_id", "elc_active_date", "elc_adjustment", "elc_change_date"]

elc_grid_new = elc_grid_new.reset_index(drop=True)

###


plantation = gpd.read_file(path+"/tree_plantations.geojson")

plantation_grid = gpd.sjoin(empty_grid_geo, plantation[["type_text", "geometry"]], how='left', op='intersects')

plantation_grid = plantation_grid.drop_duplicates("cell_id")

plantation_grid.drop(["geometry", "index_right"], axis=1, inplace=True)

plantation_grid["plantation"] = ~pd.isnull(plantation_grid["type_text"]) * 1

plantation_grid.columns = ["cell_id", "plantation_type", "plantation_dummy"]

plantation_grid = plantation_grid.reset_index(drop=True)

###

grid = pd.concat([grid, pa_grid[["issuedate", "pa_activedate"]], elc_grid_new[["elc_active_date", "elc_adjustment", "elc_change_date"]], plantation_grid[["plantation_type", "plantation_dummy"]]], axis=1)


##########



pa_grid_temp = grid["pa_activedate"]

for i in range(1993, 1999):
	pa_grid_temp[pa_grid_temp==str(i)] = "1999"

test = list(map(build, pa_grid_temp))

pa_grid_temp = pd.DataFrame(test)

for i in range(1999, 2019):
	if str(i) not in pa_grid_temp.columns:
		pa_grid_temp[str(i)] = 0

keep_cols = [str(i) for i in range(1999, 2019)]
pa_grid_temp = pa_grid_temp[keep_cols]

pa_grid_temp = pa_grid_temp.fillna(0)

pa_grid_temp = pa_grid_temp.apply(np.cumsum, axis=1)

pa_grid_temp.columns = ["protected_area_"+str(i) for i in range(1999, 2019)]

grid.drop(labels="pa_activedate", axis=1, inplace=True)

grid = pd.concat([grid.reset_index(drop=True), pa_grid_temp.reset_index(drop=True)], axis=1)

#del pa_grid_temp, test

###


grid.loc[grid["elc_active_date"]=="NaT", "elc_active_date"] = grid.loc[grid["elc_active_date"]=="NaT", "elc_change_date"]

elc_grid_temp = grid["elc_active_date"]

for i in range(1996, 1999):
	elc_grid_temp[elc_grid_temp==str(i)] = "1999"

test = list(map(build, elc_grid_temp))

elc_grid_temp = pd.DataFrame(test)

elc_grid_temp.drop(labels="NaT", axis=1, inplace=True)

for i in range(1999, 2019):
	if str(i) not in elc_grid_temp.columns:
		elc_grid_temp[str(i)] = 0

keep_cols = [str(i) for i in range(1999, 2019)]

elc_grid_temp = elc_grid_temp[keep_cols]

elc_grid_temp = elc_grid_temp.fillna(0)

elc_grid_temp = elc_grid_temp.apply(np.cumsum, axis=1)

elc_grid_temp.columns = ["land_concession_"+str(i) for i in range(1999, 2019)]

grid.drop(labels=["elc_active_date", "elc_change_date"], axis=1, inplace=True)

grid = pd.concat([grid.reset_index(drop=True), elc_grid_temp.reset_index(drop=True)], axis=1)

#del elc_grid_temp, test

#########


temp = getValuesAtPoint(indir=path, rasterfileList=["distance_to_city.tif"], pos=grid, lon="longitude", lat="latitude", cell_id="cell_id")

grid = pd.concat([grid, temp["distance_to_city"].reset_index(drop=True)], axis=1)

###


multi_treatment = gpd.read_file(path+"/pid/pid2003-18_trimmed_multiring.geojson")
#multi_treatment_temp = multi_treatment.sample(100)
multi_treatment_temp = multi_treatment
multi_treatment_temp["mrb_dist"] = multi_treatment_temp["mrb_dist"].astype(int)

del multi_treatment

for i in [1000, 2000, 3000, 4000, 5000]:
	temp = multi_treatment_temp.loc[multi_treatment_temp["mrb_dist"]==i]
	treatment_temp = gpd.sjoin(empty_grid_geo, temp[['end_year', 'geometry']], how='left', op='intersects')
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
	treatment_grid_temp.columns = ["treatment"+str(i)+"_"+str(j) for j in range(1999, 2019)]
	if i==1000:
		treatment_grid = pd.concat([empty_grid[["cell_id"]].reset_index(drop=True), treatment_grid_temp.reset_index(drop=True)], axis=1)
	else:
		treatment_grid = pd.concat([treatment_grid.reset_index(drop=True), treatment_grid_temp.reset_index(drop=True)], axis=1)

treatment_grid.drop(labels=["cell_id"], axis=1, inplace=True)

grid = pd.concat([grid.reset_index(drop=True), treatment_grid.reset_index(drop=True)], axis=1)

###

#for i in range(1, 18):
#	loss_array_year = (loss_array==i) * 1
#	loss_array_year[mask_array==1] = -9999
#	#loss_affine = loss.transform
#	a = zonal_stats(empty_grid, loss_array_year, affine=loss_affine, stats=["mean"], nodata=-9999)
#	b = pd.DataFrame(a)
#	grid["loss"+str(2000+i)] = b["mean"]

###

treatment_roadsonly = gpd.read_file(path+"/pid/pid_roadsonly_multiring.geojson")

treatment_temp = gpd.sjoin(empty_grid_geo, treatment_roadsonly[['end_year', 'geometry']], how='left', op='intersects')
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
treatment_grid_temp.columns = ["treatment_roadsonly"+str(i) for i in range(1999, 2019)]
#treatment_grid = pd.concat([empty_grid[["cell_id"]].reset_index(drop=True), treatment_grid_temp.reset_index(drop=True)], axis=1)

#grid = pd.concat([grid.reset_index(drop=True), treatment_grid.drop(["cell_id"], axis=1).reset_index(drop=True)], axis=1)

grid = pd.concat([grid.reset_index(drop=True), treatment_grid_temp.reset_index(drop=True)], axis=1)

###


for i in range(1999, 2019):
	ndvi = rasterio.open(path+"/ndvi/ndvi_landsat_"+str(i)+".tif")
	ndvi_array = ndvi.read(1)
	ndvi_array[ndvi_array<0] = -9999
	ndvi_affine = ndvi.transform
	a = zonal_stats(empty_grid, ndvi_array, affine=ndvi_affine, stats=["mean"], nodata=-9999)
	b = pd.DataFrame(a)
	grid["ndvi"+str(i)] = b

###

# #treatment_roadsonly = gpd.read_file(path+"/pid/pid_roadsonly_multiring.geojson")
# treatment_temp = gpd.sjoin(empty_grid_geo, treatment_roadsonly[['end_year', 'geometry']], how='left', op='intersects')
# 
# treatment_temp = treatment_temp[['cell_id', 'end_year']]
# treatment_temp['end_year'] = treatment_temp['end_year'].astype('Int64').astype('str')
# treatment_grid_temp = treatment_temp.pivot_table(values='end_year', index='cell_id', aggfunc='|'.join)
# treatment_grid_temp = treatment_grid_temp['end_year'].tolist()
# treatment_grid_temp = list(map(build, treatment_grid_temp))
# treatment_grid_temp = pd.DataFrame(treatment_grid_temp)
# 
# 
# for i in activity_types:
#   if i=="other":
#   treatment_temp = treatment[~treatment.activity_type.isin(["Rural Transport", "Irrigation", "Rural Domestic Water Supplies", "Urban transport", "Education"])]
# else:
#   treatment_temp = treatment[treatment.activity_type==i]
# treatment_temp = gpd.sjoin(empty_grid_geo, treatment_temp[['end_year', 'geometry']], how='left', op='intersects')
# treatment_temp = treatment_temp[['cell_id', 'end_year']]
# treatment_temp['end_year'] = treatment_temp['end_year'].astype('Int64').astype('str')
# treatment_grid_temp = treatment_temp.pivot_table(values='end_year', index='cell_id', aggfunc='|'.join)
# treatment_grid_temp = treatment_grid_temp['end_year'].tolist()
# treatment_grid_temp = list(map(build, treatment_grid_temp))
# treatment_grid_temp = pd.DataFrame(treatment_grid_temp)
# treatment_grid_temp = treatment_grid_temp.fillna(0)
# for j in range(1999, 2019):
#   if str(j) not in treatment_grid_temp.columns:
#   treatment_grid_temp[str(j)] = 0
# treatment_grid_temp = treatment_grid_temp.reindex(sorted(treatment_grid_temp.columns), axis=1)
# if '<NA>' in treatment_grid_temp.columns:
#   treatment_grid_temp.drop(labels='<NA>', axis=1, inplace=True)
# if '2019' in treatment_grid_temp.columns:
#   treatment_grid_temp.drop(labels='2019', axis=1, inplace=True)
# if "nan" in treatment_grid_temp.columns:
#   treatment_grid_temp.drop(labels="nan", axis=1, inplace=True)
# treatment_grid_temp = treatment_grid_temp.apply(np.cumsum, axis=1)
# treatment_grid_temp.columns = [i+str(j) for j in range(1999, 2019)]
# if i=="Rural Transport":
#   treatment_grid = pd.concat([empty_grid[["cell_id"]].reset_index(drop=True), treatment_grid_temp.reset_index(drop=True)], axis=1)
# else:
#   treatment_grid = pd.concat([treatment_grid.reset_index(drop=True), treatment_grid_temp.reset_index(drop=True)], axis=1)
# 
# treatment_grid.drop(["cell_id"], axis=1, inplace=True)
# 
# grid = pd.concat([grid, treatment_grid], axis=1)


#########

for i in grid.columns:
	print(i)


grid.to_csv(path+"/full_grid_hansen_commune.csv", index=False)

##########


for i in grid.columns:
	print(i)

names_order = ["cell_id", "longitude", "latitude", "GID_1", "NAME_1", "GID_2", "NAME_2", "GID_3", "NAME_3", "elc_adjustment", "plantation_type", "plantation_dummy", "distance_to_city"]

for i in ["treecover", "Rural Transport", "Irrigation", "Rural Domestic Water Supplies", "Urban transport", "Education", "other", "protected_area_", "land_concession_", "precip_", "temperature", "treatment1000_", "treatment2000_", "treatment3000_", "treatment4000_", "treatment5000_", "treatment_roadsonly", "ndvi"]:
	for j in range(1999, 2019):
		names_order = names_order + [i+str(j)]
		if i+str(j) not in grid.columns:
			grid[i+str(j)] = "NA"
grid = grid[names_order]


new_names = ["cell_id", "longitude", "latitude", "province_number", "province_name", "district_number", "district_name", "commune_number", "commune_name", "elc_adjustment", "plantation_type", "plantation_dummy", "distance_to_city"]
for i in ["treecover", "trt_rural_transport", "trt_irrigation", "trt_rural_domestic_water_supply", "trt_urban_transport", "trt_education", "trt_other", "protected_area", "land_concession", "precip", "temperature", "trt_1km", "trt_2km", "trt_3km", "trt_4km", "trt_5km", "trt_roadsonly", "ndvi"]:
	for j in range(1999, 2019):
		new_names = new_names + [i+str(j)]
names_dict = {}
for i in range(0, len(names_order)):
	names_dict[names_order[i]] = new_names[i]
grid.rename(columns=names_dict, inplace=True)

grid.dropna(axis=0, subset=["cell_id"], inplace=True)

grid.to_csv(path+"/pre_panel_hansen_commune.csv", index=False)



headers = [str(i) for i in range(1999, 2019)]
treecover_idx = ["treecover" in i for i in grid.columns]
trt_rural_transport_idx = ["trt_rural_transport" in i for i in grid.columns]
trt_irrigation_idx = ["trt_irrigation" in i for i in grid.columns]
trt_rural_domestic_water_supply_idx = ["trt_rural_domestic_water_supply" in i for i in grid.columns]
trt_urban_transport_idx = ["trt_urban_transport" in i for i in grid.columns]
trt_education_idx = ["trt_education" in i for i in grid.columns]
trt_other_idx = ["trt_other" in i for i in grid.columns]
precip_idx = ["precip" in i for i in grid.columns]
temperature_idx = ["temperature" in i for i in grid.columns]
protected_area_idx = ["protected_area" in i for i in grid.columns]
land_concession_idx = ["land_concession" in i for i in grid.columns]
trt_1km_idx = ["trt_1km" in i for i in grid.columns]
trt_2km_idx = ["trt_2km" in i for i in grid.columns]
trt_3km_idx = ["trt_3km" in i for i in grid.columns]
trt_4km_idx = ["trt_4km" in i for i in grid.columns]
trt_5km_idx = ["trt_5km" in i for i in grid.columns]
trt_roads_idx = ["trt_roadsonly" in i for i in grid.columns]
ndvi_idx = ["ndvi" in i for i in grid.columns]


del grid


with open(path+"/pre_panel_hansen_commune.csv") as f, open(path+"/panel_hansen_commune.csv", "w") as f2:
	a=f2.write("cell_id,year,longitude,latitude,province_number,province_name,district_number,district_name,commune_number,commune_name,elc_adjustment,plantation_type,plantation_dummy,distance_to_city,treecover,trt_rural_transport,trt_irrigation,trt_rural_domestic_water_supply,trt_urban_transport,trt_education,trt_other,precip,temperature,protected_area,land_concession,trt_1km,trt_2km,trt_3km,trt_4km,trt_5km,ndvi\n")
	for i, line in enumerate(f):
		if i>0:
			x = line.strip().split(",")
			cell, longitude, latitude, province_number, province_name, district_number, district_name, commune_number, commune_name, elc_adjustment, plantation_type, plantation_dummy, distance_to_city = x[0:13]
			treecover = list(itertools.compress(x, treecover_idx))
			trt1 = list(itertools.compress(x, trt_rural_transport_idx))
			trt2 = list(itertools.compress(x, trt_irrigation_idx))
			trt3 = list(itertools.compress(x, trt_rural_domestic_water_supply_idx))
			trt4 = list(itertools.compress(x, trt_urban_transport_idx))
			trt5 = list(itertools.compress(x, trt_education_idx))
			trt6 = list(itertools.compress(x, trt_other_idx))
			precip = list(itertools.compress(x, precip_idx))
			temperature = list(itertools.compress(x, temperature_idx))
			protected_area = list(itertools.compress(x, protected_area_idx))
			land_concession = list(itertools.compress(x, land_concession_idx))
			trt1km = list(itertools.compress(x, trt_1km_idx))
			trt2km = list(itertools.compress(x, trt_2km_idx))
			trt3km = list(itertools.compress(x, trt_3km_idx))
			trt4km = list(itertools.compress(x, trt_4km_idx))
			trt5km = list(itertools.compress(x, trt_5km_idx))
			ndvi = list(itertools.compress(x, ndvi_idx))
			for year, tc_out, trt1_out, trt2_out, trt3_out, trt4_out, trt5_out, trt6_out, precip_out, temperature_out, pa_out, lc_out, trt1km_out, trt2km_out, trt3km_out, trt4km_out, trt5km_out, ndvi_out in zip(headers, treecover, trt1, trt2, trt3, trt4, trt5, trt6, precip, temperature, protected_area, land_concession, trt1km, trt2km, trt3km, trt4km, trt5km, ndvi):
				a=f2.write(",".join([cell, year, longitude, latitude, province_number, province_name, district_number, district_name, commune_number, commune_name, elc_adjustment, plantation_type, plantation_dummy, distance_to_city, tc_out, trt1_out, trt2_out, trt3_out, trt4_out, trt5_out, trt6_out, precip_out, temperature_out, pa_out, lc_out, trt1km_out, trt2km_out, trt3km_out, trt4km_out, trt5km_out, ndvi_out])+'\n')










