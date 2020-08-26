
#path = "/sciclone/home20/cbaehr/cambodia/eba/inputData"
#path = "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"
path = "/Users/christianbaehr/Desktop"

import os
import pandas as pd
import rasterio

src = path+"/Hansen_treecover2000_trimmed.tif"

treecover = rasterio.open(src, "r")
treecover_array = treecover.read()
treecover_vals = treecover.read(1)

mask_src = path+"/Hansen_datamask_trimmed.tif"
mask = rasterio.open(mask_src, "r")
mask_vals = mask.read(1)
treecover_vals[mask_vals!=1] = 255

###

treecover2000 = (treecover_vals>25) * 1
treecover2000[treecover_vals==255] = 255

loss_src = path+"/Hansen_lossyear_trimmed.tif"
loss = rasterio.open(loss_src, "r")
loss_vals = loss.read(1)
loss_vals[treecover_vals==255] = 255

tc_mask = ((treecover2000==0) & (loss_vals!=0))
treecover2000[tc_mask] = 255

treecover_dict = {}
treecover_dict["treecover2000"] = treecover2000

for i in range(1, 19):
	temp = (loss_vals==i)*1
	temp[treecover_vals==255] = 0
	treecover_dict["treecover{0}".format(i+2000)] = treecover_dict["treecover{0}".format(i+1999)] - temp

###

count = 1
with open(path+"/hansen_grid.csv", "w") as f:
	a=f.write("cell_id,lon,lat,tc2000,tc2001,tc2002,tc2003,tc2004,tc2005,tc2006,tc2007,tc2008,tc2009,tc2010,tc2011,tc2012,tc2013,tc2014,tc2015,tc2016,tc2017,tc2018\n")
	for i in range(treecover_array.shape[1]):
		for j in range(treecover_array.shape[2]):
			temp = treecover_vals[i, j]
			if (temp!=255 and temp>25):
				tc = [str(treecover_dict["treecover{0}".format(k+2000)][i,j]) for k in range(0, 19)]
				x, y = treecover.xy(i, j)
				out = [str(count)] + [str(x)] + [str(y)] + tc
				a = f.write(",".join(out)+"\n")
				count = count+1

###

grid = pd.read_csv(path+"/hansen_grid.csv")
grid.drop(["lon", "lat"], axis=1).to_csv(path+"/hansen_grid.csv", index=False)
grid[["cell_id", "lon", "lat"]].to_csv(path+"/empty_grid.csv", index=False)

del grid

###

ndvi_dict = {}

for i in range(1999, 2019):
	ndvi = rasterio.open(path+"/ndvi_adjusted/ndvi_landsat_"+str(i)+"_adjusted_masked.tif", "r")
	if i==1999:
		ndvi_array=ndvi.read()
	ndvi_dict["ndvi{0}".format(i)] = ndvi.read(1)

count = 1
with open(path+"/ndvi_grid.csv", "w") as f:
	a=f.write("cell_id,ndvi1999,ndvi2000,ndvi2001,ndvi2002,ndvi2003,ndvi2004,ndvi2005,ndvi2006,ndvi2007,ndvi2008,ndvi2009,ndvi2010,ndvi2011,ndvi2012,ndvi2013,ndvi2014,ndvi2015,ndvi2016,ndvi2017,ndvi2018\n")
	for i in range(ndvi_array.shape[1]):
		for j in range(ndvi_array.shape[2]):
			temp=treecover_vals[i, j]
			if (temp!=255 and temp>25):
				vals = [str(ndvi_dict["ndvi{0}".format(k)][i,j]) for k in range(1999, 2019)]
				out = [str(count)] + vals
				a = f.write(",".join(out)+"\n")
				count = count+1











