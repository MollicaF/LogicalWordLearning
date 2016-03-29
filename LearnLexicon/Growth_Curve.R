library(matrixStats)
library(plyr)
library(ggplot2)
library(reshape)
library(boot)
library(gdata)

data = read.csv('results.csv', header=F)
colnames(data) = c('HypNo', 'Prior', 'Point_LL', 'Word', 'Correct', 'Proposed', 'Truth')

data$ACC = 0
data$ACC[data$Correct==data$Proposed & data$Proposed==data$Truth] = 1

data$Precision = data$Correct / data$Proposed
data$Precision[is.nan(data$Precision)] = 0
data$Recall = data$Correct / data$Truth

data$Word = trim(data$Word)
#data$Word = mapvalues(data$Word, from = c(" 'siblings'", " 'grandparents'", " 'parents'", " 'cousins'", " 'uncles/aunts'", " 'spouses'", " 'children'"), to = c("Sibling", "Grandparent", "Parent", "Cousin", "Uncle/Aunt", "Spouse", "Child"))


exp_stats <- function(df, amount) {
	posterior = df$Prior + amount*df$Point_LL
	lse = logSumExp(posterior)
	p = exp(posterior - lse)
    data.frame(amount=amount, Accuracy=sum(p*df$ACC), Precision=sum(p*df$Precision), Recall=sum(p*df$Recall))
}

d = NULL
for (amt in 1:400) {
    k = ddply(data, .(Word), function(Z) {exp_stats(Z, amt)})
    d = rbind(d, k)
}

d=melt(d, id=c('Word', 'amount'))

ggplot(d, aes(x=amount, value, linetype=variable, color=variable)) +
	facet_grid(.~Word, scales='free_x') +
    labs(y='Proportion', x='Number of Data Points') +
	geom_line(size=1) +
	theme_bw() +
	scale_colour_brewer(palette="Set1") +
	ylim(0,1) +
    theme(legend.title=element_blank())

ggsave('NRnego.eps', width=12, height=2)


### Frequency Analysis
data$prop = log(data$Y/(1-data$Y))
data$prop[data$prop==Inf] = 1
x = seq(0,2000,1)
uncle = with(data[data$Word=='Uncle.Aunt',], lm(prop~X))
betas_uncle = uncle$coef
betas_uncle[2] = betas_uncle[2]*(68/340)
y.unc = inv.logit(betas_uncle[1]+betas_uncle[2]*x)
rents = with(data[data$Word=='Parent',], lm(prop~X))
betas_rents = rents$coef
betas_rents[2] = betas_rents[2]*(50/340)
y.rent = inv.logit(betas_rents[1]+betas_rents[2]*x)
brother = with(data[data$Word=='Sibling',], lm(prop~X))
betas_brother = brother$coef
betas_brother[2] = betas_brother[2]*(34/340)
y.bro = inv.logit(betas_brother[1]+betas_brother[2]*x)
grandpa = with(data[data$Word=='Grandparent',], lm(prop~X))
betas_grandpa = grandpa$coef
betas_grandpa[2] = betas_grandpa[2]*(52/340)
y.grent = inv.logit(betas_grandpa[1]+betas_grandpa[2]*x)
pd = data.frame(x=x, uncle=y.unc, parents=y.rent, sibling=y.bro, grandparents=y.grent)
pot = melt(pd, id='x')
g = ggplot(pot, aes(x=x,y=value, group=variable, color=variable)) + geom_line(size=1)
