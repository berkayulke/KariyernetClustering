library(kamila)
data <- read.csv(file = "tmp.csv", header = TRUE,  sep = ",", row.names = NULL,  stringsAsFactors = TRUE) # nolint
con_ind <- c(6)
con_vars <- data[,con_ind]
con_vars <- data.frame(scale(con_vars))
cat_vars_fac <- data[,c(1,2,3,4,5)]
cat_vars_fac <- data[,c(2,3,4,5)]
cat_vars_fac[] <- lapply(cat_vars_fac, factor)
print("hi")
kamila_result <- kamila(con_vars, cat_vars_fac, numClust=10, numInit=10)
print(kamila_result)