
import pandas as pd

dat = pd.read_csv("/Users/christianbaehr/Downloads/commune_grid_mine.csv")
dat.drop(["v2", "cell_id_x"], axis=1, inplace=True)

dat2 = pd.read_csv("/Users/christianbaehr/Downloads/full_grid_commune.csv")

keep_cols = ["gid_3", "NAME_2", "GID_2", "NAME_1", "GID_1"]+ ["treatment_irrigation1000_"+str(i) for i in range(1999, 2019)]+["treatment_irrigation2000_"+str(i) for i in range(1999, 2019)]+["treatment_irrigation3000_"+str(i) for i in range(1999, 2019)]+["treatment_irrigation4000_"+str(i) for i in range(1999, 2019)]+["treatment_irrigation5000_"+str(i) for i in range(1999, 2019)]+["trtroads1km_"+str(i) for i in range(1999, 2019)]+["trtroads2km_"+str(i) for i in range(1999, 2019)]+["trtroads3km_"+str(i) for i in range(1999, 2019)]+["trtroads4km_"+str(i) for i in range(1999, 2019)]+["trtroads5km_"+str(i) for i in range(1999, 2019)]
dat2 = dat2[keep_cols]

dat3 = pd.concat([dat, dat2], axis=1)

import geopandas as gpd

geo = gpd.read_file("/Users/christianbaehr/Box Sync/cambodia/eba/inputData/gadm36_KHM_3.geojson")

dat4 = dat.merge(geo, left_on="commune_number", right_on="GID_3")

dat5=gpd.GeoDataFrame(dat4, crs="epsg:4326", geometry=dat4["geometry"])

dat4.drop(["geometry"],axis=1).to_csv("/Users/christianbaehr/Downloads/pre_panel_commune.csv", index=False)

dat5.to_file("/Users/christianbaehr/Downloads/test.geojson", driver="GeoJSON")