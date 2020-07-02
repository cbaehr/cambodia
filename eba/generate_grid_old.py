
path = "/sciclone/home20/cbaehr/cambodia/eba/inputData"
# path = "C:/Users/cbaehr/Desktop/test"

import geopandas as gpd
import fiona
import itertools
import numpy as np
import pandas as pd
import rasterio
from rasterstats import zonal_stats
from shapely.geometry import shape, Point
from shapely.prepared import prep

# build empty grid

stepsize = 0.00026949999

grid_extent = fiona.open(path+"/grid_extent.geojson")
grid_feature = grid_extent[0]

# extract geometry from boundary shapefile
grid_shape = shape(grid_feature['geometry'])
prep_feat = prep(grid_shape)

grid_bounds = grid_shape.bounds

lonmin = grid_bounds[0] + (stepsize/2)
lonmax = grid_bounds[2] - (stepsize/2)
latmin = grid_bounds[1] + (stepsize/2)
latmax = grid_bounds[3] - (stepsize/2)

coords = itertools.product(
    np.arange(lonmin, lonmax, stepsize),
    np.arange(latmin, latmax, stepsize))

point_list = map(Point, coords)

point_list_trimmed = filter(prep_feat.contains, point_list)
df_list = [{'longitude': i.x, 'latitude': i.y} for i in point_list_trimmed]

grid = pd.DataFrame(df_list)
grid_geometry = [Point(xy) for xy in zip(grid.longitude, grid.latitude)]
empty_grid_geo = gpd.GeoDataFrame(grid, crs='epsg:4326', geometry=grid_geometry)

treecover = rasterio.open(path+"/Hansen_treecover2000_cambodia.tif")
array = treecover.read(1)
affine = treecover.transform
tc_grid = zonal_stats(empty_grid_geo, array, affine=affine, stats=["mean"])
tc_grid = pd.DataFrame(tc_grid)

print(len(tc_grid[tc_grid["mean"]>50]))

grid = grid[tc_grid["mean"]>50]
grid['cell_id'] = grid.index.values+1

grid = grid[["longitude", "latitude", "cell_id"]]

print(len(grid))

grid.to_csv(path+'/empty_grid.csv', index=False)









