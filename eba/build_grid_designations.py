

path="/sciclone/home20/cbaehr/cambodia/eba/inputData"

import numpy as np
import pandas as pd
from shapely.geometry import Point
import geopandas

empty_grid = pd.read_csv(path+"/empty_grid.csv")

grid_geometry = [Point(xy) for xy in zip(empty_grid.longitude, empty_grid.latitude)]

empty_grid_geo = geopandas.GeoDataFrame(empty_grid['cell_id'], crs={'init': 'epsg:4326'}, geometry=grid_geometry)

###

pa = geopandas.read_file(path+"/protected_areas.geojson")

pa_grid = geopandas.sjoin(empty_grid_geo, pa[["issuedate", "geometry"]], how='left', op='intersects')

pa_grid["issuedate"] = pd.to_datetime(pa_grid['issuedate'])

pa_grid = pa_grid.sort_values("issuedate", ascending=True).drop_duplicates("cell_id").sort_index()

pa_grid["pa_activedate"] = pa_grid["issuedate"].astype("str").str[:4]

pa_grid.drop(["geometry", "index_right", "issuedate"], axis=1, inplace=True)

####

elc = geopandas.read_file(path+"/economic_land_concessions.geojson")

elc_grid = geopandas.sjoin(empty_grid_geo, elc[["contract_0", "adjustment", "sub_decree", "last_updat", "geometry"]], how='left', op='intersects')

elc_grid["contract_0"] = pd.to_datetime(elc_grid["contract_0"], errors="coerce")
elc_grid["sub_decree"] = pd.to_datetime(elc_grid["sub_decree"], errors="coerce")

elc_grid1 = elc_grid.sort_values("contract_0", ascending=True).drop_duplicates("cell_id").sort_index()
elc_grid2 = elc_grid.sort_values("sub_decree", ascending=False).drop_duplicates("cell_id").sort_index()

elc_grid1.drop(["geometry", "index_right", "adjustment", "sub_decree", "last_updat"], axis=1, inplace=True)
elc_grid2.drop(["cell_id", "geometry", "index_right", "contract_0", "last_updat"], axis=1, inplace=True)

elc_grid_new = pd.concat([elc_grid1, elc_grid2], axis=1)

elc_grid_new["contract_0"] = elc_grid_new["contract_0"].astype("str").str[:4]
elc_grid_new["sub_decree"] = elc_grid_new["sub_decree"].astype("str").str[:4]

elc_grid_new.columns = ["cell_id", "elc_active_date", "elc_adjustment", "elc_change_date"]

####

plantation = geopandas.read_file(path+"/tree_plantations.geojson")

plantation_grid = geopandas.sjoin(empty_grid_geo, plantation[["type_text", "geometry"]], how='left', op='intersects')

plantation_grid = plantation_grid.drop_duplicates("cell_id")

plantation_grid.drop(["geometry", "index_right"], axis=1, inplace=True)

#plantation_grid["plantation"] = ~pd.isnull(plantation_grid["type_text"]) * 1

plantation_grid.columns = ["cell_id", "plantation_type"]

####

full_grid = pd.concat([pa_grid, elc_grid_new.drop(["cell_id"], axis=1), plantation_grid.drop(["cell_id"], axis=1)], axis=1)

full_grid.to_csv(path+"/designation_grid.csv", index=False)























