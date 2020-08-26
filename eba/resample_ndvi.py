
#path = "/Users/christianbaehr/Downloads"
path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"

from osgeo import gdal, gdalconst

match_filename = path+"/Hansen_treecover2000_trimmed.tif"
match_ds = gdal.Open(match_filename, gdalconst.GA_ReadOnly)
match_proj = match_ds.GetProjection()
match_geotrans = match_ds.GetGeoTransform()
wide = match_ds.RasterXSize
high = match_ds.RasterYSize

for i in range(1999, 2019):
	src_filename = path+"/ndvi/ndvi_landsat_"+str(i)+".tif"
	src = gdal.Open(src_filename, gdalconst.GA_ReadOnly)
	src_proj = src.GetProjection()
	src_geotrans = src.GetGeoTransform()
	dst_filename = path+"/ndvi_adjusted/ndvi_landsat_"+str(i)+"_adjusted.tif"
	dst = gdal.GetDriverByName('GTiff').Create(dst_filename, wide, high, 1, gdalconst.GDT_Float32)
	dst.SetGeoTransform( match_geotrans )
	dst.SetProjection( match_proj)
	gdal.ReprojectImage(src, dst, src_proj, match_proj, gdalconst.GRA_Bilinear)
	del dst # Flush


