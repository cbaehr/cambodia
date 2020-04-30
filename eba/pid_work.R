
## Cambodia EBA Paper ##
## Scraping and merging PID treatment data ##

path <- "/Users/christianbaehr/Box Sync/cambodia/eba/inputData/pid"

library(RCurl)
library(readxl)
library(rvest)
library(sp)


######### PID 2003-08 ######### 

## all files for 2003-08 were provided by the Cambodian government to AidData. This first step involves
## merging multiple datasets containing the 2003-08 data

project <- read_excel(paste0(path, "/pid2003-08/Project.xlsx"))

project_output <- read_excel(paste0(path, "/pid2003-08/ProjectOutput.xlsx"))

a <- merge(project, project_output, by="ProjectID")

proj_type_outputs <- read_excel(paste0(path, "/pid2003-08/ProjTypeOutputs.xlsx"))

a$merge_id <- paste0(a$ProjTypeID, "_", a$OutputID)
proj_type_outputs$merge_id <- paste0(proj_type_outputs$TypeID, "_", proj_type_outputs$OutputID)

b <- merge(a, proj_type_outputs, by="merge_id")
#View(a[!a$merge_id %in% proj_type_outputs$merge_id, ])

proj_type <- read_excel(paste0(path, "/pid2003-08/ProjType.xlsx"))

c <- merge(b, proj_type, by.x="TypeID", by.y="ProjTypeID")

category_index <- read_excel(paste0(path, "/pid2003-08/CategoryIndex.xlsx"))

c$merge_id <- paste0(c$TypeID, "_", c$OutputID.x)
category_index$merge_id <- paste0(category_index$TypeID, "_", category_index$OutputID)

d <- merge(c, category_index, by="merge_id")

table3 <- read_excel(paste0(path, "/pid2003-08/Table3.xlsx"))

d$merge_id <- paste0(d$OutputID, "_", d$CategoryID)
table3$merge_id <- paste0(table3$OutputID, "_", table3$CategoryID)

e <- merge(d, table3, by="merge_id")

output_categories <- read_excel(paste0(path, "/pid2003-08/OutputCategories.xlsx"))

projects <- merge(e, output_categories, by.x="CategoryID.y", by.y="ID")

###

contract <- read_excel(paste0(path, "/pid2003-08/Contract.xlsx"))
length(unique(contract$ContractID))

contract_abandon <- read_excel(paste0(path, "/pid2003-08/tblContract_Abandon.xlsx"))

f <- merge(contract, contract_abandon, by="ContractID", all.x=T)
f <- f[is.na(f$FY), ]

amendment <- read_excel(paste0(path, "/pid2003-08/Amendment.xlsx"))

g <- merge(f, amendment, by="ContractID", all.x=T)
g$StartDate <- as.character(g$StartDate)
g$EndDate <- as.character(g$EndDate)
g$New_Start_Date <- as.character(g$New_Start_Date)
g$New_End_Date <- as.character(g$New_End_Date)

g$EndDate <- ifelse(is.na(g$New_End_Date), g$EndDate, g$New_End_Date)
g$StartDate <- ifelse(is.na(g$New_Start_Date), g$StartDate, g$New_Start_Date)
g <- g[, !names(g) %in% c("New_End_Date", "New_Start_Date")]


progress <- read_excel(paste0(path, "/pid2003-08/Progress.xlsx"))
progress <- aggregate(Progress ~ ContractID, max, data = progress)

h <- merge(g, progress, by="ContractID")
h <- h[h$Progress==100, ]

h$Amendment_Date <- as.Date(h$Amendment_Date, format="%Y-%m-%d")

k <- h[is.na(h$Amendment_Date), ]

l <- merge(aggregate(Amendment_Date ~ ContractID, max, data = h), h)
l <- l[, names(h)]

m <- rbind(k, l)

m <- m[!duplicated(m$ContractID), ]

contract_output <- read_excel(paste0(path, "/pid2003-08/ContractOutput.xlsx"))

contracts <- merge(f, contract_output, by="ContractID")

###

projects$merge_id <- paste0(projects$ProjectID, "_", projects$OrderNo)
contracts$merge_id <- paste0(contracts$linkProjectID, "_", contracts$linkOrderNo)
#View(contracts[contracts$merge_id %in% contracts$merge_id[duplicated(contracts$merge_id)],])

n <- merge(projects, contracts, by="merge_id")

village <- read_excel(paste0(path, "/pid2003-08/Village.xlsx"))
p <- merge(n, village, by="VillGis")
#sum(n$VillGis %in% village$VillGis)

