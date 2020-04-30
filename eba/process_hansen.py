
# path = "/sciclone/home20/cbaehr/cambodia/eba/inputData"
path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"

import geopandas as gpd
from osgeo import gdal, gdalconst
import os
import pandas as pd
import rasterio
from rasterstats import zonal_stats
import itertools

###

### ALIGNMENT ###

# realigning the Hansen treecover raster to the 2018 NDVI data
if not os.path.exists(path+"/treecover2000_cambodia_adjusted.tif"):
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
if not os.path.exists(path+"/treecover2000_cambodia_binary.tif"):
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

if not os.path.exists(path+"/cambodia_1kmgrid.geojson"):
	treecover = rasterio.open(path+"/treecover2000_cambodia_binary.tif")
	array = treecover.read(1)
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
		affine = loss_raster.transform
		stats = zonal_stats(grid, array, affine=affine, stats=['mean'])
		grid['pcttreecover'+str(i+2000)] = grid['pcttreecover'+str(i+1999)] - pd.DataFrame(stats)['mean']
	grid.to_file(path+"/cambodia_1kmgrid.geojson", driver="GeoJSON")


###

grid = gpd.read_file(path+"/cambodia_1kmgrid.geojson")

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

grid_slim = grid.dropna(axis=0, subset=['cell_id'])
grid_slim = grid[grid.columns.drop(['left', 'top', 'right', 'bottom', 'geometry'])]

names = ['id'] + ["pcttreecover" + str(i) for i in range(2000, 2018)] + ["ndvi" + str(i) for i in range(2000, 2018)]
grid_slim = grid_slim[names]

grid_slim.to_csv(path+"/cambodia_1kmgrid.csv", index=False)

headers = [str(i) for i in range(2000, 2018)]
tc_index = ['pcttreecover' in i for i in grid_slim.columns]
ndvi_index = ['ndvi' in i for i in grid_slim.columns]

# reshape panel from wide to long form
with open(path+"/cambodia_1kmgrid.csv") as f, open(path+'/panel.csv', 'w') as f2:
	# first line of the csv is variable names
    a=f2.write('id,year,pcttreecover,ndvi\n')
    # performing transformation one grid cell at a time
    for i, line in enumerate(f):
        if i != 0:
            x = line.strip().split(',')
            #cell, commune, province, plantation, concession, protected, distance = x[0:7]
            cell = x[0]
            pcttreecover = list(itertools.compress(x, tc_index))
            ndvi = list(itertools.compress(x, ndvi_index))
            for year, tc_out, ndvi_out in zip(headers, pcttreecover, ndvi):
            	a=f2.write(','.join([cell, year, tc_out, ndvi_out])+'\n')

panel = pd.read_csv(path+"/panel.csv")

#panel.describe()
panel.describe().apply(lambda s: s.apply(lambda x: format(x, 'g')))
panel[["pcttreecover", "ndvi"]].corr()





































