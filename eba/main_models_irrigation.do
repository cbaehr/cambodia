
global data "/sciclone/home20/cbaehr/cambodia/eba/inputData"
*global data "/Users/christianbaehr/Downloads"

global results "/sciclone/home20/cbaehr/cambodia/eba/new_results"
*global results "/Users/christianbaehr/Downloads"

**********

use "$data/panel_irrigation_formatted.dta", clear
rename trt_irrigation_overall trt_irrigation

replace ndvi = . if ndvi==0

gen dummy2002 = (year==2002) * ndvi
replace dummy2002 = . if year!=2002
egen baseline_ndvi = mean(dummy2002)
drop dummy2002

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
reghdfe ndvi trt_irrigation temperature precip c.trt_irrigation#c.(plantation concession protected_area), absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi_irrigation.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
*model6
reghdfe ndvi trt_irrigation temperature precip c.trt_irrigation#c.(protected_area distance_to_road), absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi_irrigation.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
*model7
reghdfe ndvi trt_irrigation temperature precip c.trt_irrigation#c.baseline_ndvi, absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi_irrigation.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
*model8
reghdfe ndvi trt_irrigation temperature precip c.trt_irrigation#c.(plantation concession protected_area baseline_ndvi), absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi_irrigation.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
*model9
reghdfe ndvi trt_irrigation temperature precip c.trt_irrigation#c.(plantation concession protected_area distance_to_road baseline_ndvi), absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi_irrigation.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

rm "$results/main_models_ndvi_irrigation.txt"

****************************************************************************************************


use "$data/panel_roads_formatted.dta", clear
rename trt_roads_overall trt_roads

replace ndvi = . if ndvi==0

gen dummy2002 = (year==2002) * ndvi
replace dummy2002 = . if year!=2002
egen baseline_ndvi = mean(dummy2002)
drop dummy2002

outreg2 using "$results/summary_statistics_roads.doc", replace sum(log)
rm "$results/summary_statistics_roads.txt"

*model1
gen temp = 1
reghdfe ndvi trt_roads, absorb(temp) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi_roads.doc", replace tex noni nocons addtext("Year FEs", N, "Grid cell FEs", N, "Climate Controls", N)
*model2
reghdfe ndvi trt_roads, absorb(year) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi_roads.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", N, "Climate Controls", N)
*model3
reghdfe ndvi trt_roads, absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi_roads.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", N)
*model4
reghdfe ndvi trt_roads temperature precip, absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi_roads.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
*model5
reghdfe ndvi trt_roads temperature precip c.trt_roads#c.(plantation concession protected_area) temperature precip, absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi_roads.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
*model6
reghdfe ndvi trt_roads temperature precip c.trt_roads#c.(protected_area distance_to_road), absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi_roads.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
*model7
reghdfe ndvi trt_roads temperature precip c.trt_roads#c.baseline_ndvi, absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi_roads.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
*model8
reghdfe ndvi trt_roads temperature precip c.trt_roads#c.(plantation concession protected_area baseline_ndvi), absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi_roads.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
*model9
reghdfe ndvi trt_roads temperature precip c.trt_roads#c.(plantation concession protected_area distance_to_road baseline_ndvi), absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_ndvi_roads.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

rm "$results/main_models_ndvi_roads.txt"










