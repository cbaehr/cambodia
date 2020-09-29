
### SWITCH ###
#path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"
path = "/sciclone/home20/cbaehr/cambodia/eba/inputData"

import pandas as pd
import geopandas as gpd
from shapely.geometry import shape, Point, MultiPoint, MultiPolygon
import numpy as np
from osgeo import gdal, ogr
import re
import itertools

### SWITCH ###
#empty_grid = pd.read_csv(path+"/empty_grid_test.csv").reset_index(drop=True)
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

rasters = ["distance_to_minecasualty.tif"]

mine_grid = getValuesAtPoint(indir=path, rasterfileList=rasters, pos=empty_grid, lon="lon", lat="lat", cell_id="cell_id")

mine_grid.drop(["x", "y"], axis=1, inplace=True)

mine_grid.to_csv(path+"/mine_grid.csv", index=False)

###########################################################################

grid = pd.read_csv(path+"/merging_grid_1km.csv")

full_grid = pd.concat([grid, mine_grid], axis=1)

full_grid.drop(["cell_id_y", "cell_id"], axis=1, inplace=True)

full_grid = full_grid.loc[~full_grid["cell_id_x"].isnull(), ]

del grid

grid_1km = full_grid.groupby("cell_id_x").agg(["mean"])

grid_1km.columns = grid_1km.columns.get_level_values(0)
grid_1km["cell_id"] = grid_1km.index
grid_1km = grid_1km.reset_index(drop=True)

grid_1km.to_csv(path+"/grid_1km_minecasualty.csv", index=False, encoding="utf-8")

###########################################################################

mine_grid.shape
mine_grid.drop(["cell_id"], axis=1, inplace=True)

### SWITCH ###
#full_grid = pd.read_csv(path+"/full_grid_new_test.csv")
full_grid = pd.read_csv(path+"/full_grid_new.csv")

full_grid = pd.concat([full_grid, mine_grid], axis=1)

del mine_grid

### SWITCH ###
#full_grid.to_csv(path+"/full_grid_new_test.csv", index=False, encoding="utf-8")
pd.concat([full_grid, mine_grid], axis=1).to_csv(path+"/full_grid_new.csv", index=False)

###########################################################################

full_grid = full_grid.loc[:, ["GID_3", "distance_to_minecasualty"]]
full_grid = full_grid.loc[:, ~full_grid.columns.duplicated()]

grid_commune = full_grid.groupby("GID_3").agg(["mean"])

del full_grid

grid_commune.columns = grid_commune.columns.get_level_values(0)
grid_commune["cell_id"] = grid_commune.index
grid_commune = grid_commune.reset_index(drop=True)

grid_commune.to_csv(path+"/grid_commune_minecasualty.csv", index=False, encoding="utf-8")



