q <- p[, c("ProjectID",
           "NameE.x",
           "OrderNo.x",
           "VillGis",
           "OutputID.x",
           "Qty.x",
           "NameE.y",
           "Name",
           "CategoryE",
           "UnitE",
           "ContractID",
           "StartDate",
           "EndDate",
           "X",
           "Y")]

#View(a[a$Qty.x==1400,])
#summary(a$FundCS)
## seems likely this is incorrect data
q <- q[which(q$Qty.x!=1400), ]
#View(roads[roads$Qty.x==42, ])
q <- q[which(q$Qty.x!=42), ]
#summary(roads$Qty.x)

#View(c[duplicated(c),])
q <- q[!duplicated(q), ]
q <- q[which(q$ProjectID!=4171301), ]
q <- q[which(q$ProjectID!=2171301), ]

q <- q[!is.na(q$X), ]
#sum(is.na(c$X))
#sum(is.na(c$Y))

pid2008 <- q

rm(list = setdiff(ls(), c("contract", "path", "pid2008")))

######### PID 2009-18 ######### 

## scraping project, contract, and implementation details for PID projects from 2009-2018

# province <- c("Banteay Meanchey", "Battambang", "Kampong Cham", "Kampong Chhnang", "Kampong Speu", "Kampong Thom", "Kampot", "Kandal", "Koh Kong", "Kratie", "Mondul Kiri", "Phnom Penh", "Preah Vihear", "Prey Veng", "Pursat", "Ratanak Kiri", "Siemreap", "Preah Sihanouk", "Stung Treng", "Svay Rieng", "Takeo", "Odday Meanchey", "Kep", "Pailin", "Tboung Khmum")

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
#write.csv(dat, "/Users/christianbaehr/Downloads/pid2012-18.csv", row.names = F)
#write.csv(dat, paste0(path, "/pid2009-18/pid2009-18_contractsummary.csv"), row.names = F)


# for(i in province) {
#   for(j in 2009:2018) {
#     link <- paste0("http://db.ncdd.gov.kh/pid/reports/monitoring/Implementation.castle?detail=1&pv=", which(province==i), "&year=", j)
#     if(url.exists(link)) {
#       tab <- read_html(link) %>%
#         html_nodes(., xpath = '//*[@id="tblRpt"]') %>%
#         html_table(., fill=T) %>%
#         .[[1]]
#       tab2 <- tab[-1, ]
#       names(tab2) <- tab[1, ]
#       if(nrow(tab2)!=0) {
#         tab2$province <- i
#         tab2$year <- j
#         if(!exists("dat")) {
#           dat <- tab2
#         } else {
#           dat <- rbind(dat, tab2)
#         }
#       }
#     }
#   }
# }
#write.csv(dat, paste0(path, "/pid2009-18/pid2009-18_implementation.csv"), row.names = F)


# commune <- paste0(path, "/pid2009-18/GISCommune.xlsx") %>%
#   read_excel() %>%
#   as.character(.$Id)
# 
# for(i in commune) {
#   x <- paste0("http://db.ncdd.gov.kh/pid/project/home/commune.castle?areaCode=", i)
#   if(url.exists(x)) {
#     b <- read_html(x)
#     b <- as.character(b)
#     c <- gregexpr('(?<=/pid/project/home/view\\.castle\\?pid\\=).*(?=c\\\\)', b, perl = T)
#     c <- unlist(regmatches(b, gregexpr('(?<=pid\\=).*(?=\")', b, perl = T) ))
#     d <- gsub('%5C%22\" target=\'\\\"_blank\\', "", c, fixed=T)
#     if(!exists("urls")) {
#       urls <- d
#     } else{
#       urls <- append(urls, d)
#     }
#   }
# }

# urls2 <- paste0("http://db.ncdd.gov.kh/pid/project/home/view.castle?pid=", urls)
# urls2 <- data.frame(urls2)
# write.csv(urls2, paste0(path, "/pid2009-18/pid2009-18_urls.csv"), row.names = F)


