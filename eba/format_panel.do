
global data "/sciclone/home20/cbaehr/cambodia/eba/inputData"
*global data "/Users/christianbaehr/Downloads"

import delimited "$data/panel.csv", clear

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

gen trt_overall = trt_rural_transport + trt_irrigation + trt_rural_domestic_water_supply + trt_urban_transport + trt_education + trt_other

replace ndvi = . if ndvi==-9999
replace ndvi = ndvi*0.0001
replace ndvi = . if ndvi<0

replace precip = "." if precip=="NA"
destring precip, replace
replace precip = . if precip<0 | precip>1000

replace temperature = "." if temperature=="NA"
destring temperature, replace
replace temperature = . if temperature==0

export delimited "$data/panel_formatted_test.csv", replace

save "$data/panel_formatted_test.dta", replace

su















