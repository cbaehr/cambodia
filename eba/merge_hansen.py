
import rasterio
from rasterio.plot import show
from rasterstats import zonal_stats
#import osmnx as ox
import geopandas as gpd
import pandas as pd
from shapely.geometry import shape, Point, MultiPoint, MultiPolygon


path = "/sciclone/home20/cbaehr/cambodia/eba/inputData"

grid = pd.read_csv(path+"/full_grid.csv")


geometry = [Point(xy) for xy in zip(grid.longitude, grid.latitude)]
crs = {'init': 'epsg:4326'}
gdf = gpd.GeoDataFrame(grid['cell_id'], crs=crs, geometry=geometry)

hansen = gpd.read_file(path+"/hansen_grid_1km.geojson")


cols = ["pcttreecover" + str(i) for i in range(2000, 2018)] + ["geometry"]

hansen_grid = gpd.sjoin(gdf, hansen[cols], how='left', op='intersects')

new_cols = ["pcttreecover" + str(i) for i in range(2000, 2018)]

full_grid = pd.concat([grid.reset_index(drop=True), hansen_grid[new_cols].reset_index(drop=True)], axis=1)

full_grid.to_csv(path+"/full_grid2.csv", index=False)