# urls <- read.csv(paste0(path, "/pid2009-18/pid2009-18_urls.csv"), stringsAsFactors = F)
# 
# urls <- as.character(urls$urls)
# tracker <- 0
# 
# for(i in 1:length(urls)) {
#   j <- urls[i]
#   x <- paste0("http://db.ncdd.gov.kh/pid/project/home/view.castle?pid=", j)
#   y <- try(url.exists(x))
#   m <- 0
#   while(class(y)=="try-error" & m<=10) {
#     y <- try(url.exists(x))
#     m <- m+1
#   }
#   if(y==T) {
#     page <- try(read_html(x))
#     n <- 0
#     while(class(page)=="try-error" & n<=10) {
#       page <- try(read_html(x))
#       n <- n+1
#     }
#     if(class(page)!="try-error") {
#       proj_summary <- html_nodes(page, xpath = '//*[@id="dsummary"]') %>%
#         html_text()
#       proj_table <- html_nodes(page, xpath='//*[@id="doutputlist"]/table') %>%
#         html_table(fill=T) %>%
#         data.frame()
#       proj_summary <- gsub("\r|\n|\t", "", proj_summary)
#       loc <- unlist(regmatches(proj_summary, gregexpr("(?<=Location).*(?=Sector)", gsub("Sub-Sector", "", proj_summary), perl = TRUE ) ))
#       type <- unlist(regmatches(proj_summary, gregexpr("(?<=Sub-Sector).*(?=Technical Assistant)", proj_summary, perl = TRUE ) ))
#       description <- unlist(regmatches(proj_summary, gregexpr("(?<=Name).*(?=Objective)", proj_summary, perl = TRUE ) ))
#       contractID <- ifelse(grepl("Related contract", proj_summary, fixed=T),
#                            unlist(regmatches(proj_summary, gregexpr("(?<=Related contract\\(s\\)).*(?=Created By)", proj_summary, perl = TRUE ) )), NA)
#       proj_table$loc <- loc
#       proj_table$type <- type
#       proj_table$desc <- description
#       proj_table$contractID <- contractID
#       proj_table$projectID <- i
#       if(!exists("dat")) {
#         dat <- proj_table
#       } else{
#         if(ncol(proj_table)==ncol(dat)) {
#           dat <- rbind(dat, proj_table)
#         }
#       }
#     }
#   } else {
#     tracker <- tracker +1
#   }
#   if(i%%100==0) {cat(i, "of ", length(urls), "\n")}
# }
# write.csv(dat, paste0(path, "/pid2009-18/pid2009-18_project.csv"), row.names = F)

###

## merging scraped data for 2009-18


dat <- read.csv(paste0(path, "/pid2009-18/pid2009-18_contractsummary.csv"), stringsAsFactors = F)

district <- dat$Commune[dat$Commune==dat$Village]

loc <- data.frame(id1=which(dat$Commune==dat$Village), 
                  id2=c(which(dat$Commune==dat$Village)[-1]-1, nrow(dat)))
loc2 <- apply(loc, 1, function(x) {x[1]:x[2]})

dat[, "district"] <- ""
for(i in 1:length(loc2)) {dat[loc2[[i]], "district"] <- district[i]}

dat <- dat[dat$Commune!=dat$Village, ]

commune <- dat[dat$Commune!="", c("Commune", "Village", "Outputs")]

loc <- data.frame(id1=which(dat$Commune!="")+1, 
                  id2=c(which(dat$Commune!="")[-1]-1, nrow(dat)))

loc2 <- apply(loc, 1, function(x) {x[1]:x[2]})

dat[, c("commune", "contract", "output")] <- ""
for(i in 1:length(loc2)) {dat[loc2[[i]], c("commune", "contract", "output")] <- commune[i, ]}

dat <- dat[dat$Commune=="", ]

dat <- dat[, c("Village", "commune", "district", "province_name", "contract", "year", "Outputs", "output", "Quantity")]

names(dat) <- c("village_name", 
                "commune_name", 
                "district_name", 
                "province_name", 
                "contract_id", 
                "year", 
                "activity_description", 
                "output", 
                "quantity")

contract <- dat

rm(list = setdiff(ls(), c("contract", "path", "pid2008")))

implementation <- read.csv(paste0(path, "/pid2009-18/pid2009-18_implementation.csv"), stringsAsFactors = F)

implementation <- implementation[implementation$Area.Name!="", ]

a <- merge(contract, implementation, by.x = "contract_id", by.y = "Village")
contract <- a[a$Status=="100 %", ]

#View(contract[contract$contract_id == contract$contract_id[duplicated(contract$contract_id)][2], ])

#View(project[which(project$contractID==contract$contract_id[duplicated(contract$contract_id)][2]), ])

project <- read.csv(paste0(path, "/pid2009-18/pid2009-18_project.csv"), stringsAsFactors = F)

project <- project[project$Nr.!="Estimated cost", !names(project) %in% c("Unit.Cost", "Total", "Operations")]

project$contractID <- trimws(project$contractID)

