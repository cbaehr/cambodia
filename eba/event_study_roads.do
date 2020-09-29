
clear all
set more off
set segmentsize 2g
set min_memory 16g

*ssc install reghdfe
*ssc install ftools
*ssc install erepost

*global data "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"
global data "/sciclone/home20/cbaehr/cambodia/eba/inputData"

*global results "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"
global results "/sciclone/home20/cbaehr/cambodia/eba/new_results"

reghdfe, compile

use "$data/panel_roads_formatted.dta", clear
rename trt_roads_overall trt_roads

bys year: su ndvi

egen max_trt = max(trt_roads), by(cell_id)
drop if max_trt==0
drop max_trt

egen max_ndvi = max(ndvi), by(cell_id)
drop if max_ndvi==0
drop max_ndvi

bys year: su ndvi

gen t1 = (trt_roads!=0) * year
replace t1 = . if t1==0
egen t1a = first(t1), by(cell_id)
egen t1b = mean(t1a), by(cell_id)
gen time_to_trt = year-t1b
drop t1 t1a t1b

replace time_to_trt = time_to_trt+40

drop if time_to_trt <36
drop if time_to_trt >50

bys time_to_trt: su ndvi

replace year = year-1998

drop province_number province_name district_number district_name commune_name distance_to_city distance_to_road treecover trt_roads1km trt_roads2km trt_roads3km trt_roads4km trt_roads5km trt_roads

drop if missing(ndvi) | missing(time_to_trt)

compress

*sample 80

su

reghdfe ndvi ib40.time_to_trt, absorb(year cell_id) cluster(year commune_number) pool(10)
estimates store model1
estout model1 using "$results/model1_roads.tsv", replace cells("b se") mlabels(,none)

reghdfe ndvi ib40.time_to_trt, absorb(year cell_id) cluster(year cell_id) pool(10)
estimates store model2
estout model2 using "$results/model2_roads.tsv", replace cells("b se") mlabels(,none)

reghdfe ndvi ib40.time_to_trt temperature precip, absorb(year cell_id) cluster(year commune_number) pool(10)
estimates store model3
estout model3 using "$results/model3_roads.tsv", replace cells("b se") mlabels(,none)

reghdfe ndvi ib40.time_to_trt temperature precip, absorb(year cell_id) cluster(year cell_id) pool(10)
estimates store model4
estout model4 using "$results/model4_roads.tsv", replace cells("b se") mlabels(,none)






