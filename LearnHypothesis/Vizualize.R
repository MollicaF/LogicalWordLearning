library(ggplot2)
library(matrixStats)
library(reshape)
library(gdata)

hd = read.csv('snow.data')
hd$X = NULL
gen = hd[, 5:14]/hd[, 4]
gen$GroupNo = hd$ItemNo
gen = melt(gen, id='GroupNo')
gen$GroupNo = gen$GroupNo + 1 
names = colnames(hd)[5:14]
for (n in names) {
  hd[, n] = ifelse(is.na(hd[, n]), NA, n)
}

lt = read.csv(paste('Viz/', md, '.csv', sep=''), header=F)
colnames(lt) = c('accRate', 'Prior', 'Likelihood', 'SET',
                 'Parent', 'Child', 'Spouse',
                 'Union', 'Complement', 'Intersection', 'SetDifference',
                 'Female', 'Male', 'SameGender',
                 'Gen0', 'Gen1', 'Gen2',
                 'Ancestors', 'Descendants',
                 'Maternal', 'Paternal',
#                   'Brother', 'Sister', 'Mother', 'Father', 'Children', 'Uncle', 'Aunt', 'Grandpa', 'Grandma', 'Cousin',
                 'Snow', 'charming', 'emma', 'Mira', 'rump', 'Regina', 'henry', 'neal', 'baelfire', 'Maryann', 'ego',
                 'all', 'X')

L = as.matrix(read.table(paste('Viz/Likelihoods_', md, '.csv', sep=''), header=F, sep=' '))

cnts = read.csv(paste('Viz/Counts_', md, '.csv', sep=''), header=F)
colnames(cnts) = c('Parent', 'Child', 'Spouse',
                   'Union', 'Complement', 'Intersection', 'SetDifference',
                   'Female', 'Male', 'SameGender',
                   'Gen0', 'Gen1', 'Gen2',
                   'Ancestors', 'Descendants',
                   'Maternal', 'Paternal',
                   #                   'Brother', 'Sister', 'Mother', 'Father', 'Children', 'Uncle', 'Aunt', 'Grandpa', 'Grandma', 'Cousin',
                   'Snow', 'charming', 'emma', 'Mira', 'rump', 'Regina', 'henry', 'neal', 'baelfire', 'Maryann', 'ego',
                   'all', 'X')

Model = read.csv(paste('Viz/Model_', md, '.csv', sep=''), header=F)

# Which grammar probs to use
lt$Posterior = lt$Likelihood + lt$Prior
lt$Posterior = lt$Posterior - logSumExp(lt$Posterior)
hypotheses = lt[lt$Posterior==max(lt$Posterior),]

counts = as.matrix(cnts)
rules = log(as.matrix(hypotheses[, c(5:34)]))
prior = rules %*% t(counts)

m = NULL
for(i in 1:dim(L)[2]) {
  # POSTERIOR
  posterior = prior + L[, i]
  posterior = exp(posterior - logSumExp(posterior))
  mass = posterior %*% as.matrix(Model[, ((i-1)*8+1):(i*8)])
  colnames(mass) = hd[hd$ItemNo==(i-1), 5:14][!is.na(hd[hd$ItemNo==(i-1), 5:14])]
  mpost = melt(data.frame(mass))
  colnames(mpost) = c('Object', 'Prob')
  mpost$Plot = 'Posterior'
  mpost$GroupNo = i
  
  # PRIOR
  posterior = prior
  posterior = exp(posterior - logSumExp(posterior))
  mass = posterior %*% as.matrix(Model[, ((i-1)*8+1):(i*8)])
  colnames(mass) = hd[hd$ItemNo==(i-1), 5:14][!is.na(hd[hd$ItemNo==(i-1), 5:14])]
  mpri = melt(data.frame(mass))
  colnames(mpri) = c('Object', 'Prob')
  mpri$Plot = 'Prior'
  mpri$GroupNo = i
  
  # LIKELIHOOD
  posterior =  L[, i]
  posterior = exp(posterior - logSumExp(posterior))
  mass = posterior %*% as.matrix(Model[, ((i-1)*8+1):(i*8)])
  colnames(mass) = hd[hd$ItemNo==(i-1), 5:14][!is.na(hd[hd$ItemNo==(i-1), 5:14])]
  mll = melt(data.frame(mass))
  colnames(mll) = c('Object', 'Prob')
  mll$Plot = 'Likelihood'  
  mll$GroupNo = i
  
  m = rbind(m, mpri, mpost, mll)
}

m$Plot = as.factor(m$Plot)
m$Plot = factor(m$Plot, levels(m$Plot)[c(3,1,2)])

m = GenProbs('Inference')

ggplot(m, aes(Object, Prob)) +
  stat_summary(fun.y=mean, geom='point') + 
  #stat_summary(fun.data=mean_cl_boot, geom='linerange') +
  geom_point(data=gen, aes(variable, value), shape=2) +
  facet_grid(Plot~GroupNo) +
  guides(color=F) +
  ylab('Gen. Prob.') +
  ylim(0, 1) +
  theme_bw() +
  theme(axis.text.x=element_text(angle=80, hjust=.5, vjust=.5))

#ggsave('MAP.eps', width=16, height=10)
grammarPriors = melt(rules)
grammarPriors$X2 = reorder(grammarPriors$X2, new.order=colnames(rules))

ggplot(grammarPriors, aes(X2, exp(value))) +
  stat_summary(fun.y=mean, geom='point') + 
  #stat_summary(fun.data=mean_cl_boot, geom='linerange') +
  xlab('') + ylab('Rule Probability') +
  theme_bw() +
  theme(axis.text.x=element_text(angle=80, hjust=.5, vjust=.5))
