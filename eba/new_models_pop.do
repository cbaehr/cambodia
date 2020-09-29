
*import delimited "/Users/christianbaehr/Downloads/panel_corrected_test.csv", clear
import delimited "/sciclone/home20/cbaehr/cambodia/eba/inputData/panel_corrected.csv", clear

su

drop longitude latitude province_number province_name district_number district_name commune_name plantation concession protected_area dist_to_city dist_to_road popdensity2000 treecover

replace ndvi = . if ndvi==-9999
replace ndvi = ndvi*0.0001
replace ndvi = . if ndvi<0

replace precip = "." if precip=="NA"
destring precip, replace
replace precip = . if precip<0 | precip>1000

replace temperature = "." if temperature=="NA"
destring temperature, replace
replace temperature = . if temperature==0

gen trt_overall = trt1km + trt2km + trt3km + trt4km + trt5km

drop trt1km trt2km trt3km trt4km trt5km

sort cell_id year

*merge 1:1 _n using "/Users/christianbaehr/Downloads/panel_corrected_irrigation_merge_test.dta"
merge 1:1 _n using "/sciclone/scr20/cbaehr/panel_corrected_irrigation_merge.dta"

drop _merge

*merge 1:1 _n using "/Users/christianbaehr/Downloads/panel_corrected_roads_merge_test.dta"
merge 1:1 _n using "/sciclone/scr20/cbaehr/panel_corrected_roads_merge.dta"

gen trt_other_overall = trt_overall - (trt_roads_overall+trt_irrigation_overall)

*su

gen high_pop = (popdensity2000>=1000)


reghdfe ndvi 0.high_pop#c.(trt_roads_overall trt_irrigation_overall trt_other_overall) 1.high_pop#c.(trt_roads_overall trt_irrigation_overall trt_other_overall) temperature precip, absorb(cell_id year) cluster(commune_number year) pool(10)

outreg2 using "/sciclone/home20/cbaehr/cambodia/eba/new_results/new_models_pop.doc", replace tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)


reghdfe ndvi trt_roads_overall trt_irrigation_overall trt_other_overall temperature precip if province_number!="KHM.16_1", absorb(cell_id year) cluster(commune_number year) pool(10)

outreg2 using "/sciclone/home20/cbaehr/cambodia/eba/new_results/new_models_pop.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)













