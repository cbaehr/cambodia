
*global data "/sciclone/home20/cbaehr/cambodia/eba/inputData"
*global data "/Users/christianbaehr/Downloads"
global data "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"

*global results "/sciclone/home20/cbaehr/cambodia/eba/results"
*global results "/Users/christianbaehr/Downloads"
global results "/Users/christianbaehr/Box Sync/cambodia/eba/results"


use "$data/panel_formatted_hansen.dta", clear

*tsset cell_id year

*drop if trt_overall>10

egen max_trt_overall = max(trt_overall), by(cell_id) 
drop if max_trt_overall==0

outreg2 using "$results/summary_statistics.doc", replace sum(log)
rm "$results/summary_statistics.txt"
* export delimited "/Users/christianbaehr/Downloads/test.csv", replace

gen temp = 1
reghdfe treecover trt_overall, absorb(temp) cluster(commune_number year)
outreg2 using "$results/main_models_hansen.doc", replace tex noni nocons addtext("Year FEs", N, "Grid cell FEs", N)

reghdfe treecover trt_overall, absorb(year) cluster(commune_number year)
outreg2 using "$results/main_models_hansen.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", N)

reghdfe treecover trt_overall, absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/main_models_hansen.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y)

reghdfe treecover trt_overall temperature precip, absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/main_models_hansen.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y)

reghdfe treecover trt_overall temperature precip land_concession protected_area, absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/main_models_hansen.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y)

rm "$results/main_models_hansen.txt"

***

reghdfe ndvi trt_overall, absorb(temp) cluster(commune_number year)
outreg2 using "$results/main_models_ndvi.doc", replace tex noni nocons addtext("Year FEs", N, "Grid cell FEs", N)

reghdfe ndvi trt_overall, absorb(year) cluster(commune_number year)
outreg2 using "$results/main_models_ndvi.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", N)

reghdfe ndvi trt_overall, absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/main_models_ndvi.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y)

reghdfe ndvi trt_overall temperature precip, absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/main_models_ndvi.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y)

reghdfe ndvi trt_overall temperature precip land_concession protected_area, absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/main_models_ndvi.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y)

rm "$results/main_models_ndvi.txt"

******

egen baseline_treecover = max(treecover), by(cell_id)
*drop if baseline_treecover<0.25

outreg2 if baseline_treecover>=0.25 & !missing(baseline_treecover) using "$results/summary_statistics_forested.doc", replace sum(log)

reghdfe treecover trt_overall if baseline_treecover>=0.25 & !missing(baseline_treecover), absorb(temp) cluster(commune_number year)
outreg2 using "$results/main_models_hansen_forested.doc", replace tex noni nocons addtext("Year FEs", N, "Grid cell FEs", N)

reghdfe treecover trt_overall if baseline_treecover>=0.25 & !missing(baseline_treecover), absorb(year) cluster(commune_number year)
outreg2 using "$results/main_models_hansen_forested.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", N)

reghdfe treecover trt_overall if baseline_treecover>=0.25 & !missing(baseline_treecover), absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/main_models_hansen_forested.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y)

reghdfe treecover trt_overall temperature precip if baseline_treecover>=0.25 & !missing(baseline_treecover), absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/main_models_hansen_forested.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y)

reghdfe treecover trt_overall temperature precip land_concession protected_area if baseline_treecover>=0.25 & !missing(baseline_treecover), absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/main_models_hansen_forested.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y)

rm "$results/main_models_hansen_forested.txt"

***

reghdfe ndvi trt_overall if baseline_treecover>=0.25 & !missing(baseline_treecover), absorb(temp) cluster(commune_number year)
outreg2 using "$results/main_models_ndvi_forested.doc", replace tex noni nocons addtext("Year FEs", N, "Grid cell FEs", N)

reghdfe ndvi trt_overall if baseline_treecover>=0.25 & !missing(baseline_treecover), absorb(year) cluster(commune_number year)
outreg2 using "$results/main_models_ndvi_forested.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", N)

reghdfe ndvi trt_overall if baseline_treecover>=0.25 & !missing(baseline_treecover), absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/main_models_ndvi_forested.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y)

reghdfe ndvi trt_overall temperature precip if baseline_treecover>=0.25 & !missing(baseline_treecover), absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/main_models_ndvi_forested.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y)

reghdfe ndvi trt_overall temperature precip land_concession protected_area if baseline_treecover>=0.25 & !missing(baseline_treecover), absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/main_models_ndvi_forested.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y)

rm "$results/main_models_ndvi_forested.txt"







*********

reghdfe treecover trt_overall temperature precip if max_trt_overall<10, absorb(year cell_id) cluster(commune_number year)

*bysort cell_id (year) : gen baseline_treecover = treecover[2]
*reghdfe treecover c.trt_overall##c.baseline_treecover, absorb(year cell_id) cluster(commune_number year)

reghdfe treecover c.trt_overall##c.distance_to_city, absorb(year cell_id) cluster(commune_number year)

***

reghdfe treecover trt_rural_transport, absorb(temp) cluster(commune_number year)
outreg2 using "$results/main_models_hansen_ruraltrans.doc", replace tex noni nocons addtext("Year FEs", N, "Grid cell FEs", N, "Climate Controls", N)

reghdfe treecover trt_rural_transport, absorb(year) cluster(commune_number year)
outreg2 using "$results/main_models_hansen_ruraltrans.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", N, "Climate Controls", N)

reghdfe treecover trt_rural_transport, absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/main_models_hansen_ruraltrans.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", N)

reghdfe treecover trt_rural_transport temperature precip, absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/main_models_hansen_ruraltrans.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

