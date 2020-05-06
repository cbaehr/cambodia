
path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"

import geopandas as gpd
import itertools
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

activity_types = ["Rural Transport", "Irrigation", "Rural Domestic Water Supplies", "Urban transport", "Education", "other"]

for i in activity_types:
	if i=="other":
		treatment_temp = treatment[~treatment.activity_type.isin(["Rural Transport", "Irrigation", "Rural Domestic Water Supplies", "Urban transport", "Education"])]
	else:
		treatment_temp = treatment[treatment.activity_type==i]
	treatment_temp = gpd.sjoin(empty_grid_geo, treatment_temp[['end_year', 'geometry']], how='left', op='intersects')
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
	treatment_grid_temp = treatment_grid_temp.apply(np.cumsum, axis=1)
	treatment_grid_temp.columns = [i+str(j) for j in range(1999, 2019)]
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


#########

adm = gpd.read_file(path+"/gadm36_KHM_3.geojson")
adm_grid = gpd.sjoin(empty_grid_geo, adm[["GID_1", "NAME_1", "GID_2", "NAME_2", "GID_3", "NAME_3", "geometry"]], how='left', op='intersects')
#adm_grid.drop(["cell_id", "geometry", "index_right"], axis=1, inplace=True)

grid = pd.concat([empty_grid.reset_index(drop=True), 
					adm_grid.drop(["cell_id", "geometry", "index_right"], axis=1).reset_index(drop=True),
					treatment_grid.drop(labels=["latitude", "longitude", "cell_id"], axis=1).reset_index(drop=True), 
					ndvi_grid.drop(labels=["latitude", "longitude", "cell_id"], axis=1).reset_index(drop=True), 
					temperature_grid.drop(labels=["latitude", "longitude", "cell_id"], axis=1).reset_index(drop=True),
					precip_grid.drop(labels=["latitude", "longitude", "cell_id"], axis=1).reset_index(drop=True)], 
					axis=1)

for i in range(1999, 2019):
	if "ndvi"+str(i) not in grid.columns:
		grid["ndvi"+str(i)] = "NA"
	if "temperature"+str(i) not in grid.columns:
		grid["temperature"+str(i)] = "NA"
	if "precip"+str(i) not in grid.columns:
		grid["precip"+str(i)] = "NA"


new_names = ["latitude", "longitude", "cell_id", "GID_1", "NAME_1", "GID_2", "NAME_2", "GID_3", "NAME_3"] + ["Rural Transport" + str(i) for i in range(1999, 2019)] + ["Irrigation" + str(i) for i in range(1999, 2019)] + ["Rural Domestic Water Supplies" + str(i) for i in range(1999, 2019)] + ["Urban transport" + str(i) for i in range(1999, 2019)] + ["Education" + str(i) for i in range(1999, 2019)] + ["other" + str(i) for i in range(1999, 2019)] + ["ndvi" + str(i) for i in range(1999, 2019)] + ["temperature" + str(i) for i in range(1999, 2019)] + ["precip" + str(i) for i in range(1999, 2019)]

grid = grid[new_names]

# grid.dropna(axis=0, subset=['cell_id'], inplace=True)

grid.to_csv(path+'/pre_panel.csv', index=False)

# identify column indices for each time-variant measure. Will need these indices for reshaping
headers = [str(i) for i in range(1999, 2019)]
trt_rural_transport_index = ["Rural Transport" in i for i in grid.columns]
trt_irrigation_index = ["Irrigation" in i for i in grid.columns]
trt_rural_water_index = ["Rural Domestic Water Supplies" in i for i in grid.columns]
trt_urban_transport_index = ["Urban transport" in i for i in grid.columns]
trt_education_index = ["Education" in i for i in grid.columns]
trt_other_index = ["other" in i for i in grid.columns]
ndvi_index = ["ndvi" in i for i in grid.columns]
temperature_index = ['temperature' in i for i in grid.columns]
precip_index = ['precip' in i for i in grid.columns]

#for name in dir():
#	if not name.startswith('_') and name!="path" and name!="itertools":
#		del globals()[name]

# reshape panel from wide to long form
with open(path+"/pre_panel.csv") as f, open(path+"/panel.csv", "w") as f2:
	# first line of the csv is variable names
    a=f2.write("latitude,longitude,cell_id,year,province_id,province_name,district_id,district_name,commune_id,commune_name,ndvi,trt_ruraltrans,trt_irrigation,trt_ruralwater,trt_urbantrans,trt_education,trt_other,temperature,precip\n")
    # performing transformation one grid cell at a time
    for i, line in enumerate(f):
        if i != 0:
            x = line.strip().split(',')
            latitude, longitude, cell, province_id, province_name, district_id, district_name, commune_id, commune_name = x[0:9]
            ndvi = list(itertools.compress(x, ndvi_index))
            trt_rural_trans = list(itertools.compress(x, trt_rural_transport_index))
            trt_irrigation = list(itertools.compress(x, trt_irrigation_index))
            trt_rural_water = list(itertools.compress(x, trt_rural_water_index))
            trt_urban_trans = list(itertools.compress(x, trt_urban_transport_index))
            trt_education = list(itertools.compress(x, trt_education_index))
            trt_other = list(itertools.compress(x, trt_other_index))
            temperature = list(itertools.compress(x, temperature_index))
            precip = list(itertools.compress(x, precip_index))
            for year, ndvi_out, trt_rt_out, trt_ir_out, trt_rw_out, trt_ut_out, trt_ed_out, trt_ot_out, temp_out, precip_out in zip(headers, ndvi, trt_rural_trans, trt_irrigation, trt_rural_water, trt_urban_trans, trt_education, trt_other, temperature, precip):
                a=f2.write(','.join([latitude, longitude, cell, year,province_id, province_name, district_id, district_name, commune_id, commune_name, ndvi_out, trt_rt_out, trt_ir_out, trt_rw_out, trt_ut_out, trt_ed_out, trt_ot_out, temp_out, precip_out])+'\n')

















