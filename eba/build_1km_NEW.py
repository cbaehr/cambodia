
home = "/sciclone/home20/cbaehr/cambodia/eba/inputData"
scr = "/sciclone/scr20/cbaehr"

import pandas as pd

empty_grid = pd.read_csv(home+"/empty_grid.csv", nrows=5000)

treatment_grid = pd.read_csv(home+"/treatment_grid.csv", nrows=5000)

treatment_irrigation_grid = pd.read_csv(home+"/irrigation_grid.csv", nrows=5000)

treatment_roads_grid = pd.read_csv(home+"/roads_grid.csv", nrows=5000)





