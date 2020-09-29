
path = "/sciclone/home20/cbaehr/cambodia/eba/inputData"

import pandas as pd
import numpy as np

grid = pd.read_csv(path+"/pre_1km_grid.csv")

adm = pd.read_csv(path+"/adm_grid.csv")

new_grid = pd.concat([grid.drop(["cell_id_x"], axis=1), adm[["GID_3"]]], axis=1)

new_grid.to_csv(path+"/pre_commune_grid.csv", index=False)

grid.sample(10000).to_csv(path+"/pre_commune_grid_test.csv", index=False)
