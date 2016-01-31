library(matrixStats)
library(plyr)
library(ggplot2)
library(reshape)
library(boot)

data = read.csv('results.csv', header=F)
colnames(data) = c('HypNo', 'Prior', 'Point_LL', 'Word', 'Correct', 'Proposed', 'Truth')

data$ACC = 0
data$ACC[data$Correct==data$Proposed & data$Proposed==data$Truth] = 1

data$Word = mapvalues(data$Word, from = c(" 'siblings'", " 'grandparents'", " 'parents'", " 'cousins'", " 'uncles/aunts'", " 'spouses'", " 'children'"), to = c("Sibling", "Grandparent", "Parent", "Cousin", "Uncle/Aunt", "Spouse", "Child"))


exp_prop <- function(df, amount) {
	posterior = df$Prior + amount*df$Point_LL
	lse = logSumExp(posterior)
	p = exp(posterior - lse)
	return(sum(p*df$ACC))
}

x = 1:400
k = daply(data, .(Word), function(Z) return(c(Y=sapply(x, exp_prop, df=Z))))
pd = data.frame(t(k))
pd$X = x
pd = melt(pd, id='X')
colnames(pd) = c('X','Word','Y')
pd$Y[pd$Y>0.999] = 0.999
data = pd

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





g = ggplot(pd, aes(x=X, y=Y, group=Word, color=Word, label=Word)) +
#	facet_grid(.~Word, scales='free_x') +
    labs(y='Proportion Correct Hypotheses', x='Number of Data Points') +
	geom_line(size=1) +
	theme_bw(base_size=14) +
#	theme(legend.position="none") +
	scale_colour_brewer(palette="Set1") +
	ylim(0,1)
ggsave('~/Projects/LogicalWordLearning/LearnLexicon/growth.pdf', g, width=6, height=4)
