
path = "/sciclone/scr20/cbaehr"

import pandas as pd

grid = pd.read_csv(path+"/pre_1km_grid_ancillary.csv")

grid.columns

old_names = []
for i in [1000, 2000, 3000, 4000, 5000]:
	for j in range(1999, 2019):
		old_names = old_names + ["treatment_roadsandbridges"+str(i)+"_"+str(j)]

new_names = []
for i in [1, 2, 3, 4, 5]:
	for j in range(1999, 2019):
		new_names = new_names + ["trtroads"+str(i)+"km_"+str(j)]

names_dict = {}
for i in range(0, len(old_names)):
	names_dict[old_names[i]] = new_names[i]

grid.rename(columns=names_dict, inplace=True)

grid.to_csv(path+"/pre_1km_grid_ancillary.csv", index=False)

grid.describe()