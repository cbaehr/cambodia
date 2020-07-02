
path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"

#import os

from distancerasters import build_distance_array, rasterize, export_raster

# -----------------------------------------------------------------------------

from affine import Affine
# import numpy as np
import fiona
from shapely.geometry import shape


pixel_size = 0.00026949999

# canal_path = os.path.expanduser("~/git/afghanistan_gie/canal_data/canal_lines.geojson")
canal_path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData/cambodia_cities500.geojson"


#with fiona.open(canal_path) as canal_src:
#    bounds = canal_src.bounds

grid_extent = fiona.open(path+"/grid_extent.geojson")
grid_feature = grid_extent[0]
grid_shape = shape(grid_feature['geometry'])
bounds = grid_shape.bounds


rv_array, affine = rasterize(canal_path, pixel_size=pixel_size, bounds=bounds)


# binary_raster_path = "/sciclone/aiddata10/REU/projects/afghanistan_gie/distance_to_canals/binary_canals.tif"
# binary_raster_path = "/sciclone/aiddata10/REU/projects/afghanistan_gie/distance_to_canals/binary_starts.tif"
binary_raster_path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData/binary_starts.tif"

export_raster(rv_array, affine, binary_raster_path)

# import tarfile

# def make_tarfile(dst, src):
#     with tarfile.open(dst, "w:gz") as tar:
#         tar.add(src, arcname=os.path.basename(src))


# make_tarfile(dst=binary_raster_path + ".tar.gz" , src=binary_raster_path)

# -----------------------------------------------------------------------------


# distance_raster_path = "/sciclone/aiddata10/REU/projects/afghanistan_gie/distance_to_canals/distance_canals.tif"
# distance_raster_path = "/sciclone/aiddata10/REU/projects/afghanistan_gie/distance_to_canals/distance_starts.tif"
distance_raster_path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData/distance_starts.tif"

def raster_conditional(rarray):
    return (rarray == 1)

dist = build_distance_array(rv_array, affine=affine,
                            output=distance_raster_path,
                            conditional=raster_conditional)


# make_tarfile(dst=distance_raster_path + ".tar.gz" , src=distance_raster_path)
















