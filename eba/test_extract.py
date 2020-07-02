
my_dir = '/sciclone/home20/cbaehr/cambodia/eba/inputData'

import pandas as pd
import rasterio
import time

starttime_2 = time.time()


pts = pd.read_csv(my_dir+"/empty_grid.csv")
pts.index = range(len(pts))
coords = [(x,y) for x, y in zip(pts.longitude, pts.latitude)]

src = rasterio.open(my_dir+'/Hansen_treecover2000_cambodia_adjusted.tif')
pts['hansen'] = [x[0] for x in src.sample(coords)]

for i in range(1999, 2019):
	src = rasterio.open(my_dir+'/ndvi/'+str(i)+'_all.tif')
	pts['ndvi'+str(i)] = [x[0] for x in src.sample(coords)]

endtime_2 = time.time()

print(endtime_2-starttime_2)

pts.to_csv(my_dir+'/test_grid.csv', index=False)










