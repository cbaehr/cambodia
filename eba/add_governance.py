



path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"

import fiona
import pandas as pd
import geopandas as gpd
from shapely.geometry import shape, Point, MultiPoint, MultiPolygon
from shapely.prepared import prep
import numpy as np
from osgeo import gdal, ogr
import re
import itertools

empty_grid = gpd.read_file(path+"/empty_grid_1km.geojson")

# load plantations shapefile and prepare to merge with grid
plantations = fiona.open(path+"/tree_plantations_dissolved.geojson")
plantations = plantations[0]
plantations = shape(plantations['geometry'])
prep_plantations = prep(plantations)

# load concessions shapefile and prepare to merge with grid
concessions = fiona.open(path+"/economic_land_concessions_dissolved.geojson")
concessions = concessions[0]
concessions = shape(concessions['geometry'])
prep_concessions = prep(concessions)

# load protected areas shapefile and prepare to merge with grid
protected_areas = fiona.open(path+"/protected_areas_dissolved.geojson")
protected_areas = protected_areas[0]
protected_areas = shape(protected_areas['geometry'])
prep_protected_areas = prep(protected_areas)

# create empty lists to store land designation dummies
plantations_col = []
concessions_col = []
protected_areas_col = []
