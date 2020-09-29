
global data "/sciclone/home20/cbaehr/cambodia/eba/inputData"
*global data "/Users/christianbaehr/Downloads"

global results "/sciclone/home20/cbaehr/cambodia/eba/new_results"
*global results "/Users/christianbaehr/Downloads"

**********

use "$data/panel_formatted.dta", clear

replace ndvi = . if ndvi==0

egen max_trt_overall = max(trt_overall), by(cell_id)
drop if max_trt_overall==0
drop max_trt_overall

bysort cell_id (year): gen baseline_ndvi = ndvi[4]

drop province_number province_name district_number district_name commune_name popdensity2000 treecover trt1km trt2km trt3km trt4km trt5km

*model7
*reghdfe ndvi trt_overall temperature precip c.trt_overall#c.baseline_ndvi, absorb(year cell_id) cluster(commune_number year) pool(10)
*outreg2 using "$results/main_models_baselinendvi.doc", replace tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

*model8
reghdfe ndvi trt_overall temperature precip c.trt_overall#c.(plantation concession protected_area baseline_ndvi), absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_baselinendvi.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

*model9
reghdfe ndvi trt_overall temperature precip c.trt_overall#c.(plantation concession protected_area dist_to_road baseline_ndvi), absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_baselinendvi.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
