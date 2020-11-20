
### Intermediate Data and Programming for *Linking Local Infrastructure Development and Deforestation*
#### Baehr, BenYishay, and Parks
#### November 2020


##### Data Processing and Consolidation
Primary data processing was done using Python. We originally constructed a GIS grid of ~27.5 sq. meter cells. The grid was built to map each cell to a corresponding pixel in the Hansen Forest Cover Change raster dataset of tree canopy cover for the year 2000. Each grid cell thus corresponds to a single Hansen pixel. We then map Hansen tree cover values onto the corresponding grid cells. Cells with tree cover values >=25% (e.g. "forested") are maintained, and cells with tree cover <25% are dropped. We then build a time-series "tree cover" measure indicating whether cell i is forested in year t. All cells in our sample are forested in 2000, and thus have values of 1. We incorporate the binary Hansen Forest Loss raster dataset, which indicates the year a cell shifted from a "forest" to "non-forest state". We map this forest loss dataset onto our panel, and assign each cell a "tree cover" value of 1 until the year it shifts to a non-forest, and 0 thereafter.

We also incorporate NDVI data sourced from the Landsat satellite. Landsat 16-day OLI imagery is aggregated to annual scales, and we mask out medium- or high-cloud cover areas to avoid biased greenness values. This raster data shares a similar resolution to the Hansen products (~30m pixel), but pixels are not aligned to Hansen. We thus resample each annual NDVI image using bilinear interpolation to match the Hansen alignment. This way, we achieve a unique NDVI value for each grid cell in each year with light processing of the data. Resampled NDVI values are mapped onto the grid.

Treatment data is sourced from the Cambodia NCDDS Project Implementation Database. The dataset contains completion date and location information (lon/lat) on 41,850 development activities associated with the Commune/Sangkat Fund. We build a 3km circular buffer around treatment location points then spatially join our grid with these buffered treatment sites, allowing us to identify all projects within 3 kilometers of a grid cell as well as when these projects were completed. Using this information, we build a cumulative count of completed projects occuring within 5km of each grid cell. To get road- and irrigation-specific project counts we filter the treatment dataset by the included "project type" variable to the appropriate subset of projects, then rerun the spatial join with the grid using the type-specific project locations only. The "other" project count is simply the residual when irrigation- and road-project counts are deducted from the overall project count.

Temperature and precipitation data were in raster format, but at much weaker spatial resolution than 30m. Thus, we extract these rasters by sampling them using the centroid of our grid cells. In the rare cases that a grid cell falls on the border of two raster pixels, the cell is filled with the raster value that overlaps the center of the cell. This process is repeated using each annual raster dataset for both temperature and precipitation data.

Economic land concessions, tree plantations, and protected areas data were all provided in shapefiles, each with polygons representing the areas falling under the corresponding governance regime. We perform a spatial intersection of each shapefile with our grid to obtain separate indicators of whether grid cell i falls within each governance regime. 

The CGEO exposure variables are provided as a shapefile with points indicating the location of a bombing, burial, memorial, or prison. We buffer each point by 1km and intersect the result with our grid to create an indicator of whether a cell is within 1km of a CGEO site. This is done separately for each type of site.

Distance to city, road and mine casualty are calculated via a two-stage process. We use a GIS dataset from GeoNames tracking the lon/lat of cities in Cambodia with population>500. We use the distancerasters package produced by Seth Goodman to first build a countrywide raster layer with 30m pixels reflecting distance to the nearest city. We then map these values onto our grid. We conduct the same process for distance to roads using linear road data and distance to nearest mine casualty using point data produced on casualty locations by Open Development Cambodia. 

Population density data was retrieved in raster format from the Gridded Population of the World dataset for the year 2000. Like for temperature and precipitation rasters, this raster data is relatively coarse so we extract the value that overlaps the centroid of each grid cell.


##### Aggregation
To produce the 1km level dataset, we aggregate our 30m panel in Python. We build a 1 sq. km grid of cells throughout Cambodia, and 30m cells are grouped into the 1km cell that contains their centroid. Not all 1km cells contain the same number of 30m cells. This is for a number of reasons, including that many non-forested cells are dropped and some 1km cells partially overlap with national borders. Thus, we record the number of 30m cells that contribute to the aggregation. 

All this data merging and aggregation produces a cross-sectional dataset with one 1km grid cell per row. We "reshape" our dataset in Python to create a panel format, with each observation measuring a single year for a grid cell. The 1km panel is then exported for analysis in Stata.

Note: to create the commune-level dataset, we aggregate the 30m cells. We do NOT use the 1km grid cell dataset to aggregate to the commune level, as this would introduce some avoidable measurement error. We essentially use the same process to aggregate, but we are aggregating to commune-level administrative boundaries (retrieved from GADM). We then export the commune-level panel for analysis in Stata.










