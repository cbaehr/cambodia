
#path = "/sciclone/home20/cbaehr/cambodia/eba/inputData"
path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"
#path = "/home/cdsw/inputData"

import geopandas as gpd
import numpy as np
from osgeo import gdal, gdalconst
import os
import pandas as pd
import rasterio
from rasterstats import zonal_stats
import re
from shapely.geometry import Point
import itertools

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

empty_grid = gpd.read_file(path+"/cambodia_template_1kmgrid.geojson")

centroid = empty_grid.geometry.centroid
empty_grid["lon"] = centroid.x
empty_grid["lat"] = centroid.y

#empty_grid = empty_grid.sample(1000)
empty_grid = empty_grid.reset_index(drop=True)

###

temp = getValuesAtPoint(indir=path, rasterfileList=["Hansen_datamask_cambodia.tif"], pos=empty_grid, lon="lon", lat="lat", cell_id="id")

empty_grid = empty_grid.loc[temp["Hansen_datamask_cambodia"]==1]

###


grid_geometry = [Point(xy) for xy in zip(empty_grid.lon, empty_grid.lat)]
empty_grid_geo = gpd.GeoDataFrame(empty_grid['id'], crs='epsg:4326', geometry=grid_geometry)
#empty_grid_geo = gpd.GeoDataFrame(empty_grid['id'], crs={'init': 'epsg:4326'}, geometry=grid_geometry)

adm = gpd.read_file(path+"/gadm36_KHM_3.geojson")

adm_grid = gpd.sjoin(empty_grid_geo, adm[["GID_1", "NAME_1", "GID_2", "NAME_2", "GID_3", "NAME_3", "geometry"]], how='left', op='intersects')

#adm_grid['lon'] = adm_grid.geometry.x
#adm_grid['lat'] = adm_grid.geometry.y
#adm_grid.drop(["geometry", "index_right"], axis=1, inplace=True)

#adm_grid.to_csv(path+"/adm_grid_hansen.csv",index=False, encoding="utf-8")

##########


pa = gpd.read_file(path+"/protected_areas.geojson")

#pa_grid = gpd.sjoin(pre_panel_centroid, pa[["issuedate", "geometry"]], how='left', op='intersects')
pa_grid = gpd.sjoin(empty_grid_geo, pa[["issuedate", "geometry"]], how='left', op='intersects')

pa_grid["issuedate"] = pd.to_datetime(pa_grid['issuedate'])

pa_grid = pa_grid.sort_values("issuedate", ascending=True).drop_duplicates("id").sort_index()

pa_grid["pa_activedate"] = pa_grid["issuedate"].astype("str").str[:4]

#pa_grid.drop(["geometry", "index_right", "issuedate"], axis=1, inplace=True)

###


elc = gpd.read_file(path+"/economic_land_concessions.geojson")

elc_grid = gpd.sjoin(empty_grid_geo, elc[["contract_0", "adjustment", "sub_decree", "last_updat", "geometry"]], how='left', op='intersects')

elc_grid["contract_0"] = pd.to_datetime(elc_grid["contract_0"], errors="coerce")
elc_grid["sub_decree"] = pd.to_datetime(elc_grid["sub_decree"], errors="coerce")

elc_grid1 = elc_grid.sort_values("contract_0", ascending=True).drop_duplicates("id").sort_index()
elc_grid2 = elc_grid.sort_values("sub_decree", ascending=False).drop_duplicates("id").sort_index()

elc_grid1.drop(["geometry", "index_right", "adjustment", "sub_decree", "last_updat"], axis=1, inplace=True)
elc_grid2.drop(["id", "geometry", "index_right", "contract_0", "last_updat"], axis=1, inplace=True)

elc_grid_new = pd.concat([elc_grid1, elc_grid2], axis=1)

elc_grid_new["contract_0"] = elc_grid_new["contract_0"].astype("str").str[:4]
elc_grid_new["sub_decree"] = elc_grid_new["sub_decree"].astype("str").str[:4]

