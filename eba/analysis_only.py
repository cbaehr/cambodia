

my_dir = '/sciclone/home20/cbaehr/cambodia/eba/inputData'

import fiona
import itertools
import math
import numpy as np
from osgeo import gdal, gdalconst
import pandas as pd
import rasterio
from shapely.geometry import shape, Point
from shapely.prepared import prep

grid = pd.read_csv(my_dir+'/full_grid.csv')

for i in range(1999, 2019):
	col = 'ndvi' + str(i)
	grid.loc[grid[col]<0, col] = np.nan

grid.describe().to_csv(my_dir+'/summary_stats.csv')

correlation_cols = ['hansen'] + ['ndvi'+str(i) for i in range(1999, 2019)]
grid[correlation_cols].corr().to_csv(my_dir+'/correlation_matrix.csv')

###

grid = grid[grid['hansen'] > 0.5]

grid.describe().to_csv(my_dir+'/summary_stats_forestsonly.csv')

grid[correlation_cols].corr().to_csv(my_dir+'/correlation_matrix_forestsonly.csv')


