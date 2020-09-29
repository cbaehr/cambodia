
import delimited "/sciclone/scr20/cbaehr/panel_corrected_irrigation.csv", clear

replace ndvi = . if ndvi==-9999
replace ndvi = ndvi*0.0001
replace ndvi = . if ndvi<0

replace precip = "." if precip=="NA"
destring precip, replace
replace precip = . if precip<0 | precip>1000

replace temperature = "." if temperature=="NA"
destring temperature, replace
replace temperature = . if temperature==0

drop longitude latitude province_number province_name district_number commune_name plantation concession protected_area dist_to_city dist_to_road popdensity dist_to_minecasualty

gen trt_irrigation_overall = trt1km_irrigation + trt2km_irrigation + trt3km_irrigation + trt4km_irrigation + trt5km_irrigation

drop trt1km_irrigation trt2km_irrigation trt3km_irrigation trt4km_irrigation trt5km_irrigation

replace treecover="." if treecover=="NA"
destring treecover, replace

*reghdfe ndvi trt_irrigation_overall temperature precip, absorb(cell_id year) cluster(commune_number year) pool(10)
*outreg2 using "/sciclone/home20/cbaehr/cambodia/eba/new_results/irrigation_models_fullsample.doc", replace tex noni nocons ctitle(ndvi) addtext("Sample", Full, "Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

reghdfe treecover trt_irrigation_overall temperature precip, absorb(cell_id year) cluster(commune_number year) pool(10)
outreg2 using "/sciclone/home20/cbaehr/cambodia/eba/new_results/irrigation_models_fullsample.doc", append tex noni nocons ctitle(treecover) addtext("Sample", Full, "Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

***

import delimited "/sciclone/scr20/cbaehr/panel_corrected_roads.csv", clear

replace ndvi = . if ndvi==-9999
replace ndvi = ndvi*0.0001
replace ndvi = . if ndvi<0

replace precip = "." if precip=="NA"
destring precip, replace
replace precip = . if precip<0 | precip>1000

replace temperature = "." if temperature=="NA"
destring temperature, replace
replace temperature = . if temperature==0

drop longitude latitude province_number province_name district_number commune_name plantation concession protected_area dist_to_city dist_to_road popdensity dist_to_minecasualty

gen trt_roads_overall = trt1km_roads + trt2km_roads + trt3km_roads + trt4km_roads + trt5km_roads

drop trt1km_roads trt2km_roads trt3km_roads trt4km_roads trt5km_roads


replace treecover="." if treecover=="NA"
destring treecover, replace


reghdfe ndvi trt_roads_overall temperature precip, absorb(cell_id year) cluster(commune_number year) pool(10)
outreg2 using "/sciclone/home20/cbaehr/cambodia/eba/new_results/roads_models_fullsample.doc", replace tex noni nocons ctitle(ndvi) addtext("Sample", Full, "Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

reghdfe treecover trt_roads_overall temperature precip, absorb(cell_id year) cluster(commune_number year) pool(10)
outreg2 using "/sciclone/home20/cbaehr/cambodia/eba/new_results/_models_fullsample.doc", append tex noni nocons ctitle(treecover) addtext("Sample", Full, "Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)





















