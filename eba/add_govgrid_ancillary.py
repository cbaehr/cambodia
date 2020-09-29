

path = "/sciclone/home20/cbaehr/cambodia/eba/inputData"
output = "/sciclone/scr20/cbaehr"

import pandas as pd
import numpy as np

temp_names = ["cell_id"]+["treatment_irrigation1000_"+str(i) for i in range(1999,2019)]+["treatment_irrigation2000_"+str(i) for i in range(1999,2019)]+["treatment_irrigation3000_"+str(i) for i in range(1999,2019)]+["treatment_irrigation4000_"+str(i) for i in range(1999,2019)]+["treatment_irrigation5000_"+str(i) for i in range(1999,2019)]

irrigation_grid = pd.read_csv(path+"/full_grid_irrigation.csv")
irrigation_grid = irrigation_grid[temp_names]

temp_names = ["treatment_roadsandbridges1000_"+str(i) for i in range(1999,2019)]+["treatment_roadsandbridges2000_"+str(i) for i in range(1999,2019)]+["treatment_roadsandbridges3000_"+str(i) for i in range(1999,2019)]+["treatment_roadsandbridges4000_"+str(i) for i in range(1999,2019)]+["treatment_roadsandbridges5000_"+str(i) for i in range(1999,2019)]

road_grid = pd.read_csv(path+"/full_grid_roads.csv")
road_grid = road_grid[temp_names]

adm_grid = pd.read_csv(path+"/adm_grid.csv")

grid = pd.concat([irrigation_grid, road_grid, adm_grid[["GID_3"]]], axis=1)
del irrigation_grid, road_grid

big_grid = pd.read_csv(path+"/merging_grid_1km.csv")

grid = big_grid.merge(grid, left_on="cell_id_y", right_on="cell_id")
del big_grid

grid = grid.loc[~grid["cell_id_x"].isnull(), ]
grid.drop(["cell_id"], axis=1, inplace=True)

grid.to_csv(output+"/pre_1km_grid_ancillary.csv", index=False)
