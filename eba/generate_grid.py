
path = "/sciclone/home20/cbaehr/cambodia/eba/inputData"
# path = "C:/Users/cbaehr/Desktop/test"

import fiona
import itertools
import numpy as np
import pandas as pd
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

grid['cell_id'] = grid.index.values+1
grid.to_csv(path+'/empty_grid.csv', index=False)