
import delimited "/Users/christianbaehr/Downloads/pre_panel_commune.csv", clear

reshape long treatment1000_ treatment2000_ treatment3000_ treatment4000_ treatment5000_ treatment_irrigation1000_ treatment_irrigation2000_ treatment_irrigation3000_ treatment_irrigation4000_ treatment_irrigation5000_ trtroads1km_ trtroads2km_ trtroads3km_ trtroads4km_ trtroads5km_ temp_ precip_ tc ndvi, i(gid_3) j(year)

reshape long treecover ndvi trt1km trt2km trt3km trt4km trt5km temperature precip treatment_irrigation1000_ treatment_irrigation2000_ treatment_irrigation3000_ treatment_irrigation4000_ treatment_irrigation5000_ trtroads1km_ trtroads2km_ trtroads3km_ trtroads4km_ trtroads5km_, i(gid_3) j(year)


rename count count_30mcells

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

save "/Users/christianbaehr/Box Sync/cambodia/eba/inputData/grid_commune_formatted_updated.dta", replace

