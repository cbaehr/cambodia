
path = "/sciclone/home20/cbaehr/cambodia/eba/inputData"
# path = "C:/Users/cbaehr/Desktop/test"
# path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"

import geopandas as gpd
import fiona
import itertools
import numpy as np
from osgeo import gdal
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

grid['cell_id'] = grid.index.values+1

###############################################################

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

###############################################################

#grid = getValuesAtPoint(indir=working_dir, rasterfileList=['hansen_treecover'], pos=grid, lon='longitude', lat='latitude', cell_id='Unnamed: 0')
grid = getValuesAtPoint(indir=path, rasterfileList=['Hansen_treecover2000_cambodia'], pos=grid, lon='longitude', lat='latitude', cell_id='cell_id')

grid = grid[grid["Hansen_treecover2000_cambodia"]>50]

grid['cell_id'] = grid.index.values+1

grid = grid[["x", "y", "cell_id"]]
grid.columns = ["longitude", "latitude", "cell_id"]

grid.to_csv(path+'/empty_grid.csv', index=False)







