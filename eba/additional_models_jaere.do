
global data "/sciclone/scr20/cbaehr"
*global data "/Users/christianbaehr/Downloads"

global results "/sciclone/home20/cbaehr/cambodia/eba/new_results"
*global results "/Users/christianbaehr/Downloads"

**********

use "$data/panel_corrected_cgeo_formatted.dta", clear

gen trt_overall = 

* drop all observations if cell is never treated
egen max_trt_overall = max(trt_overall), by(cell_id)
drop if max_trt_overall==0
drop max_trt_overall

* drop all observations if cell NDVI is never >0
replace ndvi = . if ndvi==0

* generate baseline ndvi measure (2002)
bysort cell_id (year): gen baseline_ndvi = ndvi[4]

*table1
reghdfe ndvi trt_overall c.trt_overall#c.popdensity2000 temperature precip, absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/additional_models_ndvi.doc", replace tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

gen trt_dummy = (trt_overall>0)
reghdfe ndvi trt_dummy temperature precip, absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/additional_models_ndvi.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

reghdfe ndvi trt_overall temperature precip c.trt_overall#c.dist_to_city, absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/additional_models_ndvi.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

reghdfe ndvi trt_overall temperature precip c.trt_overall#c.dist_to_road, absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/additional_models_ndvi.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

reghdfe ndvi trt_overall temperature precip c.trt_overall#c.bombings, absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/additional_models_ndvi.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

reghdfe ndvi trt_overall temperature precip c.trt_overall#c.burials, absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/additional_models_ndvi.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

reghdfe ndvi trt_overall temperature precip c.trt_overall#c.memorials, absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/additional_models_ndvi.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

reghdfe ndvi trt_overall temperature precip c.trt_overall#c.prisons, absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/additional_models_ndvi.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

reghdfe ndvi trt_overall temperature precip c.trt_overall#c.(bombings burials memorials prisons), absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/additional_models_ndvi.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

reghdfe ndvi trt_overall temperature precip c.trt_overall#c.(plantation concession protected_area baseline_ndvi distance_to_road bombings burials memorials prisons), absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/additional_models_ndvi.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)


rm "$results/additional_models_ndvi.txt"




*model1
gen temp = 1
reghdfe ndvi trt_overall, absorb(temp) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi.doc", replace tex noni nocons addtext("Year FEs", N, "Grid cell FEs", N, "Climate Controls", N)
*model2
reghdfe ndvi trt_overall, absorb(year) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", N, "Climate Controls", N)
*model3
reghdfe ndvi trt_overall, absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", N)
*model4
reghdfe ndvi trt_overall temperature precip, absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
*model5
reghdfe ndvi trt_overall temperature precip c.trt_overall#c.(plantation concession protected_area), absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
*model6
reghdfe ndvi trt_overall temperature precip c.trt_overall#c.(protected_area dist_to_road), absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
*model7
reghdfe ndvi trt_overall temperature precip c.trt_overall#c.baseline_ndvi, absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
*model8
reghdfe ndvi trt_overall temperature precip c.trt_overall#c.(plantation concession protected_area baseline_ndvi), absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
*model9
reghdfe ndvi trt_overall temperature precip c.trt_overall#c.(plantation concession protected_area dist_to_road baseline_ndvi), absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

