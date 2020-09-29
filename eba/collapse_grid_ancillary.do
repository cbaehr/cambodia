
* global data "/Users/christianbaehr/Box Sync/cambodia/eba/inputData"
* global input "/sciclone/home20/cbaehr/cambodia/eba/inputData"

global output "/sciclone/scr20/cbaehr"

import delimited "$output/pre_1km_grid_ancillary.csv", clear
* import delimited "$data/pre_1km_grid_test.csv", clear
drop gid_3

ds cell_id_x, not
collapse (mean) `r(varlist)', by(cell_id_x)

su

export delimited "$output/grid_1km_ancillary.csv", replace

********************************************************************************


* import delimited "$data/pre_1km_grid.csv", clear
import delimited "$output/pre_1km_grid_ancillary.csv", clear

ds gid_3, not
collapse (mean) `r(varlist)', by(gid_3)

su

export delimited "$output/grid_commune_ancillary.csv", replace


