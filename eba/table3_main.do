
global data "/sciclone/home20/cbaehr/cambodia/eba/inputData"
*global data "/Users/christianbaehr/Downloads"

global results "/sciclone/home20/cbaehr/cambodia/eba/new_results"
*global results "/Users/christianbaehr/Downloads"

**********

use "$data/panel_formatted_test_updated.dta", clear

replace ndvi = . if ndvi==0

egen max_trt_overall = max(trt_irrigation), by(cell_id)
drop if max_trt_overall==0
drop max_trt_overall

bysort cell_id (year): gen baseline_ndvi = ndvi[4]

outreg2 using "$results/summary_statistics_irrigation.doc", replace sum(log)
rm "$results/summary_statistics_irrigation.txt"

*model1
gen temp = 1
reghdfe ndvi trt_irrigation, absorb(temp) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi_irrigation.doc", replace tex noni nocons addtext("Year FEs", N, "Grid cell FEs", N, "Climate Controls", N)
*model2
reghdfe ndvi trt_irrigation, absorb(year) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi_irrigation.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", N, "Climate Controls", N)
*model3
reghdfe ndvi trt_irrigation, absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi_irrigation.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", N)
*model4
reghdfe ndvi trt_irrigation temperature precip, absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi_irrigation.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
*model5
reghdfe ndvi c.trt_irrigation#c.(plantation concession protected_area) temperature precip, absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi_irrigation.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
*model6
reghdfe ndvi c.trt_irrigation#c.(protected_area distance_to_road) temperature precip, absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi_irrigation.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
*model7
reghdfe ndvi c.trt_irrigation#c.baseline_ndvi temperature precip, absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi_irrigation.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
*model8
reghdfe ndvi c.trt_irrigation#c.(plantation concession protected_area baseline_ndvi) temperature precip, absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi_irrigation.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
*model9
reghdfe ndvi c.trt_irrigation#c.(plantation concession protected_area distance_to_road baseline_ndvi) temperature precip, absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi_irrigation.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

rm "$results/main_models_ndvi_irrigation.txt"
