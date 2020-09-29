
path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"

import pandas as pd
import geopandas as gpd
from shapely.geometry import shape, Point, MultiPoint, MultiPolygon
from shapely.prepared import prep
import fiona


pid = gpd.read_file(path+"/pid/pid2003-18_trimmed.geojson")
pid["geometry"] = pid["geometry"].centroid

protected_areas = gpd.read_file(path+"/protected_areas_dissolved.geojson")
bounds = protected_areas[["geometry"]].boundary

pa = fiona.open(path+"/protected_areas_dissolved.geojson")
pa = pa[0]
pa = shape(pa["geometry"])
prep_pa = prep(pa)

dist = []
dist2 = []

for i in range(0, 26675):
	dist.append(float(bounds.distance(pid["geometry"][i])[0]))
	dist2.append(prep_pa.intersects(pid["geometry"][i]))


dist3 = dist2

b = pd.Series(dist3)
c=b*1
c.describe()

pid2 = pid

#pid2["distance_to_pa"] = pd.Series(dist)
pid2["distance_to_pa"] = dist

pid2["distance_to_pa"].describe()
pid2.loc[dist3, "distance_to_pa"] = 0

#pid["geometry"]

#bounds.distance(pid["geometry"][1])

#pid2["distance_to_pa"] = pd.Series(dist)

#pid["geometry"]

#pid2 = gpd.GeoDataFrame(pid.drop(["geometry"], axis=1), crs="epsg:4326", geometry=pid["geometry"])


#gpd.GeoDataFrame(entity2).T.dtypes




pid2.to_file("/Users/christianbaehr/Downloads/pid.geojson", driver="GeoJSON")

