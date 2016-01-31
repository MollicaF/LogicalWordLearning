library(ggplot2)
library(plyr)
d <- read.csv('priors.csv', header=T)
colnames(d)[1] = 'source'
d$p = as.numeric(as.character(d$p))
d$i = as.numeric(d$i)
d$temp = as.numeric(as.character(d$temp))
m <- sort(unique(d$i), decreasing=TRUE)[3]

q <- subset(d, i>2*m/3)       # Second half of samples
q <- subset(q, i<m)
q$x <- paste(q$nt, ' --> ', q$name, q$to)

q = ddply(q, .(source, i, nt), mutate, z=sum(p), gp=p/z, lgp=log(gp))

q$lgpj = q$lgp + 0.0000001*rnorm(length(q$lgp))

plt <- ggplot(q[q$nt!='START',], aes(x=x, y=lgpj)) +
    geom_violin(fill = "yellow", scale="width") +
    ylab("Log Probability") +  xlab("PCFG Parameter") +
    theme_bw() +
    theme(axis.text.x = element_text(angle = 90, hjust = 1))
plt
ggsave('~/Projects/LogicalWordLearning/Figures/InferredPriors.pdf',plt,width=10, height=4.5)

llt = ddply(q, .(source, i), summarise, llt=mean(temp), x="")

plt <- ggplot(llt, aes(x=x, y=llt)) +
    geom_violin(fill='green', scale='width') +
    ylab('Likelihood Temperature') + xlab('') +
    theme_bw()
plt
ggsave('~/Projects/LogicalWordLearning/Figures/LLT.pdf',plt,width=5, height=4.5)
optimal = ddply(q, .(nt, name, to, x), summarise, mean=mean(gp))
optimal = ddply(optimal, .(nt), transform, lambda=mean/min(mean))

write.csv(optimal, 'optimalGrammar.csv', row.names=F)
