
pid <- read.csv("/Users/christianbaehr/Box Sync/cambodia/eba/inputData/pid/pid2003-18_trimmed.csv",
                stringsAsFactors = F)

end_date <- as.Date(pid$end_date, format = "%Y-%m-%d")
end_date <- format(end_date, "%Y")

hist(as.numeric(end_date),
     col = "skyblue",
     xlab = "End Year",
     main = "Temporal distribution of treatment projects",
     xaxt = "none")
axis(1, seq(2003, 2019, 2))

