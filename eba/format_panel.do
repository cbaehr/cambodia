
global data "/sciclone/home20/cbaehr/cambodia/eba/inputData"
*global data "/Users/christianbaehr/Downloads"

import delimited "$data/panel_new.csv", clear

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

replace protected_area = "1" if protected_area=="True"
replace protected_area = "0" if protected_area=="False"
destring protected_area, replace

replace plantation = "1" if plantation=="True"
replace plantation = "0" if plantation=="False"
destring plantation, replace

replace concession = "1" if concession=="True"
replace concession = "0" if concession=="False"
destring concession, replace

gen trt_overall = trt1km + trt2km + trt3km + trt4km + trt5km

replace distance_to_city = distance_to_city/1000
replace distance_to_road = distance_to_road/1000

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

save "$data/panel_formatted.dta", replace

su

replace treecover="." if treecover=="NA"
destring treecover, replace

su

save "$data/panel_formatted.dta", replace





