


*global data "/sciclone/home20/cbaehr/cambodia/eba/inputData"
global data "/sciclone/scr20/cbaehr"
*global data "/Users/christianbaehr/Downloads"

import delimited "$data/panel_corrected_roads.csv", clear

gen trt_roads_overall = trt1km_roads + trt2km_roads + trt3km_roads + trt4km_roads + trt5km_roads

egen max_trt_overall = max(trt_roads_overall), by(cell_id)
drop if max_trt_overall==0
drop max_trt_overall

*levelsof province_number
egen temp = group(province_number)
tostring temp, replace
replace province_number = temp
destring province_number, replace
drop temp

*levelsof district_number
egen temp = group(district_number)
tostring temp, replace
replace district_number = temp
destring district_number, replace
drop temp

*levelsof commune_number
egen temp = group(commune_number)
tostring temp, replace
replace commune_number = temp
destring commune_number, replace
drop temp

replace dist_to_city = dist_to_city/1000
replace dist_to_road = dist_to_road/1000

replace ndvi = . if ndvi==-9999
replace ndvi = ndvi*0.0001
replace ndvi = . if ndvi<0

replace precip = "." if precip=="NA"
destring precip, replace
replace precip = . if precip<0 | precip>1000

replace temperature = "." if temperature=="NA"
destring temperature, replace
replace temperature = . if temperature==0

drop longitude latitude

save "$data/panel_corrected_roads_formatted.dta", replace
*export delimited "$data/panel_irrigation_formatted.csv", replace

su

