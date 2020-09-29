
* global data "/Users/christianbaehr/Downloads"
* global data "/sciclone/home20/cbaehr/cambodia/eba/inputData"

global data "/sciclone/scr20/cbaehr"

* import delimited "$data/pre_1km_grid.csv", clear
import delimited "$data/pre_panel_corrected_cgeo_mines.csv", clear

drop province_name province_number district_name district_number commune_name latitude longitude treecover1999 temperature1999 temperature2000 temperature2018 precip1999 precip2017 precip2018
su

local var "ndvi1999 ndvi2000 ndvi2001 ndvi2002 ndvi2003 ndvi2004 ndvi2005 ndvi2006 ndvi2007 ndvi2008 ndvi2009 ndvi2010 ndvi2011 ndvi2012 ndvi2013 ndvi2014 ndvi2015 ndvi2016 ndvi2017 ndvi2018"

foreach i of local var {
	replace `i' = `i' / 10000
}

replace dist_to_city = dist_to_city/1000
replace dist_to_road = dist_to_road/1000
replace distance_to_minecasualty = distance_to_minecasualty/1000

ds commune_number cell_id, not
collapse (count) count=cell_id (mean) `r(varlist)', by(commune_number)

su

export delimited "$data/commune_grid_mine.csv", replace

