
*ssc install erepost

global data "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"
*global data "/sciclone/home20/cbaehr/cambodia/eba/inputData"

global results "/Users/christianbaehr/Box Sync/cambodia/eba/new_results"
*global results "/sciclone/home20/cbaehr/cambodia/eba/new_results"

use "$data/panel_1km_formatted.dta", clear

gen t1 = (trt_overall!=0) * year
replace t1 = . if t1==0
egen t1a = first(t1), by(cell_id)
egen t1b = mean(t1a), by(cell_id)
gen time_to_trt = year-t1b

replace time_to_trt = time_to_trt+40
replace time_to_trt = . if time_to_trt <30
replace time_to_trt = . if time_to_trt >50

drop t1 t1a t1b

collapse

drop province_number province_name district_number district_name commune_name treecover trt1km trt2km trt3km trt4km trt5km trt_overall

reghdfe ndvi ib40.time_to_trt, absorb(year cell_id) cluster(year commune_id)
estimates store model1
estout model1 using "$results/model1_1km.tsv", replace cells("b se") mlabels(,none)

reghdfe ndvi ib40.time_to_trt, absorb(year cell_id) cluster(year cell_id)
estimates store model2
estout model2 using "$results/model2_1km.tsv", replace cells("b se") mlabels(,none)


reghdfe ndvi ib40.time_to_trt temperature precip, absorb(year cell_id) cluster(year commune_id)
estimates store model3
estout model3 using "$results/model3_1km.tsv", replace cells("b se") mlabels(,none)


reghdfe ndvi ib40.time_to_trt temperature precip, absorb(year cell_id) cluster(year cell_id)
estimates store model4
estout model4 using "$results/model4_1km.tsv", replace cells("b se") mlabels(,none)