reghdfe treecover trt_rural_transport temperature precip land_concession protected_area, absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/main_models_hansen_ruraltrans.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

rm "$results/main_models_hansen_ruraltrans.txt"

***

reghdfe treecover trt1km temperature precip, absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/distance_models_hansen.doc", replace tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

reghdfe treecover trt2km temperature precip, absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/distance_models_hansen.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

reghdfe treecover trt3km temperature precip, absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/distance_models_hansen.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

reghdfe treecover trt4km temperature precip, absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/distance_models_hansen.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

reghdfe treecover trt5km temperature precip, absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/distance_models_hansen.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

rm "$results/distance_models_hansen.txt"


***

reghdfe treecover trt_rural_transport temperature precip, absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/projecttype_models_hansen.doc", replace tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

reghdfe treecover trt_irrigation temperature precip, absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/projecttype_models_hansen.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

reghdfe treecover trt_rural_domestic_water_supply temperature precip, absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/projecttype_models_hansen.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", N)

reghdfe treecover trt_urban_transport temperature precip, absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/projecttype_models_hansen.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

reghdfe treecover trt_education temperature precip, absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/projecttype_models_hansen.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

reghdfe treecover trt_other temperature precip, absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/projecttype_models_hansen.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

rm "$results/projecttype_models_hansen.txt"

reghdfe treecover trt_rural_transport trt_irrigation trt_rural_domestic_water_supply trt_urban_transport trt_education trt_other temperature precip, absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/projecttype_models_hansen.doc", replace tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
rm "$results/projecttype_models_hansen.txt"



***


gen temp = 1
reghdfe loss trt_overall, absorb(temp) cluster(commune_number year)
outreg2 using "$results/loss_models_hansen.doc", replace tex noni nocons addtext("Year FEs", N, "Grid cell FEs", N, "Climate Controls", N)

reghdfe loss trt_overall, absorb(year) cluster(commune_number year)
outreg2 using "$results/loss_models_hansen.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", N, "Climate Controls", N)

reghdfe loss trt_overall, absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/loss_models_hansen.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", N)

reghdfe loss trt_overall temperature precip, absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/loss_models_hansen.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

reghdfe loss trt_overall temperature precip land_concession protected_area, absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/loss_models_hansen.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

rm "$results/loss_models_hansen.txt"

***

bys cell_id (year): gen trt_overall_lag_1yr = trt_overall[_n-1]
bys cell_id (year): gen trt_overall_lag_2yr = trt_overall[_n-2]

reghdfe trt_overall trt_overall_lag_1yr trt_overall_lag_2yr, absorb(cell_id year) cluster(commune_number year)

***

gen trt_dummy = (trt_overall>0)

gen temp = 1
reghdfe treecover trt_dummy, absorb(temp) cluster(commune_number year)
outreg2 using "$results/dummy_models_hansen.doc", replace tex noni nocons addtext("Year FEs", N, "Grid cell FEs", N, "Climate Controls", N)

reghdfe treecover trt_dummy, absorb(year) cluster(commune_number year)
outreg2 using "$results/dummy_models_hansen.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", N, "Climate Controls", N)

reghdfe treecover trt_dummy, absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/dummy_models_hansen.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", N)

reghdfe treecover trt_dummy temperature precip, absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/dummy_models_hansen.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

reghdfe treecover trt_dummy temperature precip land_concession protected_area, absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/dummy_models_hansen.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

rm "$results/dummy_models_hansen.txt"

***

gen trt1_5 = (trt_overall >= 1)
gen trt6_12 = (trt_overall >= 6)
gen trt13_29 = (trt_overall >= 13)
gen trt30_ = (trt_overall >= 30)


reghdfe treecover trt1_5 trt6_12 trt13_29 trt30_ temperature precip, cluster(commune_number year) absorb(cell_id year)
outreg2 using "$results/main_models_splittrt.doc", replace tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

rm "$results/main_models_splittrt.txt"



***

*egen max_trt_roadsonly = max(trt_roadsonly), by(cell_id) 
*drop if max_trt_roadsonly==0

reghdfe treecover trt_roadsonly temperature precip, absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/roadsonly_models.doc", replace tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
reghdfe treecover trt_roadsonly1km trt_roadsonly2km trt_roadsonly3km trt_roadsonly4km trt_roadsonly5km temperature precip, absorb(year cell_id) cluster(commune_number year)
outreg2 using "$results/roadsonly_models.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

*sample 0.01
*export delimited "/Users/christianbaehr/Downloads/test.csv", replace

********************************************************************************

*** COMMUNE-LEVEL ANALYSIS ***


*global data "/sciclone/home20/cbaehr/cambodia/eba/inputData"
*global data "/Users/christianbaehr/Downloads"
global data "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"

*global results "/sciclone/home20/cbaehr/cambodia/eba/results"
*global results "/Users/christianbaehr/Downloads"
global results "/Users/christianbaehr/Box Sync/cambodia/eba/results"


use "$data/panel_formatted_hansen_commune.dta", clear

reghdfe treecover trt_overall if year>=2009, absorb(year cell_id) cluster(commune_number year)
reghdfe treecover trt_overall if year<2009, absorb(year cell_id) cluster(commune_number year)


reghdfe treecover trt_overall, absorb(year commune_number) cluster(province_number year)
reghdfe treecover trt_overall if year>=2009, absorb(year commune_number) cluster(province_number year)
reghdfe treecover trt_overall if year<2009, absorb(year commune_number) cluster(province_number year)

reghdfe treecover trt_overall, absorb(year commune_number) cluster(province_number year)
reghdfe treecover trt_overall if province_name=="KaÃ´h Kong", absorb(year commune_number) cluster(year commune_number)






































