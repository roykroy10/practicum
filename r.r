rm(list=ls())
setwd("C:/Users/Roy/Documents/IDC/practicum")

train <- read.csv("train.csv",header = T)
test <- read.csv("test.csv",header = T)

dim(train)
names(train)
str(train)
summary(train$LotArea)
summary(train$Neighborhood)
summary(train$SalePrice)
table(train$Neighborhood)

prop.table(table(train$Neighborhood))

nei <- data.frame(table(train$Neighborhood))
colnames(nei) <- c("Neighborhood", "count")
nei$percent <- round((nei$count/sum(nei$count))*100, digits=2)

avg_sale_price <- tapply(train$SalePrice, train$Neighborhood, mean)
avg_sale_price <- data.frame(avg_sale_price)
nei <- cbind(nei, avg_sale_price)

median_sale_price <- tapply(train$SalePrice, train$Neighborhood, median)
median_sale_price <- data.frame(median_sale_price)
nei <- cbind(nei, median_sale_price)

avg_lotarea <- tapply(train$LotArea, train$Neighborhood, mean)
avg_lotarea <- data.frame(avg_lotarea)
nei <- cbind(nei, avg_lotarea)

median_lotarea <- tapply(train$LotArea, train$Neighborhood, median)
median_lotarea <- data.frame(median_lotarea)
nei <- cbind(nei, median_lotarea)

avg_yearbuilt <- tapply(train$YearBuilt, train$Neighborhood, mean)
avg_yearbuilt <- data.frame(avg_yearbuilt)
nei <- cbind(nei, avg_yearbuilt)

median_yearbuilt <- tapply(train$YearBuilt, train$Neighborhood, median)
median_yearbuilt <- data.frame(median_yearbuilt)
nei <- cbind(nei, median_yearbuilt)

train$pricepersqft <- train$SalePrice / train$LotArea
train$avglivingprice <- train$SalePrice / train$GrLivArea
mean_pricepersqft <- tapply(train$pricepersqft, train$Neighborhood, mean)
mean_pricepersqft <- data.frame(mean_pricepersqft)
nei <- cbind(nei, mean_pricepersqft)
?plot
library(ggplot2)


ggplot(subset(train), 
       aes(SalePrice, color = Neighborhood)) +
  stat_density(geom="line") +
  facet_wrap(~Neighborhood, scales = "free",ncol = 5)

nei <- nei[nei$count>50,]
ggplot(subset(train), 
       aes(SalePrice, color = Neighborhood)) +
  stat_density(geom="line") +
  facet_wrap(~Neighborhood, scales = "free",ncol = 5)

nei_filtered <- merge(train,nei) # leaves only relevant neighborhoods


ggplot(data=nei_filtered)+aes(x=Neighborhood,y=pricepersqft)+
  geom_point(color="darkblue",alpha=0.6,position='jitter')+
  labs(title="ground living area against sale price",x="ground living area",y="Sale price")

ggplot(nei_filtered, aes(x=GrLivArea, y=SalePrice,colour=Neighborhood))+
  geom_point(position='jitter') + stat_smooth(method=lm)

ggplot(nei_filtered, aes(x=Neighborhood, y=pricepersqft,size=LotArea))+
  geom_point(position='jitter', color='darkblue', fill='cornsilk', shape=21) + geom_boxplot(aes( x=Neighborhood,y=mean_pricepersqft))+ scale_size_area(max_size=15)

ggplot(nei_filtered, aes(x=Neighborhood, y=pricepersqft,size=GrLivArea))+
  geom_point(position='jitter', color='darkblue', fill='cornsilk', shape=21) + geom_boxplot(aes( x=Neighborhood,y=mean_pricepersqft))+ scale_size_area(max_size=15)

View(nei_filtered[nei_filtered$Neighborhood=="Edwards" & nei_filtered$pricepersqft<nei_filtered$mean_pricepersqft,])

library(glmnet)

grliv_saleprice_reg <- lm(SalePrice ~ GrLivArea, data=nei_filtered)
summary(grliv_saleprice_reg)
coef(grliv_saleprice_reg)

grliv_reg <- lm(SalePrice ~ GrLivArea+YearBuilt+OverallQual, data=nei_filtered)
summary(grliv_reg)

lotarea_saleprice_reg <- lm(pricepersqft ~ GrLivArea+YearBuilt+OverallQual, data=nei_filtered) # not good results
summary(lotarea_saleprice_reg)

ggplot(data=nei_filtered)+aes(x=GrLivArea,y=SalePrice, color = Neighborhood  )  + 
  geom_point(alpha=0.6)+ 
  geom_line(mapping = aes(y=predict(grliv_saleprice_reg)),size=1)
