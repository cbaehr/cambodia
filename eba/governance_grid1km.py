
### SWITCH ###
#path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"
path = "/sciclone/home20/cbaehr/cambodia/eba/inputData"

import fiona
import pandas as pd
import geopandas as gpd
from shapely.geometry import shape, Point, MultiPoint, MultiPolygon
from shapely.prepared import prep
import numpy as np
from osgeo import gdal, ogr
import re
import itertools

grid = pd.read_csv(path+"/governance_grid.csv")