project$merge_id <- paste(project$contractID, project$Village, project$Qty)
contract$merge_id <- paste(contract$contract_id, contract$village_name, contract$quantity)
b <- merge(project, contract, by="merge_id")

b$End.Actual..Delay. <- as.Date(b$End.Actual..Delay., format = "%d-%b-%Y")

b <- b[!is.na(b$End.Actual..Delay.), ]

###############################################################

villgis <- unlist(regmatches(b$Description.x, gregexpr('\\[(.*)\\]', b$Description.x, perl=T)))
villgis <- unlist(gsub("\\[ | \\]", "", villgis))

b$VillGis <- villgis

fun1 <- function(x) {
  y <- strsplit(x, "\\[|;")[[1]][3]
  z <- strsplit(trimws(y), " ")[[1]][1]
  return(z)
}

b$qty <- sapply(b$activity_description, fun1) %>%
  gsub(",", "", .) %>%
  as.numeric(.)

fun2 <- function(x) {
  a <- strsplit(x, "New|Upgrade|Repair")[[1]][1]
  b <- trimws(a)
  return(b)
}

b$type2 <- sapply(b$Description.x, fun2)

fun3 <- function(x) {
  c <- strsplit(x, " ")[[1]]
  d <- as.numeric(c)
  e <- c[is.na(d)]
  return(e)
}

b$unit <- sapply(b$Qty, fun3)

fun4 <- function(x) {
  f <- as.numeric(strsplit(x, " ")[[1]])
  g <- f[!is.na(f)]
  return(g)
}

b$new_quantity <- sapply(b$Qty, fun4)

village <- read_excel(paste0(path, "/pid2003-08/Village.xlsx"))

b$village <- as.numeric(b$VillGis)
sum(b$village %in% village$VillGis)
sum(tolower(b$Village) %in% tolower(village$NameE))

fun5 <- function(x) {
  h <- strsplit(x, "/")[[1]][1]
  return(h)
}

b$commune_id <- sapply(b$contract_id, fun5)
b$commune_id <- as.numeric(b$commune_id)

#b$merge_id <- tolower(b$Village)
village$merge_id <- paste(tolower(village$NameE), village$CommGis)
village <- village[!village$merge_id %in% village$merge_id[duplicated(village$merge_id)], ]

b$merge_id <- paste(tolower(b$Village), b$commune_id)

c <- merge(b, village, by="merge_id")


d <- c[, c("projectID",
           "activity_description",
           "Nr.",
           "VillGis.y",
           "new_quantity",
           "type",
           "type2",
           "Description.x",
           "unit", 
           "contract_id",
           "Start.Actual..Delay.",
           "End.Actual..Delay.",
           "X",
           "Y")]

#write.csv(d, "/Users/christianbaehr/Downloads/pid2009-16.csv", row.names = F)
#write.csv(d, paste0(path, "/Users/christianbaehr/Downloads/pid2009-16.csv"), row.names = F)


# e <- read.csv("/Users/christianbaehr/Downloads/pid2008.csv", stringsAsFactors = F)
e <- pid2008

names(d) <- c("project_id",
              "activity_desc",
              "order_nr",
              "village_id",
              "quantity",
              "activity_type",
              "activity_desc_long",
              "activity_desc_long2",
              "unit",
              "contract_id",
              "start_date",
              "end_date",
              "lon",
              "lat")

names(e) <- c("project_id",
              "activity_desc",
              "order_nr",
              "village_id",
              "OutputID.x",
              "quantity",
              "activity_type",
              "activity_desc_long",
              "activity_desc_long2",
              "unit",
              "contract_id",
              "start_date",
              "end_date",
              "lon",
              "lat")


f <- rbind(d, e[, names(e)!="OutputID.x"])
f <- f[!is.na(f$lon),]

g <- SpatialPoints(coords = f[, c("lon", "lat")], proj4string = CRS("+init=epsg:32648"))

h <- SpatialPointsDataFrame(coords = g, data = f)

geo_proj <- "+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0,0,0"
k <- spTransform(h, geo_proj)

f$lon <- k@coords[,1]
f$lat <- k@coords[,2]

#f$start_year <- format(as.Date(f$start_date, "%d-%b-%Y"), "%Y")
f$end_year <- format(f$end_date, "%Y")

#writeOGR(k, "/Users/christianbaehr/Desktop/pid_full.geojson", layer = "ProjectID", driver = "GeoJSON")
write.csv(f, file = paste0(path, "/pid2003-18.csv"), row.names = F)




























