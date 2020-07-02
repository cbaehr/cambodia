
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


def getValuesAtPoint(indir, rasterfileList, pos, lon, lat, cell_id):
    #gt(2) and gt(4) coefficients are zero, and the gt(1) is pixel width, and gt(5) is pixel height.
    #The (gt(0),gt(3)) position is the top left corner of the top left pixel of the raster.
    for i, rs in enumerate(rasterfileList):
        presValues = []
        gdata = gdal.Open('{}/{}.tif'.format(indir,rs))
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
            df = pd.DataFrame(presValues, columns=['cell_id', 'x', 'y', rs])
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
            df[rs] = pd.Series(presValues)
    del data, band
    return df

###



grid = pd.read_csv(my_dir+'/empty_grid.csv')

raster_list = ['Hansen_treecover2000_cambodia_adjusted'] + ['ndvi/'+str(i)+'_all' for i in range(1999, 2019)]

grid = getValuesAtPoint(indir=my_dir, rasterfileList=raster_list, pos=grid, lon='longitude', lat='latitude', cell_id='Unnamed: 0')

grid.columns = ['cell_id', 'latitude', 'longitude', 'hansen'] + ['ndvi'+str(i) for i in range(1999, 2019)]
grid.to_csv(my_dir+'/full_grid.csv', index=False)

grid.describe().to_csv(my_dir+'/summary_stats.csv')

correlation_cols = ['hansen'] + ['ndvi'+str(i) for i in range(1999, 2019)]
grid[correlation_cols].corr().to_csv(my_dir+'/correlation_matrix.csv')

###

grid = grid[grid['hansen'] > 0.5]

grid.describe().to_csv(my_dir+'/summary_stats_forestsonly.csv')

grid[correlation_cols].corr().to_csv(my_dir+'/correlation_matrix_forestsonly.csv')


