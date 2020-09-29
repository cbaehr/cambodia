
#path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"
path = "/sciclone/home20/cbaehr/cambodia/eba/inputData"

import pandas as pd
import geopandas as gpd
from shapely.geometry import shape, Point, MultiPoint, MultiPolygon
import numpy as np
from osgeo import gdal, ogr
import re
import itertools

empty_grid = pd.read_csv(path+"/empty_grid.csv").reset_index(drop=True)

def getValuesAtPoint(indir, rasterfileList, pos, lon, lat, cell_id):
    #gt(2) and gt(4) coefficients are zero, and the gt(1) is pixel width, and gt(5) is pixel height.
    #The (gt(0),gt(3)) position is the top left corner of the top left pixel of the raster.
    for i, rs in enumerate(rasterfileList):
        presValues = []
        gdata = gdal.Open('{}/{}'.format(indir,rs))
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
            df = pd.DataFrame(presValues, columns=['cell_id', 'x', 'y', re.sub(".tif", "", rs)])
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
            df[re.sub(".tif", "", rs)] = pd.Series(presValues)
    del data, band
    return df

rasters = ["distance_to_city.tif", "distance_to_road.tif", "gpw_density_2000.tif", "gpw_density_2005.tif", "gpw_density_2010.tif", "gpw_density_2015.tif", "gpw_density_2020.tif"]

misc_grid = getValuesAtPoint(indir=path, rasterfileList=rasters, pos=empty_grid, lon="lon", lat="lat", cell_id="cell_id")

misc_grid.drop(["x", "y"], axis=1, inplace=True)

misc_grid.to_csv(path+"/misc_grid.csv", index=False)













