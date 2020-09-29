
*global data "/sciclone/home20/cbaehr/cambodia/eba/inputData"
global output "/sciclone/scr20/cbaehr"
*global output "/Users/christianbaehr/Downloads"

import delimited "$output/panel_corrected_cgeo_mines.csv", clear

replace precip = "." if precip=="NA"
destring precip, replace
replace precip = . if precip<0 | precip>1000

replace temperature = "." if temperature=="NA"
destring temperature, replace
replace temperature = . if temperature==0


drop province_number province_name district_number district_name commune_name longitude latitude


su


*levelsof commune_number
egen temp = group(commune_number)
tostring temp, replace
replace commune_number = temp
destring commune_number, replace
drop temp



*replace protected_area = "1" if protected_area=="True"
*replace protected_area = "0" if protected_area=="False"
*destring protected_area, replace

*replace plantation = "1" if plantation=="True"
*replace plantation = "0" if plantation=="False"
*destring plantation, replace

*replace concession = "1" if concession=="True"
*replace concession = "0" if concession=="False"
*destring concession, replace

gen trt_overall = trt1km + trt2km + trt3km + trt4km + trt5km

replace dist_to_city = dist_to_city/1000
replace dist_to_road = dist_to_road/1000
replace distance_to_minecasualty = distance_to_minecasualty/1000

replace ndvi = . if ndvi==-9999
replace ndvi = ndvi*0.0001
replace ndvi = . if ndvi<0

*replace treecover="." if treecover=="NA"
*destring treecover, replace

su

save "$output/panel_corrected_cgeo_formatted.dta", replace
