
global data "/sciclone/home20/cbaehr/cambodia/eba/inputData"
*global data "/Users/christianbaehr/Downloads"

global results "/sciclone/home20/cbaehr/cambodia/eba/results"
*global results "/Users/christianbaehr/Downloads"


use "$data/panel_formatted.dta", clear

gen temp = 1
reghdfe ndvi trt_overall, absorb(temp) cluster(commune_number year)
outreg2 using "$results/main_models.doc", replace tex noni nocons addtext("Year FEs", N, "Grid cell FEs", N, "Climate Controls", N)

reghdfe ndvi trt_overall, absorb(year) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", N, "Climate Controls", N)

reghdfe ndvi trt_overall, absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", N)

reghdfe ndvi trt_overall temperature precip, absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

rm "$results/main_models.txt"