elc_grid_new.columns = ["id", "elc_active_date", "elc_adjustment", "elc_change_date"]

###


plantation = gpd.read_file(path+"/tree_plantations.geojson")

plantation_grid = gpd.sjoin(empty_grid_geo, plantation[["type_text", "geometry"]], how='left', op='intersects')

plantation_grid = plantation_grid.drop_duplicates("id")



plantation_grid.drop(["geometry", "index_right"], axis=1, inplace=True)

plantation_grid["plantation"] = ~pd.isnull(plantation_grid["type_text"]) * 1

plantation_grid.columns = ["cell_id", "plantation_type", "plantation_dummy"]

##########


hansen_grid = empty_grid[["id", "lon", "lat"]]
hansen_grid = hansen_grid.reset_index(drop=True)

gain = rasterio.open(path+"/Hansen_gain_cambodia.tif")
gain_array = gain.read(1)
#gain_array==1

#if not os.path.exists(path+"/cambodia_1kmgrid.geojson"):
treecover = rasterio.open(path+"/treecover2000_cambodia_binary.tif")
array = treecover.read(1)
array[gain_array==1] = 100

affine = treecover.transform
#grid = gpd.read_file(path+"/cambodia_template_1kmgrid.geojson")
stats = zonal_stats(empty_grid, array, affine=affine, stats=['mean'], nodata=100)
hansen_grid['pcttreecover2000'] = pd.DataFrame(stats)

base = gdal.Open(path+"/Hansen_lossyear_cambodia.tif")
driver_tiff = gdal.GetDriverByName("GTiff")
band_base = base.GetRasterBand(1).ReadAsArray()
fn_new = path+"/temp.tif"
for i in range(1, 19):
	ds_new = driver_tiff.CreateCopy(fn_new, base, strict=0)
	band_new = band_base==i
	ds_new.GetRasterBand(1).WriteArray(band_new)
	del ds_new
	#now convert
	loss_raster = rasterio.open(path+"/temp.tif")
	array = loss_raster.read(1)
	array[gain_array==1] = 100
	affine = loss_raster.transform
	stats = zonal_stats(empty_grid, array, affine=affine, stats=['mean'], nodata=100)
	hansen_grid['pcttreecover'+str(i+2000)] = hansen_grid['pcttreecover'+str(i+1999)] - pd.DataFrame(stats)['mean']

#hansen_grid.to_csv(path+"/hansen_grid_hansen.csv", index=False)

###


ndvi_grid = empty_grid[["id", "lon", "lat"]]

ndvi_grid = ndvi_grid.reset_index(drop=True)

for i in range(1999, 2019):
	ndvi = rasterio.open(path+"/ndvi/ndvi_landsat_"+str(i)+".tif")
	array = ndvi.read(1)
	array[array<0] = -9999
	affine = ndvi.transform
	stats = zonal_stats(empty_grid, array, affine=affine, stats=['mean'], nodata=-9999)
	ndvi_grid['ndvi'+str(i)] = pd.DataFrame(stats) * 0.0001

#ndvi_grid.to_csv(path+"/ndvi_grid_hansen.csv", index=False)
#grid.to_file(path+"/cambodia_1kmgrid.geojson", driver="GeoJSON")

###


def build(year_str):
    j = year_str.split('|')
    return {i:j.count(i) for i in set(j)}

treatment = gpd.read_file(path+"/pid/pid2003-18.geojson")

#grid_geometry = [Point(xy) for xy in zip(empty_grid.longitude, empty_grid.latitude)]
#empty_grid_geo = gpd.GeoDataFrame(empty_grid['cell_id'], crs={'init': 'epsg:4326'}, geometry=grid_geometry)

activity_types = ["Rural Transport", "Irrigation", "Rural Domestic Water Supplies", "Urban transport", "Education", "other"]

