
path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"

import pandas as pd
from shapely.geometry import shape, Point, MultiPoint, MultiPolygon
import numpy as np
from osgeo import gdal, ogr
import geopandas as gpd
import re
import itertools


###

#grid = pd.read_csv("/Users/christianbaehr/Downloads/empty_grid_test.csv").reset_index(drop=True)

grid = pd.read_csv(path+"/empty_grid.csv").reset_index(drop=True)
#empty_grid = pd.read_csv("/Users/christianbaehr/Downloads/empty_grid_test.csv").reset_index(drop=True)

#hansen_grid = pd.read_csv(path+"/hansen_grid.csv").reset_index(drop=True)
#hansen_grid = pd.read_csv("/Users/christianbaehr/Downloads/hansen_grid_test.csv").reset_index(drop=True)

#ndvi_grid = pd.read_csv(path+"/ndvi_grid.csv").reset_index(drop=True)
#ndvi_grid = pd.read_csv("/Users/christianbaehr/Downloads/ndvi_grid_test.csv").reset_index(drop=True)

#grid = pd.concat([empty_grid, hansen_grid.drop(["cell_id"], axis=1), ndvi_grid.drop(["cell_id"], axis=1)], axis=1)

#del empty_grid, hansen_grid, ndvi_grid

###

grid_geometry = [Point(xy) for xy in zip(grid.lon, grid.lat)]
grid_geo = gpd.GeoDataFrame(grid['cell_id'], crs='epsg:4326', geometry=grid_geometry)

del grid_geometry

###

def build(year_str):
    j = year_str.split('|')
    return {i:j.count(i) for i in set(j)}

multiring_treatment = gpd.read_file(path+"/pid/pid2003-18_trimmed_multiring.geojson")
multiring_treatment = multiring_treatment[["end_year", "mrb_dist", "geometry"]]
multiring_treatment["mrb_dist"] = multiring_treatment["mrb_dist"].astype(int)


for i in [1000, 2000, 3000, 4000, 5000]:
	temp = multiring_treatment.loc[multiring_treatment["mrb_dist"]==i]
	treatment_temp = gpd.sjoin(grid_geo, temp[['end_year', 'geometry']], how='left', op='intersects')
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
		treatment_grid = pd.concat([grid[["cell_id"]].reset_index(drop=True), treatment_grid_temp.reset_index(drop=True)], axis=1)
	else:
		treatment_grid = pd.concat([treatment_grid.reset_index(drop=True), treatment_grid_temp.reset_index(drop=True)], axis=1)

#treatment_grid = pd.concat([grid.reset_index(drop=True), treatment_grid.reset_index(drop=True).drop(["cell_id"], axis=1)], axis=1)

treatment_grid.to_csv(path+"/treatment_grid.csv", index=False)

#del treatment_grid

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

rasters = ["temp_"+str(i)+".tif" for i in range(2001, 2018)]

temperature_grid = getValuesAtPoint(indir=path+"/temperature", rasterfileList=rasters, pos=grid, lon="lon", lat="lat", cell_id="cell_id")

#temperature_grid = pd.concat([grid, temp.reset_index(drop=True).drop(["cell_id", "x", "y"], axis=1)], axis=1)

temperature_grid.drop(["x", "y"], axis=1).to_csv(path+"/temperature_grid.csv", index=False)

#del temperature_grid

###


rasters = ["precip_"+str(i)+".tif" for i in range(2000, 2017)]

precip_grid = getValuesAtPoint(indir=path+"/precip", rasterfileList=rasters, pos=grid, lon="lon", lat="lat", cell_id="cell_id")

#grid = pd.concat([grid, temp.reset_index(drop=True).drop(["cell_id", "x", "y"], axis=1)], axis=1)

precip_grid.drop(["x", "y"], axis=1).to_csv(path+"/precip_grid.csv", index=False)

#precip_grid.to_csv(path+"/precip_grid.csv", index=False)

#del precip_grid

###

adm = gpd.read_file(path+"/gadm36_KHM_3.geojson")
adm_grid = gpd.sjoin(grid_geo, adm[["GID_1", "NAME_1", "GID_2", "NAME_2", "GID_3", "NAME_3", "geometry"]], how='left', op='intersects')
#grid = pd.concat([grid, adm_grid[["GID_1", "NAME_1", "GID_2", "NAME_2", "GID_3", "NAME_3"]].reset_index(drop=True).drop(["geometry"], axis=1)], axis=1)
#grid = pd.concat([grid, adm_grid.reset_index(drop=True).drop(["cell_id", "index_right", "geometry"], axis=1)], axis=1)
adm_grid.drop(["geometry", "index_right"], axis=1, inplace=True)

adm_grid.to_csv(path+"/adm_grid.csv", index=False)

#adm_grid.to_csv(path+"/adm_grid.csv", index=False)

#del adm_grid

#grid.to_csv(path+"/full_grid.csv", index=False)
#grid.to_csv("/Users/christianbaehr/Downloads/full_grid.csv", index=False)


#for i in grid.columns:
#	print(i)

##################################################################

#grid = pd.concat([grid, adm_grid.drop(["cell_id", "geometry", "index_right"], axis=1)], axis=1)
#del adm_grid

