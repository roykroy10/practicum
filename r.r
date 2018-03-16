rm(list=ls())
setwd("C:/Users/Royka/Documents/IDC/practicum")

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
# ?plot
#install.packages("ggplot2")
library(ggplot2)

mean_2006 <- tapply(train[train$YrSold==2006,]$SalePrice, train[train$YrSold==2006,]$Neighborhood, mean)
mean_2006 <- data.frame(mean_2006)
nei <- cbind(nei, mean_2006)
mean_2007 <- tapply(train[train$YrSold==2007,]$SalePrice, train[train$YrSold==2007,]$Neighborhood, mean)
mean_2007 <- data.frame(mean_2007)
nei <- cbind(nei, mean_2007)
mean_2008 <- tapply(train[train$YrSold==2008,]$SalePrice, train[train$YrSold==2008,]$Neighborhood, mean)
mean_2008 <- data.frame(mean_2008)
nei <- cbind(nei, mean_2008)
mean_2009 <- tapply(train[train$YrSold==2009,]$SalePrice, train[train$YrSold==2009,]$Neighborhood, mean)
mean_2009 <- data.frame(mean_2009)
nei <- cbind(nei, mean_2009)
mean_2010 <- tapply(train[train$YrSold==2010,]$SalePrice, train[train$YrSold==2010,]$Neighborhood, mean)
mean_2010 <- data.frame(mean_2010)
nei <- cbind(nei, mean_2010)

years_mean <- cbind.data.frame(mean_2006,mean_2007,mean_2008,mean_2009,mean_2010)

ggplot(subset(train), 
       aes(SalePrice, color = Neighborhood)) +
  stat_density(geom="line") +
  facet_wrap(~Neighborhood, scales = "free",ncol = 5)


p <- ggplot(data = train, aes(x = SalePrice)) + geom_density()
p + facet_wrap(~Neighborhood, scales = "free")
# p <- ggplot(data = train, aes(x = SalePrice)) + geom_histogram(binwidth = 1000)
# p + facet_wrap(~Neighborhood, scales = "free")

nei <- nei[nei$count>50,] # Remove neighborhoods with less the 50 houses

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

ggplot(nei_filtered[nei_filtered$Neighborhood=="Edwards", ], aes(x=factor(YrSold), y=factor(MoSold),size=SalePrice))+
  geom_point(position='jitter', color='darkblue', fill='cornsilk', shape=21) + geom_boxplot(aes(x=Neighborhood,y=mean_pricepersqft))+ scale_size_area(max_size=15)

View(nei_filtered[nei_filtered$Neighborhood=="Edwards" & nei_filtered$pricepersqft<nei_filtered$mean_pricepersqft,])

install.packages("plotly")
library(plotly)

# function for computing mean, DS, max and min values
min.mean.sd.max <- function(x) {
  r <- c(min(x), mean(x) - sd(x), mean(x), mean(x) + sd(x), max(x))
  names(r) <- c("ymin", "lower", "middle", "upper", "ymax")
  r
}

p2 <- ggplot( nei_filtered[nei_filtered$Neighborhood=="NAmes", ], aes(x=factor(MoSold) , y=SalePrice, color=YrSold)) + scale_color_distiller(palette = "RdPu")
p2 <- p2 + stat_summary(fun.data = min.mean.sd.max, geom = "boxplot") + geom_jitter(size=5)
p2
p1 <- ggplot(aes(y = SalePrice, x = factor(YrSold)), data = nei_filtered[nei_filtered$Neighborhood=="NAmes", ])
p1 <- p1 + stat_summary(fun.data = min.mean.sd.max, geom = "boxplot") + geom_jitter(position=position_jitter(width=.2), size=3) + ggtitle("Sale price by year and ") + xlab("YrSold") + ylab("SalePrice")
p1
library(glmnet)

grliv_saleprice_reg <- lm(SalePrice ~ GrLivArea+YearBuilt+factor(Neighborhood)+LotArea+TotalBsmtSF, data=nei_filtered)
summary(grliv_saleprice_reg)
coef(grliv_saleprice_reg)

grliv_reg <- lm(SalePrice ~ GrLivArea+YearBuilt+OverallQual, data=nei_filtered)
summary(grliv_reg)

test_reg <- lm(SalePrice ~ GrLivArea+TotalBsmtSF+LotArea -1, data=train)
summary(test_reg)

lotarea_saleprice_reg <- lm(pricepersqft ~ GrLivArea+YearBuilt+OverallQual, data=nei_filtered) # not good results
summary(lotarea_saleprice_reg)

ggplot(data=nei_filtered)+aes(x=GrLivArea,y=SalePrice, color = Neighborhood  )  + 
  geom_point(alpha=0.6)+ 
  geom_line(mapping = aes(y=predict(grliv_saleprice_reg)),size=1)


train$weighted_size = weighted.mean(c(train$LotArea,train$TotalBsmtSF,train$GrLivArea),c(0.2107,61.6591,75.7305))


ggplot( nei_filtered[nei_filtered$Neighborhood=="Edwards", ], aes(x=factor(YrSold) , y=SalePrice, color=YrSold))  + 
  scale_color_gradient(low = "black", high = "red")+ stat_summary(fun.data = min.mean.sd.max, geom = "boxplot")+ geom_jitter(size=5)

ggplot( nei_filtered, aes(x=factor(MoSold) , y=SalePrice, color=Neighborhood))  + 
   stat_summary(fun.data = min.mean.sd.max, geom = "boxplot")+ geom_jitter(size=5)

