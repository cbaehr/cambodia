
path = "/sciclone/home20/cbaehr/cambodia/eba/inputData"

import pandas as pd
import numpy as np

gov_grid = pd.read_csv(path+"/governance_grid.csv")
print(gov_grid.shape)
gov_grid.drop(["cell_id"], axis=1, inplace=True)

mine_grid = pd.read_csv(path+"/mine_grid.csv")
print(mine_grid.shape)
mine_grid.drop(["cell_id"], axis=1, inplace=True)

main_grid = pd.read_csv(path+"/full_grid_new.csv")
print(main_grid.shape)
main_grid.drop(["plantation", "concession", "protected_area"], axis=1, inplace=True)

for i in range(1999, 2019):
	main_grid.loc[main_grid["ndvi"+str(i)]<=0, "ndvi"+str(i)] = np.nan
### NEED TO DO THE REGULAR PRE PANEL PROCESSING FOR THIS FINAL DATASET
for i in range(2001, 2018):
	main_grid.loc[main_grid["temp_"+str(i)]<=0, "temp_"+str(i)] = np.nan
for i in range(2000, 2017):
	main_grid.loc[(main_grid["precip_"+str(i)]<=0) | (main_grid["precip_"+str(i)]>1000), "precip_"+str(i)] = np.nan

main_grid = pd.concat([main_grid, gov_grid, mine_grid], axis=1)

del gov_grid, mine_grid

#main_grid.to_csv(path+"/full_grid_new.csv", index=False)

#main_grid.drop(["lon", "lat", "GID_1", "NAME_1", "GID_2", "NAME_2", "GID_3", "NAME_3", "gpw_density_2005", "gpw_density_2010", "gpw_density_2015", "gpw_density_2020"], axis=1, inplace=True)
main_grid.drop(["lon", "lat", "GID_1", "NAME_1", "GID_2", "NAME_2", "GID_3", "NAME_3", "gpw_density_2005", "gpw_density_2010", "gpw_density_2015", "gpw_density_2020"], axis=1, inplace=True)

grid = pd.read_csv(path+"/merging_grid_1km.csv")

grid = grid.merge(main_grid, left_on="cell_id_y", right_on="cell_id")

del main_grid

grid = grid.loc[~grid["cell_id_x"].isnull(), ]
grid.drop(["cell_id"], axis=1, inplace=True)

grid.to_csv(path+"/pre_1km_grid.csv", index=False)

grid.sample(10000).to_csv(path+"/pre_1km_grid_test.csv", index=False)






