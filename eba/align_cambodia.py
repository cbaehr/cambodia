
import fiona
from shapely.geometry import shape, Point
from shapely.prepared import prep
import math
import itertools
import numpy as np
import pandas as pd
from osgeo import gdal, gdalconst

###

src_filename = '/sciclone/home20/cbaehr/cambodia/eba/inputData/Hansen_treecover2000_cambodia.tif'
src = gdal.Open(src_filename, gdalconst.GA_ReadOnly)
src_proj = src.GetProjection()
src_geotrans = src.GetGeoTransform()

#match_filename = '/sciclone/aiddata10/REU/projects/cambodia_eba_gie/ndvi/landsat/mosaic/all/2018_all.tif'
match_filename = '/sciclone/home20/cbaehr/cambodia/eba/inputData/ndvi/2018_all.tif'
match_ds = gdal.Open(match_filename, gdalconst.GA_ReadOnly)
match_proj = match_ds.GetProjection()
match_geotrans = match_ds.GetGeoTransform()
wide = match_ds.RasterXSize
high = match_ds.RasterYSize

#dst_filename = '/Users/christianbaehr/Downloads/cambodia_new/aligned_raster.tif'
dst_filename = '/sciclone/home20/cbaehr/cambodia/eba/inputData/Hansen_treecover2000_cambodia_adjusted.tif'

dst = gdal.GetDriverByName('GTiff').Create(dst_filename, wide, high, 1, gdalconst.GDT_Float32)
dst.SetGeoTransform( match_geotrans )
dst.SetProjection( match_proj)

# Do the work
gdal.ReprojectImage(src, dst, src_proj, match_proj, gdalconst.GRA_Bilinear)

del dst # Flush

















































