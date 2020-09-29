
* global data "/sciclone/home20/cbaehr/cambodia/eba/inputData"
global input "/sciclone/scr20/cbaehr"

*global data "/Users/christianbaehr/Downloads"

global results "/sciclone/home20/cbaehr/cambodia/eba/new_results"
*global results "/Users/christianbaehr/Downloads"

**********

use "$input/panel_corrected_formatted.dta", clear

replace ndvi = . if ndvi==0

egen max_trt_overall = max(trt_overall), by(cell_id)
drop if max_trt_overall==0
drop max_trt_overall

bysort cell_id (year): gen baseline_ndvi = ndvi[4]

outreg2 using "$results/summary_statistics.doc", replace sum(log)
rm "$results/summary_statistics.txt"

*model5
*reghdfe ndvi trt_overall temperature precip c.trt_overall#c.(plantation concession protected_area), absorb(year cell_id) cluster(commune_number year) pool(10)
*outreg2 using "$results/main_models_goodgovernance.doc", replace tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
*model6
reghdfe ndvi trt_overall temperature precip c.trt_overall#c.(protected_area dist_to_road), absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_goodgovernance.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
*model8
reghdfe ndvi trt_overall temperature precip c.trt_overall#c.(plantation concession protected_area baseline_ndvi), absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_goodgovernance.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)
*model9
reghdfe ndvi trt_overall temperature precip c.trt_overall#c.(plantation concession protected_area dist_to_road baseline_ndvi), absorb(year cell_id) cluster(commune_number year) pool(10)
outreg2 using "$results/main_models_goodgovernance.doc", append tex noni nocons addtext("Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

rm "$results/main_models_goodgovernance.txt"
