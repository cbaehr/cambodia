
path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterstats import zonal_stats
from shapely.geometry import Point


empty_grid = pd.read_csv(path+"/empty_grid_sample.csv")

########

def build(year_str):
    j = year_str.split('|')
    return {i:j.count(i) for i in set(j)}

treatment = gpd.read_file(path+"/pid/pid2003-18.geojson")

grid_geometry = [Point(xy) for xy in zip(empty_grid.longitude, empty_grid.latitude)]
empty_grid_geo = gpd.GeoDataFrame(empty_grid['cell_id'], crs='epsg:4326', geometry=grid_geometry)

activity_types = ["Rural Transport", "Irrigation", "Rural Domestic Water Supplies", "Urban transport", "Education"]

for i in activity_types:
	treatment_temp = treatment[treatment.activity_type==i]
	treatment_temp = gpd.sjoin(empty_grid_geo, treatment_temp[['end_year', 'geometry']], how='left', op='intersects')
	treatment_temp = treatment_temp[['cell_id', 'end_year']]
	treatment_temp['end_year'] = treatment_temp['end_year'].astype('Int64').astype('str')
	treatment_grid_temp = treatment_temp.pivot_table(values='end_year', index='cell_id', aggfunc='|'.join)
	treatment_grid_temp = treatment_grid_temp['end_year'].tolist()
	treatment_grid_temp = list(map(build, treatment_grid_temp))
	treatment_grid_temp = pd.DataFrame(treatment_grid_temp)
	treatment_grid_temp = treatment_grid_temp.fillna(0)
	for j in range(2003, 2019):
		if str(j) not in treatment_grid_temp.columns:
			treatment_grid_temp[str(j)] = 0
	treatment_grid_temp = treatment_grid_temp.reindex(sorted(treatment_grid_temp.columns), axis=1)
	if '<NA>' in treatment_grid_temp.columns:
		treatment_grid_temp.drop(labels='<NA>', axis=1, inplace=True)
	if '2019' in treatment_grid_temp.columns:
		treatment_grid_temp.drop(labels='2019', axis=1, inplace=True)
	treatment_grid_temp = treatment_grid_temp.apply(np.cumsum, axis=1)
	treatment_grid_temp.columns = [i+str(j) for j in range(2003, 2019)]
	if i=="Rural Transport":
		treatment_grid = pd.concat([empty_grid.reset_index(drop=True), treatment_grid_temp.reset_index(drop=True)], axis=1)
	else:
		treatment_grid = pd.concat([treatment_grid.reset_index(drop=True), treatment_grid_temp.reset_index(drop=True)], axis=1)

#########

for i in range(1999, 2019):
	ndvi = rasterio.open(path+"/ndvi/ndvi_"+str(i)+"_landsat.tif")
	array = ndvi.read(1)
	affine = ndvi.transform
	ndvi_grid_temp = zonal_stats(empty_grid_geo, array, affine=affine, stats=['mean'])
	ndvi_grid_temp = pd.DataFrame(ndvi_grid_temp)
	ndvi_grid_temp.columns = ["ndvi"+str(i)]
	if i==1999:
		ndvi_grid = pd.concat([empty_grid.reset_index(drop=True), ndvi_grid_temp.reset_index(drop=True)], axis=1)
	else:
		ndvi_grid = pd.concat([ndvi_grid.reset_index(drop=True), ndvi_grid_temp.reset_index(drop=True)], axis=1)

for i in range(2001, 2018):
	temperature = rasterio.open(path+"/temperature/temp_"+str(i)+".tif")
	array = temperature.read(1)
	affine = temperature.transform
	temperature_grid_temp = zonal_stats(empty_grid_geo, array, affine=affine, stats=['mean'])
	temperature_grid_temp = pd.DataFrame(temperature_grid_temp)
	temperature_grid_temp.columns = ["temperature"+str(i)]
	if i==2001:
		temperature_grid = pd.concat([empty_grid.reset_index(drop=True), temperature_grid_temp.reset_index(drop=True)], axis=1)
	else:
		temperature_grid = pd.concat([temperature_grid.reset_index(drop=True), temperature_grid_temp.reset_index(drop=True)], axis=1)

