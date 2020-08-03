
path = "/sciclone/home20/cbaehr/cambodia/eba/inputData"
#path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"

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
match_filename = path+"/ndvi/ndvi_landsat_2003.tif"
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
del dst


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
new_vals = base_vals >= 0.25
# write binary raster to new Tiff
new.GetRasterBand(1).WriteArray(new_vals)
del base, new

#########

for i in range(2001, 2018):
	#match_filename = path+"/ndvi/ndvi_landsat_2003.tif"
	#match_ds = gdal.Open(match_filename, gdalconst.GA_ReadOnly)
	#match_proj = match_ds.GetProjection()
	#match_geotrans = match_ds.GetGeoTransform()
	#wide = match_ds.RasterXSize
	#high = match_ds.RasterYSize
	src_filename = path+"/temperature/temp_"+str(i)+".tif"
	src = gdal.Open(src_filename, gdalconst.GA_ReadOnly)
	src_proj = src.GetProjection()
	src_geotrans = src.GetGeoTransform()
	dst_filename = path+"/temperature30m/temperature30m_"+str(i)+".tif"
	dst = gdal.GetDriverByName("GTiff").Create(dst_filename, wide, high, 1, gdalconst.GDT_Float32)
	dst.SetGeoTransform(match_geotrans)
	dst.SetProjection(match_proj)
	gdal.ReprojectImage(src, dst, src_proj, match_proj, gdalconst.GRA_Bilinear)
	del dst

###

for i in range(1999, 2019):
	#match_filename = path+"/ndvi/ndvi_landsat_2003.tif"
	#match_ds = gdal.Open(match_filename, gdalconst.GA_ReadOnly)
	#match_proj = match_ds.GetProjection()
	#match_geotrans = match_ds.GetGeoTransform()
	#wide = match_ds.RasterXSize
	#high = match_ds.RasterYSize
	src_filename = path+"/precip/precip_"+str(i)+".tif"
	src = gdal.Open(src_filename, gdalconst.GA_ReadOnly)
	src_proj = src.GetProjection()
	src_geotrans = src.GetGeoTransform()
	dst_filename = path+"/precip30m/precip30m_"+str(i)+".tif"
	dst = gdal.GetDriverByName("GTiff").Create(dst_filename, wide, high, 1, gdalconst.GDT_Float32)
	dst.SetGeoTransform(match_geotrans)
	dst.SetProjection(match_proj)
	gdal.ReprojectImage(src, dst, src_proj, match_proj, gdalconst.GRA_Bilinear)
	del dst

#########






























