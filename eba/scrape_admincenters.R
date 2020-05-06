
library(rvest)

tab <- read_html("https://www.citypopulation.de/en/cambodia/cities/")

provinces <- html_nodes(tab, xpath = '//*[@id="tl"]') %>%
  html_table(.)
provinces <- provinces[[1]]

cities <- html_nodes(tab, xpath = '//*[@id="ts"]') %>%
  html_table(.)
cities <- cities[[1]]

'//*[@id="tl"]'
'//*[@id="ts"]'




# for(i in province) {
#   for(j in 2009:2018) {
#     link <- paste0("http://db.ncdd.gov.kh/pid/reports/monitoring/contractsummary.castle?pv=", which(province==i), "&year=", j)
#     if(url.exists(link)) {
#       tab <- read_html(link) %>%
#         html_nodes(., xpath = '//*[@id="tblRpt"]') %>%
#         html_table(.) %>%
#         .[[1]]
#       if(nrow(tab)>0) {
#         tab$province_name <- i
#         tab$year <- j
#         if(!exists("dat")) {
#           dat <- tab
#         } else {
#           dat <- rbind(dat, tab)
#         }
#       }
#     }
#   }
# }