for i in activity_types:
	if i=="other":
		treatment_temp = treatment[~treatment.activity_type.isin(["Rural Transport", "Irrigation", "Rural Domestic Water Supplies", "Urban transport", "Education"])]
	else:
		treatment_temp = treatment[treatment.activity_type==i]
	treatment_temp = gpd.sjoin(empty_grid_geo, treatment_temp[['end_year', 'geometry']], how='left', op='intersects')
	treatment_temp = treatment_temp[['id', 'end_year']]
	treatment_temp['end_year'] = treatment_temp['end_year'].astype('Int64').astype('str')
	treatment_grid_temp = treatment_temp.pivot_table(values='end_year', index='id', aggfunc='|'.join)
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
		treatment_grid = pd.concat([empty_grid.reset_index(drop=True), treatment_grid_temp.reset_index(drop=True)], axis=1)
	else:
		treatment_grid = pd.concat([treatment_grid.reset_index(drop=True), treatment_grid_temp.reset_index(drop=True)], axis=1)

#treatment_grid.to_csv(path+"/treatment_grid.csv",index=False)

###


#temperature_grid = empty_grid[["id", "lon", "lat"]]

#temperature_grid = temperature_grid.reset_index(drop=True)

#for i in range(1999, 2019):
#	temperature = rasterio.open(path+"/temperature30m/temperature30m"+str(i)+".tif")
#	array = ndvi.read(1)
#	array[array<0] = -9999
#	affine = ndvi.transform
#	stats = zonal_stats(empty_grid, array, affine=affine, stats=['mean'], nodata=-9999)
#	ndvi_grid['ndvi'+str(i)] = pd.DataFrame(stats) * 0.0001

#ndvi_grid.to_csv(path+"/ndvi_grid_hansen.csv", index=False)

###

temperature_grid = empty_grid[["id", "lon", "lat"]]

ndvi_grid = ndvi_grid.reset_index(drop=True)

for i in range(1999, 2019):
	temperature = rasterio.open(path+"/temperature30m/temperature30m_"+str(i)+".tif")
	array = temperature.read(1)
	affine = temperature.transform
	stats = zonal_stats(empty_grid, array, affine=affine, stats=['mean'])
	temperature_grid['temperature'+str(i)] = pd.DataFrame(stats)

###

precip_grid = empty_grid[["id", "lon", "lat"]]


for i in range(1999, 2019):
	precip = rasterio.open(path+"/precip30m/precip30m_"+str(i)+".tif")
	array = precip.read(1)
	affine = precip.transform
	stats = zonal_stats(empty_grid, array, affine=affine, stats=['mean'])
	precip_grid['precip'+str(i)] = pd.DataFrame(stats)


#########

empty_grid = empty_grid[["id", "lon", "lat"]]
adm_grid.drop(["id", "geometry", "index_right"], axis=1, inplace=True)
pa_grid = pa_grid[["pa_activedate"]]
elc_grid_new = elc_grid_new[["elc_active_date", "elc_adjustment", "elc_change_date"]]
plantation_grid = plantation_grid[["plantation_type", "plantation_dummy"]]
hansen_grid.drop(["id", "lon", "lat"], axis=1, inplace=True)
ndvi_grid.drop(["id", "lon", "lat"], axis=1, inplace=True)
treatment_grid.drop(["id", "lon", "lat", 'left', 'top', 'right', 'bottom', 'geometry'], axis=1, inplace=True)
temperature_grid.drop(["id", "lon", "lat"], axis=1, inplace=True)
precip_grid.drop(["id", "lon", "lat"], axis=1, inplace=True)

grid = pd.concat([empty_grid, adm_grid, pa_grid, elc_grid_new, plantation_grid, hansen_grid, ndvi_grid, treatment_grid, precip_grid, temperature_grid], axis=1)

grid.to_csv(path+"/full_grid_hansen.csv", index=False)













