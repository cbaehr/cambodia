
global data "/sciclone/home20/cbaehr/cambodia/eba/inputData"
*global data "/Users/christianbaehr/Downloads"

global results "/sciclone/home20/cbaehr/cambodia/eba/new_results"
*global results "/Users/christianbaehr/Downloads"

**********

use "$data/panel_formatted.dta", clear

drop province_number district_number

replace ndvi = . if ndvi==0

egen max_trt_overall = max(trt_overall), by(cell_id)
drop if max_trt_overall==0
drop max_trt_overall

gen dummy2002 = (year==2002) * ndvi
replace dummy2002 = . if year!=2002
egen baseline_ndvi = mean(dummy2002)
drop dummy2002

*******************

replace year = year-1998
drop if missing(temperature) | missing(precip) | missing(ndvi)

compress


*model8
reghdfe ndvi trt_overall temperature precip c.trt_overall#c.(plantation concession protected_area baseline_ndvi), absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
*model9
reghdfe ndvi trt_overall temperature precip c.trt_overall#c.(plantation concession protected_area dist_to_road baseline_ndvi), absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

rm "$results/main_models_ndvi.txt"
