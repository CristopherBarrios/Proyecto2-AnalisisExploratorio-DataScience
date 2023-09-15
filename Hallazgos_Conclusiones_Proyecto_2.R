options(scipen = 999)
library(dplyr)
library(ggplot2) 
library(readxl)
library(gmodels)
library(Hmisc)
library(ggthemes)

glimpse(newTrain)

table(newTrain$image_id)

table(newTrain$center_id)

table(newTrain$patient_id)

table(newTrain$image_num)

table(newTrain$label)

prop.table(table(newTrain$image_num))

prop.table(table(newTrain$center_id))

prop.table(table(newTrain$label))

summary(newTrain)

describe(newTrain)

hist(newTrain$image_num)

hist(newTrain$center_id)

pie(table(newTrain$center_id))

pie(table(newTrain$image_num))

pie(table(newTrain$label))