for i in range(1999, 2018):
	precip = rasterio.open(path+"/precip/precip_"+str(i)+".tif")
	array = precip.read(1)
	affine = precip.transform
	precip_grid_temp = zonal_stats(empty_grid_geo, array, affine=affine, stats=['mean'])
	precip_grid_temp = pd.DataFrame(precip_grid_temp)
	precip_grid_temp.columns = ["precip"+str(i)]
	if i==1999:
		precip_grid = pd.concat([empty_grid.reset_index(drop=True), precip_grid_temp.reset_index(drop=True)], axis=1)
	else:
		precip_grid = pd.concat([precip_grid.reset_index(drop=True), precip_grid_temp.reset_index(drop=True)], axis=1)








#mask=gdf_mask[gdf_mask.continent=="Africa"]
#treatment_grid.to_file("/Users/christianbaehr/Desktop/test.geojson", driver='GeoJSON')


for i in range(1999, 2003):
    full_grid['trt_'+str(i)] = 0
    full_grid['trt1k_'+str(i)] = 0
    full_grid['trt2k_'+str(i)] = 0
    full_grid['trt3k_'+str(i)] = 0

for i in list(range(1999, 2001))+[2018]:
    full_grid['temp_'+str(i)] = 'NA'

full_grid['precip_2018'] = 'NA'

for i in range(2014, 2019):
	full_grid['ntl_'+str(i)] = 'NA'

# reorder columns in main dataset
new_names = ['cell_id', 'commune', 'province', 'plantation', 'concession', 'protected_area', 'road_distance', 'bombings', 'burials', 'memorials', 'prisons'] + ['ndvi_' + str(i) for i in range(1999, 2019)] + ['trt_' + str(i) for i in range(1999, 2019)] + ['trt1k_' + str(i) for i in range(1999, 2019)] + ['trt2k_' + str(i) for i in range(1999, 2019)] + ['trt3k_' + str(i) for i in range(1999, 2019)] + ['temp_' + str(i) for i in range(1999, 2019)] + ['precip_' + str(i) for i in range(1999, 2019)] + ['ntl_' + str(i) for i in range(1999, 2019)]
full_grid = full_grid[new_names]

# drop observations with missing cell ID
full_grid.dropna(axis=0, subset=['cell_id'], inplace=True)

# write "pre panel" to csv file
if overwrite:
    full_grid.to_csv(out_dir+'/pre_panel.csv', index=False)

# identify column indices for each time-variant measure. Will need these indices for reshaping
headers = [str(i) for i in range(1999, 2019)]
ndvi_index = ['ndvi' in i for i in full_grid.columns]
trt_index = ['trt' in i for i in full_grid.columns]
trt1k_index = ['trt1k' in i for i in full_grid.columns]
trt2k_index = ['trt2k' in i for i in full_grid.columns]
trt3k_index = ['trt3k' in i for i in full_grid.columns]
temp_index = ['temp' in i for i in full_grid.columns]
precip_index = ['precip' in i for i in full_grid.columns]
ntl_index = ['ntl' in i for i in full_grid.columns]

del full_grid

# reshape panel from wide to long form
with open(out_dir+'/pre_panel.csv') as f, open(out_dir+'/panel.csv', 'w') as f2:
	# first line of the csv is variable names
    a=f2.write('cell_id,year,commune,province,plantation,concession,protected_area,road_distance,bombings,burials,memorials,prisons,ndvi,trt,trt1k,trt2k,trt3k,temp,precip,ntl\n')
    # performing transformation one grid cell at a time
    for i, line in enumerate(f):
        if i != 0:
            x = line.strip().split(',')
            cell, commune, province, plantation, concession, protected, distance = x[0:7]
            ndvi = list(itertools.compress(x, ndvi_index))
            trt = list(itertools.compress(x, trt_index))
            trt1k = list(itertools.compress(x, trt1k_index))
            trt2k = list(itertools.compress(x, trt2k_index))
            trt3k = list(itertools.compress(x, trt3k_index))
            temp = list(itertools.compress(x, temp_index))
            precip = list(itertools.compress(x, precip_index))
            ntl = list(itertools.compress(x, ntl_index))
            for year, ndvi_out, trt_out, trt1k_out, trt2k_out, trt3k_out, temp_out, precip_out, ntl_out in zip(headers, ndvi, trt, trt1k, trt2k, trt3k, temp, precip, ntl):
                a=f2.write(','.join([cell, year, commune, province, plantation, concession, protected, distance, bombings, burials, memorials, prisons, ndvi_out, trt_out, trt1k_out, trt2k_out, trt3k_out, temp_out, precip_out, ntl_out])+'\n')





















