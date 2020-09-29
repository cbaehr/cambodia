
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

* reghdfe, compile

use "$data/panel_formatted.dta", clear

bys year: su ndvi

* drop all observations if cell is never treated
egen max_trt = max(trt_overall), by(cell_id)
drop if max_trt==0
drop max_trt

* drop all observations if cell NDVI is never >0
egen max_ndvi = max(ndvi), by(cell_id)
drop if max_ndvi==0
drop max_ndvi

bys year: su ndvi

* build time to treatment measure
gen t1 = (trt_overall!=0) * year
replace t1 = . if t1==0
egen t1a = first(t1), by(cell_id)
egen t1b = mean(t1a), by(cell_id)
gen time_to_trt = year-t1b
drop t1 t1a t1b

* add 40 to avoid negative factor issue
replace time_to_trt = time_to_trt+40

* drop observations >4 periods before treatment or >10 periods after
drop if time_to_trt <36
drop if time_to_trt >50

bys time_to_trt: su ndvi

* memory saving
replace year = year-1998
drop province_number province_name district_number district_name commune_name plantation concession protected_area dist_to_city dist_to_road treecover trt1km trt2km trt3km trt4km trt5km trt_overall
drop if missing(ndvi) | missing(time_to_trt)
compress
sample 80

su

reghdfe ndvi ib40.time_to_trt, absorb(year cell_id) cluster(year commune_number) pool(10)
estimates store model1
estout model1 using "$results/model1_80.tsv", replace cells("b se") mlabels(,none)

reghdfe ndvi ib40.time_to_trt, absorb(year cell_id) cluster(year cell_id) pool(10)
estimates store model2
estout model2 using "$results/model2_80.tsv", replace cells("b se") mlabels(,none)

reghdfe ndvi ib40.time_to_trt temperature precip, absorb(year cell_id) cluster(year commune_number) pool(10)
estimates store model3
estout model3 using "$results/model3_80.tsv", replace cells("b se") mlabels(,none)

reghdfe ndvi ib40.time_to_trt temperature precip, absorb(year cell_id) cluster(year cell_id) pool(10)
estimates store model4
estout model4 using "$results/model4_80.tsv", replace cells("b se") mlabels(,none)








