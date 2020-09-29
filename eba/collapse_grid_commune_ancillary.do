
global data "/Users/christianbaehr/Downloads"
* global data "/sciclone/home20/cbaehr/cambodia/eba/inputData"

* import delimited "$data/pre_1km_grid.csv", clear
import delimited "$data/pre_1km_grid_ancillary.csv", clear

ds gid_3 cell_id_y, not
collapse (mean) `r(varlist)', by(gid_3)

su

export delimited "$data/grid_commune_ancillary.csv", replace

