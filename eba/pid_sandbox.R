
pid <- read.csv("/Users/christianbaehr/Box Sync/cambodia/eba/inputData/pid/pid2003-18_trimmed.csv",
                stringsAsFactors = F)

names(pid)

summary(pid$quantity)
unique(pid$activity_type)

rural_transport <- pid[which(pid$activity_type=="Rural Transport"), ]

unique(rural_transport$activity_desc)
unique(rural_transport$unit)

rural_transport <- rural_transport[!grepl("routine maintenance", tolower(rural_transport$activity_desc_long)), ]

unique(rural_transport$activity_desc_long)

activities <- c("wood bridge",
                "earth road",
                "sand road",
                "laterite road",
                "concrete bridge",
                "gravel road",
                "concrete road",
                "stone road",
                "earth dam",
                "wood bridge",
                "bailey bridge",
                "bitumen road")

activities <- paste(activities, collapse = "|")

rural_transport <- rural_transport[grepl(activities, tolower(rural_transport$activity_desc_long)), ]
rural_transport <- rural_transport[!grepl("repeated service", tolower(rural_transport$activity_desc_long)), ]


unique(rural_transport$activity_desc_long)
unique(rural_transport$unit)

place <- rural_transport[which(rural_transport$unit=="Place"), ]
unique(place$activity_desc_long)

km <- rural_transport[which(rural_transport$unit=="km"), ]
unique(km$activity_desc_long)
summary(km$quantity)

bridges <- rural_transport[which(rural_transport$unit=="Bridges"), ]
unique(bridges$activity_desc_long)

write.csv(km, "/Users/christianbaehr/Box Sync/cambodia/eba/inputData/pid/pid_roadsonly.csv", row.names = F)

#########


pid_slim <- data.frame(village_id=unique(pid$village_id))
pid_slim["time_to_2ndproject"] <- NA
pid_slim["time_to_3rdproject"] <- NA
pid_slim["time_to_4thproject"] <- NA

for(i in 1:nrow(pid_slim)) {
  
  temp <- pid[pid$village_id==pid_slim$village_id[i],]
  end_dates <- sort(temp$end_date[which(!is.na(temp$end_date))])
  if(length(end_dates)>1) {
    end_dates <- as.Date(end_dates)
    pid_slim$time_to_2ndproject[i] <- end_dates[2] - end_dates[1]
    if(length(end_dates)>2) {
      pid_slim$time_to_3rdproject[i] <- end_dates[3] - end_dates[2]
    }
      if(length(end_dates)>3) {
        pid_slim$time_to_4thproject[i] <- end_dates[4] - end_dates[3]
      }
  }
  
}

hist(pid_slim$time_to_2ndproject)
hist(pid_slim$time_to_3rdproject)
hist(pid_slim$time_to_4thproject)

summary(pid_slim$time_to_2ndproject)
summary(pid_slim$time_to_3rdproject)
summary(pid_slim$time_to_4thproject)












