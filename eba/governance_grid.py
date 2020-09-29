

#path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"
path = "/sciclone/home20/cbaehr/cambodia/eba/inputData"

import fiona
from shapely.geometry import shape, Point, MultiPoint, MultiPolygon
from shapely.prepared import prep
import pandas as pd

###

grid = pd.read_csv(path+"/empty_grid.csv").reset_index(drop=True)

###

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

###

# iterate through each grid cell to determine whether it intersects a plantation,
# concession, or PA
for _, row in grid.iterrows():
    c = Point(row['lon'], row['lat'])
    plantations_col.append(prep_plantations.intersects(c))
    concessions_col.append(prep_concessions.intersects(c))
    protected_areas_col.append(prep_protected_areas.intersects(c))

###

# create empty df to store land designation dummies
land_designation = pd.DataFrame()
land_designation.insert(loc=0, column="cell_id", value=grid["cell_id"])
land_designation.insert(loc=1, column='plantation', value=plantations_col)
land_designation.insert(loc=2, column='concession', value=concessions_col)
land_designation.insert(loc=3, column='protected_area', value=protected_areas_col)

land_designation["plantation"] = land_designation["plantation"].astype(int)
land_designation["concession"] = land_designation["concession"].astype(int)
land_designation["protected_area"] = land_designation["protected_area"].astype(int)

# export land designation grid
land_designation.reset_index(drop=True).to_csv(path+"/governance_grid.csv", index=False)











