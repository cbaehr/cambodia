
path="/sciclone/home20/cbaehr/cambodia/eba/inputData"

import pandas as pd

empty_grid = pd.read_csv(path+"/empty_grid.csv")

###

adm_grid = pd.read_csv(path+"/adm_grid.csv")
adm_grid.drop(["cell_id"], axis=1, inplace=True)

grid = pd.concat([empty_grid.reset_index(drop=True), adm_grid], axis=1)

del empty_grid, adm_grid

###

ndvi_grid = pd.read_csv(path+"/ndvi_grid.csv")
ndvi_grid.drop(["cell_id"], axis=1, inplace=True)

grid = pd.concat([grid.reset_index(drop=True), ndvi_grid], axis=1)

del ndvi_grid

###

treatment_grid = pd.read_csv(path+"/treatment_grid.csv")
treatment_grid.drop(["cell_id", "longitude", "latitude"], axis=1, inplace=True)

grid = pd.concat([grid.reset_index(drop=True), treatment_grid], axis=1)

del treatment_grid

###

precip_grid = pd.read_csv(path+"/precip_grid.csv")
precip_grid.drop(["cell_id"], axis=1, inplace=True)

grid = pd.concat([grid.reset_index(drop=True), precip_grid], axis=1)

del precip_grid

###

temperature_grid = pd.read_csv(path+"/temperature_grid.csv")
temperature_grid.drop(["cell_id"], axis=1, inplace=True)

grid = pd.concat([grid.reset_index(drop=True), temperature_grid], axis=1)

del temperature_grid

###

designation_grid = pd.read_csv(path+"/designation_grid.csv")
designation_grid.drop(["cell_id"], axis=1, inplace=True)

grid = pd.concat([grid.reset_index(drop=True), designation_grid], axis=1)

###

grid.to_csv(path+"/full_grid.csv", index=False)



