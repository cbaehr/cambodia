
*import delimited "/Users/christianbaehr/Downloads/pre_panel_1km.csv", clear
import delimited "/Users/christianbaehr/Downloads/pre_panel_1km_ntl.csv", clear

*drop cell_id_y

*reshape long treatment1000_ treatment2000_ treatment3000_ treatment4000_ treatment5000_ treatment_irrigation1000_ treatment_irrigation2000_ treatment_irrigation3000_ treatment_irrigation4000_ treatment_irrigation5000_ trtroads1km_ trtroads2km_ trtroads3km_ trtroads4km_ trtroads5km_ temp_ precip_ tc ndvi, i(cell_id_x) j(year)

rename ntl1992mean ntl1992
rename ntl1993mean ntl1993
rename ntl1994mean ntl1994
rename ntl1995mean ntl1995
rename ntl1996mean ntl1996
rename ntl1997mean ntl1997
rename ntl1998mean ntl1998
rename ntl1999mean ntl1999
rename ntl2000mean ntl2000
rename ntl2001mean ntl2001
rename ntl2002mean ntl2002
rename ntl2003mean ntl2003
rename ntl2004mean ntl2004
rename ntl2005mean ntl2005
rename ntl2006mean ntl2006
rename ntl2007mean ntl2007
rename ntl2008mean ntl2008
rename ntl2009mean ntl2009
rename ntl2010mean ntl2010
rename ntl2011mean ntl2011
rename ntl2012mean ntl2012
rename ntl2013mean ntl2013


*reshape long treecover ndvi trt1km trt2km trt3km trt4km trt5km temperature precip treatment_irrigation1000_ treatment_irrigation2000_ treatment_irrigation3000_ treatment_irrigation4000_ treatment_irrigation5000_ trtroads1km_ trtroads2km_ trtroads3km_ trtroads4km_ trtroads5km_, i(cell_id_x) j(year)

reshape long treecover ndvi trt1km trt2km trt3km trt4km trt5km temperature precip treatment_irrigation1000_ treatment_irrigation2000_ treatment_irrigation3000_ treatment_irrigation4000_ treatment_irrigation5000_ trtroads1km_ trtroads2km_ trtroads3km_ trtroads4km_ trtroads5km_ ntl infant_mort, i(cell_id_x) j(year)

*bys year: su trt1km

*reshape long trt1km trt2km trt3km trt4km trt5km  temperature precip treecover ndvi, i(cell_id_x) j(year)

*rename count count_30mcells
*rename treatment1000_ trt1km
*rename treatment2000_ trt2km
*rename treatment3000_ trt3km
*rename treatment4000_ trt4km
*rename treatment5000_ trt5km

*rename tc treecover
*rename gpw_density_2000 popdensity2000

rename treatment_irrigation1000_ trt1km_irrigation
rename treatment_irrigation2000_ trt2km_irrigation
rename treatment_irrigation3000_ trt3km_irrigation
rename treatment_irrigation4000_ trt4km_irrigation
rename treatment_irrigation5000_ trt5km_irrigation

rename trtroads1km_ trt1km_roads
rename trtroads2km_ trt2km_roads
rename trtroads3km_ trt3km_roads
rename trtroads4km_ trt4km_roads
rename trtroads5km_ trt5km_roads

rename gid_1 province_number
rename name_1 province_name
rename gid_2 district_number
rename name_2 district_name
rename gid_3 commune_number
rename name_3 commune_name
*rename temp_ temperature
*rename precip_ precipitation

*drop cell_id

egen province_num = group(province_number)
egen commune_num = group(commune_number)

egen trt_overall = rowtotal(trt1km trt2km trt3km trt4km trt5km)
egen trt_overall_roads = rowtotal(trt?km_roads)
egen trt_overall_irrigation = rowtotal(trt?km_irrigation)
forv i = 1/5 {
	gen trt`i'km_else = trt`i'km - (trt`i'km_roads + trt`i'km_irrigation)
}
egen trt_overall_else = rowtotal(trt?km_else)


keep cell_id_x year infant_mort ntl



save "${data}/development_outcomes.dta", replace


*export delimited "/Users/christianbaehr/Downloads/test.csv", replace

end

*************************************************

use "/Users/christianbaehr/Box Sync/cambodia/eba/inputData/grid_1km_formatted_updated_ntl.dta", clear





su
*drop if year!=2010
*export delimited "/Users/christianbaehr/Documents/test.csv", replace

reghdfe ntl trt_overall_roads trt_overall_irrigation trt_overall_else [aw=count], absorb(cell_id_x year) cluster(commune_num year)
outreg2 using "/Users/christianbaehr/Downloads/Ntl_results.doc", replace tex noni nocons ctitle(ntl) addtext("Sample", Full, "Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)

reghdfe infant_mort trt_overall_roads trt_overall_irrigation trt_overall_else [aw=count], absorb(cell_id_x year) cluster(commune_num year)
outreg2 using "/Users/christianbaehr/Downloads/Ntl_results.doc", append tex noni nocons ctitle(mort) addtext("Sample", Full, "Year FEs", Y, "Grid cell FEs", Y, "Climate Controls", Y)