#hansen_grid = pd.read_csv("/Users/christianbaehr/Downloads/hansen_grid_test.csv")
hansen_grid = pd.read_csv(path+"/hansen_grid.csv")
#grid = pd.concat([grid, hansen_grid.drop(["cell_id"], axis=1)], axis=1)
#del hansen_grid

#ndvi_grid = pd.read_csv("/Users/christianbaehr/Downloads/ndvi_grid_test.csv")
ndvi_grid = pd.read_csv(path+"/ndvi_grid.csv")
#grid = pd.concat([grid, ndvi_grid.drop(["cell_id"], axis=1)], axis=1)
#del ndvi_grid

#treatment_grid = pd.read_csv(path+"/treatment_grid.csv")
#grid = pd.concat([grid, treatment_grid.drop(["cell_id"], axis=1)], axis=1)
#del treatment_grid

#temperature_grid = pd.read_csv(path+"/temperature_grid.csv")
#grid = pd.concat([grid, temperature_grid.drop(["cell_id"], axis=1)], axis=1)
#del temperature_grid

#precip_grid = pd.read_csv(path+"/precip_grid.csv")
#grid = pd.concat([grid, precip_grid.drop(["cell_id"], axis=1)], axis=1)
#del precip_grid

gov_grid = pd.read_csv(path+"/governance_grid.csv").reset_index(drop=True)

#treatment_grid.to_csv(path+"/treatment_grid.csv", index=False)
#temperature_grid.drop(["x", "y"], axis=1).to_csv(path+"/temperature_grid.csv", index=False)

#precip_grid.drop(["x", "y"], axis=1).to_csv(path+"/precip_grid.csv", index=False)

#adm_grid.drop(["geometry", "index_right"], axis=1).to_csv(path+"/adm_grid.csv", index=False)

grid = grid.reset_index(drop=True)
adm_grid = adm_grid.reset_index(drop=True).drop(["cell_id"], axis=1)
hansen_grid = hansen_grid.reset_index(drop=True).drop(["cell_id"],axis=1)
ndvi_grid = ndvi_grid.reset_index(drop=True).drop(["cell_id"],axis=1)
treatment_grid = treatment_grid.reset_index(drop=True).drop(["cell_id"], axis=1)
temperature_grid = temperature_grid.reset_index(drop=True).drop(["cell_id", "x", "y"], axis=1)
precip_grid = precip_grid.reset_index(drop=True).drop(["cell_id", "x", "y"], axis=1)
gov_grid = gov_grid.drop(["cell_id"], axis=1)

full_grid = pd.concat([grid, adm_grid, hansen_grid, ndvi_grid, treatment_grid, temperature_grid, precip_grid, gov_grid], axis=1)


full_grid.to_csv(path+"/full_grid.csv", index=False)
grid=full_grid

del grid, ndvi_grid, hansen_grid, adm_grid, temperature_grid, precip_grid

##################################################################

for i in grid.columns:
	print(i)

names_order = ["cell_id", "lon", "lat", "GID_1", "NAME_1", "GID_2", "NAME_2", "GID_3", "NAME_3", "plantation", "concession", "protected_area"]

for i in ["tc", "ndvi", "treatment1000_", "treatment2000_", "treatment3000_", "treatment4000_", "treatment5000_", "temp_", "precip_"]:
	for j in range(1999, 2019):
		names_order = names_order + [i+str(j)]
		if i+str(j) not in grid.columns:
			grid[i+str(j)] = "NA"
grid = grid[names_order]

new_names = ["cell_id", "longitude", "latitude", "province_number", "province_name", "district_number", "district_name", "commune_number", "commune_name", "plantation", "concession", "protected_area"]
for i in ["treecover", "ndvi", "trt1km", "trt2km", "trt3km", "trt4km", "trt5km", "temperature", "precip"]:
	for j in range(1999, 2019):
		new_names = new_names + [i+str(j)]
names_dict = {}
for i in range(0, len(names_order)):
	names_dict[names_order[i]] = new_names[i]
grid.rename(columns=names_dict, inplace=True)

grid.dropna(axis=0, subset=["cell_id"], inplace=True)

grid.to_csv(path+"/pre_panel.csv", index=False, encoding="utf-8")

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


with open(path+"/pre_panel.csv") as f, open(path+"/panel.csv", "w") as f2:
	a=f2.write("cell_id,year,longitude,latitude,province_number,province_name,district_number,district_name,commune_number,commune_name,plantation,concession,protected_area,treecover,ndvi,trt1km,trt2km,trt3km,trt4km,trt5km,temperature,precip\n")
	for i, line in enumerate(f):
		if i>0:
			x = line.strip().split(",")
			cell, longitude, latitude, province_number, province_name, district_number, district_name, commune_number, commune_name, plantation, concession, pa = x[0:12]
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
				a=f2.write(",".join([cell, year, longitude, latitude, province_number, province_name, district_number, district_name, commune_number, commune_name, plantation, concession, pa, tc_out, ndvi_out, trt1km_out, trt2km_out, trt3km_out, trt4km_out, trt5km_out, temperature_out, precip_out])+'\n')





















