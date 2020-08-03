
# path = "/sciclone/home20/cbaehr/cambodia/eba/inputData"
path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"

import geopandas as gpd
from osgeo import gdal, gdalconst
import os
import pandas as pd
import rasterio
from rasterstats import zonal_stats
import itertools

### ALIGNMENT ###

# realigning the Hansen treecover raster to the 2018 NDVI data
#if not os.path.exists(path+"/treecover2000_cambodia_adjusted.tif"):
match_filename = path+"/ndvi/ndvi_2003_landsat.tif"
match_ds = gdal.Open(match_filename, gdalconst.GA_ReadOnly)
match_proj = match_ds.GetProjection()
match_geotrans = match_ds.GetGeoTransform()
wide = match_ds.RasterXSize
high = match_ds.RasterYSize
# file to be re-aligned. Hansen 2000 treecover raster
src_filename = path+"/Hansen_treecover2000_cambodia.tif"
src = gdal.Open(src_filename, gdalconst.GA_ReadOnly)
src_proj = src.GetProjection()
src_geotrans = src.GetGeoTransform()
# filename for re-aligned Hansen raster
dst_filename = path+"/treecover2000_cambodia_adjusted.tif"
# pre-processing. Set up GeoTiff and get projection3
dst = gdal.GetDriverByName("GTiff").Create(dst_filename, wide, high, 1, gdalconst.GDT_Float32)
dst.SetGeoTransform(match_geotrans)
dst.SetProjection(match_proj)
# perform re-alignment and save to specified output dst
gdal.ReprojectImage(src, dst, src_proj, match_proj, gdalconst.GRA_Bilinear)

##########

### BINARY CONVERSION ###

# can run locally

# convert ALIGNED hansen 2000 tree cover raster to binary (>25% treecover)

# check that binary raster doesnt already exist
#if not os.path.exists(path+"/treecover2000_cambodia_binary.tif"):
# open hansen treecover with actual values
base = gdal.Open(path+"/Hansen_treecover2000_cambodia.tif")
# set path to export binary raster to
new_path = path+"/treecover2000_cambodia_binary.tif"
# retrieve driver info
d = gdal.GetDriverByName("GTiff")
# create a copy of hansen raster to store new values in
new = d.CreateCopy(new_path, base, strict=0)
# convert tree cover values to array
base_vals = base.GetRasterBand(1).ReadAsArray()
# convert values to either 1 or 0 based on this condition
new_vals = base_vals > 0.25
# write binary raster to new Tiff
new.GetRasterBand(1).WriteArray(new_vals)
del base, new

### AGGREGATE HANSEN TO 1KM GRID ###

# can run locally

# aggregate Hansen 2000 tree cover binary values to the 1km grid cell level. This gives
# us a baseline "percent tree cover" measure

gain = rasterio.open(path+"/Hansen_gain_cambodia.tif")
gain_array = gain.read(1)

gain_array==1

#if not os.path.exists(path+"/cambodia_1kmgrid.geojson"):
treecover = rasterio.open(path+"/treecover2000_cambodia_binary.tif")
array = treecover.read(1)
array[gain_array==1] = -9999
affine = treecover.transform
grid = gpd.read_file(path+"/cambodia_template_1kmgrid.geojson")
stats = zonal_stats(grid, array, affine=affine, stats=['mean'])
grid['pcttreecover2000'] = pd.DataFrame(stats)
#grid.to_file(path+"/cambodia_1kmgrid.geojson", driver="GeoJSON")
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
	array[gain_array==1] = -9999
	affine = loss_raster.transform
	stats = zonal_stats(grid, array, affine=affine, stats=['mean'])
	grid['pcttreecover'+str(i+2000)] = grid['pcttreecover'+str(i+1999)] - pd.DataFrame(stats)['mean']

#grid.to_file(path+"/cambodia_1kmgrid.geojson", driver="GeoJSON")

###

#grid = gpd.read_file(path+"/cambodia_1kmgrid.geojson")

# add NDVI to 1km grid

for i in range(1999, 2019):
	ndvi = rasterio.open(path+"/ndvi/ndvi_"+str(i)+"_landsat.tif")
	array = ndvi.read(1)
	array[array<0] = -9999
	affine = ndvi.transform
	stats = zonal_stats(grid, array, affine=affine, stats=['mean'], nodata=-9999)
	grid['ndvi'+str(i)] = pd.DataFrame(stats) * 0.0001

grid.to_file(path+"/cambodia_1kmgrid.geojson", driver="GeoJSON")


###

grid = gpd.read_file(path+"/cambodia_1kmgrid.geojson")

#grid_slim = grid[grid.columns.drop(['left', 'top', 'right', 'bottom', 'geometry'])]

grid.reset_index(inplace=True)

names = ['id', "geometry"] + ["pcttreecover" + str(i) for i in range(2000, 2018)] + ["ndvi" + str(i) for i in range(2000, 2018)]
pre_panel = grid[names]

pre_panel = pre_panel.dropna(axis=0, subset=['id'])

#new_names = ["cell_id"] + ["pcttreecover"+str(i) for i in range(2000, 2018)] + ["ndvi"+str(i) for i in range(2000, 2018)]

pre_panel.rename(columns={"id":"cell_id"}, inplace=True)

##########

adm = gpd.read_file(path+"/gadm36_KHM_3.geojson")

test = gpd.sjoin(pre_panel, adm[['GID_1', 'NAME_1', 'NL_NAME_1', 'GID_2', 'NAME_2', 'GID_3', 'NAME_3', "geometry"]], how="left", op="intersects")



path = "/sciclone/home20/cbaehr/cambodia/eba/inputData"

grid = pd.read_csv(path+"/full_grid.csv")


geometry = [Point(xy) for xy in zip(grid.longitude, grid.latitude)]
crs = {'init': 'epsg:4326'}
gdf = gpd.GeoDataFrame(grid['cell_id'], crs=crs, geometry=geometry)

hansen = gpd.read_file(path+"/hansen_grid_1km.geojson")


cols = ["pcttreecover" + str(i) for i in range(2000, 2018)] + ["geometry"]

hansen_grid = gpd.sjoin(gdf, hansen[cols], how='left', op='intersects')

new_cols = ["pcttreecover" + str(i) for i in range(2000, 2018)]

full_grid = pd.concat([grid.reset_index(drop=True), hansen_grid[new_cols].reset_index(drop=True)], axis=1)

full_grid.to_csv(path+"/full_grid2.csv", index=False)






for i in range(1999, 2019):
	ndvi = rasterio.open(path+"/ndvi/ndvi_"+str(i)+"_landsat.tif")
	array = ndvi.read(1)
	array[array<0] = -9999
	affine = ndvi.transform
	stats = zonal_stats(grid, array, affine=affine, stats=['mean'], nodata=-9999)
	grid['ndvi'+str(i)] = pd.DataFrame(stats) * 0.0001






##########

pre_panel.to_file(path+"/pre_panel_hansen.geojson", driver="GeoJSON")




##########

#grid_slim["cell_id"] = grid_slim.index

test=pd.wide_to_long(pre_panel, stubnames=["pcttreecover", "ndvi"], i="cell_id", j="year")

test.reset_index(inplace=True)


test = test[["id", "year", "pcttreecover", "ndvi", "geometry"]]

test.to_file(path+"/panel_hansen.geojson", driver="GeoJSON")







panel = pd.read_csv(path+"/panel_hansen.csv")

#panel.describe()
panel.describe().apply(lambda s: s.apply(lambda x: format(x, 'g')))
panel[["pcttreecover", "ndvi"]].corr()





































