
*global data "/sciclone/home20/cbaehr/cambodia/eba/inputData"
global data "/sciclone/scr20/cbaehr"

*global data "/Users/christianbaehr/Downloads"

global results "/sciclone/home20/cbaehr/cambodia/eba/new_results"
*global results "/Users/christianbaehr/Downloads"

**********

use "$data/panel_corrected_irrigation_formatted2.dta", clear

drop province_number district_number

* drop all observations if cell NDVI is never >0
replace ndvi = . if ndvi==0

* generate baseline ndvi measure (2002)
bysort cell_id (year): gen baseline_ndvi = ndvi[4]

outreg2 using "$results/summary_statistics_irrigation.doc", replace sum(log)
rm "$results/summary_statistics_irrigation.txt"


*model1
*gen temp = 1
*reghdfe ndvi trt_irrigation_overall, absorb(temp) cluster(commune_number year) pool(10)
*outreg2 using "$results/main_models_ndvi_irrigation.doc", replace tex noni nocons addtext("Year FEs", N, "Grid cell FEs", N, "Climate Controls", N)
*model2
*reghdfe ndvi trt_irrigation_overall, absorb(year) cluster(commune_number year) pool(10)
*outreg2 using "$results/main_models_ndvi_irrigation.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", N, "Climate Controls", N)
*model3
*reghdfe ndvi trt_irrigation_overall, absorb(year cell_id) cluster(commune_number year) pool(10)
*outreg2 using "$results/main_models_ndvi_irrigation.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", N)
*model4
*reghdfe ndvi trt_irrigation_overall temperature precip, absorb(year cell_id) cluster(commune_number year) pool(10)
*outreg2 using "$results/main_models_ndvi_irrigation.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
*model5
reghdfe ndvi trt_irrigation_overall temperature precip c.trt_irrigation_overall#c.(plantation concession protected_area), absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi_irrigation.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
*model6
reghdfe ndvi trt_irrigation_overall temperature precip c.trt_irrigation_overall#c.(protected_area dist_to_road), absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi_irrigation.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
*model7
reghdfe ndvi trt_irrigation_overall temperature precip c.trt_irrigation_overall#c.baseline_ndvi, absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi_irrigation.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
*model8
reghdfe ndvi trt_irrigation_overall temperature precip c.trt_irrigation_overall#c.(plantation concession protected_area baseline_ndvi), absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi_irrigation.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
*model9
reghdfe ndvi trt_irrigation_overall temperature precip c.trt_irrigation_overall#c.(plantation concession protected_area dist_to_road baseline_ndvi), absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi_irrigation.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

rm "$results/main_models_ndvi_irrigation.txt"

























