
use "/sciclone/home20/cbaehr/cambodia/eba/inputData/panel_formatted.dta"

bysort cell_id (year): gen baseline_ndvi1 = ndvi[4]

gen dummy2002 = (year==2002) * ndvi
replace dummy2002 = . if year!=2002
egen baseline_ndvi2 = mean(dummy2002)
drop dummy2002

su year ndvi baseline_ndvi1 baseline_ndvi2
