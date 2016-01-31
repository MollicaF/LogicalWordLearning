############################################################################
# This script will make the figures for cogsci paper
############################################################################

library(matrixStats)
library(plyr)
library(ggplot2)
library(gdata)
library(dplyr)

names = c('Info2', 'Info1', 'Simu')
maxData = 50
maxDataRes = 1

exp_prob <- function(df, amount) {
  posterior = df$Prior + amount*df$Point_LL_1
  lse = logSumExp(posterior)
  p = exp(posterior - lse)
  return(sum(p[df$HypType=='CHAR']))
}

exp_f1 <- function(df, amount) {
  posterior = df$Prior + amount*df$Point_LL_1
  lse = logSumExp(posterior)
  p = exp(posterior - lse)
  return(sum(p*df$f1))
}

exp_pri <- function(df, amount, ratio) {
  prior = ifelse(df$HypType=="CHAR",
                 df$Prior + log(1-ratio),
                 df$Prior + log(ratio))
  posterior = prior + amount*df$Point_LL_0
  lse = logSumExp(posterior)
  p= exp(posterior - lse)
  return(sum(p[df$HypType=="CHAR"]))
}


for (fyle in names) {
  # Read in the file
  data = read.csv(paste(fyle, 'Mom.csv', sep=''), header=F)
  data = rbind(data, read.csv(paste(fyle, 'Grandma.csv', sep=''), header=F))
  data = rbind(data, read.csv(paste(fyle, 'Brother.csv', sep=''), header=F))
  data = rbind(data, read.csv(paste(fyle, 'Uncle.csv', sep=''), header=F))
  colnames(data) = c('HypNo', 'HypType', 'Prior', 'Point_LL_0', 'Point_LL_1', 'Point_LL_2', 'Word', 'Correct', 'Proposed', 'Truth')
  data$Word = trim(data$Word, recode.factor=T)
  data$HypType = trim(data$HypType, recode.factor=T)
  data$ACC = 0
  data$ACC[data$Correct==data$Proposed & data$Proposed==data$Truth] = 1
  data$Recall = data$Correct / data$Truth
  data$Precision = data$Correct / data$Proposed
  data$f1 = 2*(data$Recall*data$Precision)/(data$Recall+data$Precision)
  unique(data$Word[data$ACC==1])
  
   x = seq(1, maxData, maxDataRes)
  d = NULL
  for (amt in x){
    PhGd = ddply(data[data$Word!='uncle',], .(Word), function(Z){return(exp_prob(Z, amt))})
    colnames(PhGd)[2] = 'P'
    PhGd$Amount = amt
    PhGd$HypType = 'CHAR'
    d = rbind(d, PhGd)
  }

  for (amt in seq(1, 750, 15)){
    PhGd = ddply(data[data$Word=='uncle',], .(Word), function(Z){return(exp_prob(Z, amt))})
    colnames(PhGd)[2] = 'P'
    PhGd$Amount = amt
    PhGd$HypType = 'CHAR'
    d = rbind(d, PhGd)
  }
  
  d = rbind(d, data.frame(Word=d$Word, P=1-d$P, Amount=d$Amount, HypType='DEF'))
  
  plt = ggplot(d, aes(Amount, P, color=HypType, shape=HypType)) +
    geom_point() +
    geom_line() +
    facet_grid(~Word, scales='free_x') +
    labs(y='Posterior Probability', x='Number of Data Points') +
    ylim(0, 1) + 
    #guides(color=F, shape=F) +
    theme_bw() +
    theme(legend.justification = c(1, 0.5), legend.position = c(1, 0.5), legend.title=element_blank(), legend.background=element_rect(fill='transparent'), legend.key.size=unit(0.3,'cm'), legend.text=element_text(size=8), legend.margin=unit(0,'cm'), legend.key=element_rect(fill='transparent', color='transparent'))
  plt  
  ggsave(paste('Figures/', fyle, '-Shift.eps', sep=''), width=7, height=2)

  df1 = NULL
  for (amt in x){
    PhGd = ddply(data[!is.na(data$f1) & data$Word!='uncle',], .(Word, HypType), function(Z){return(exp_f1(Z, amt))})
    colnames(PhGd)[3] = 'pHgD'
    PhGd$Amount = amt
    df1 = rbind(df1, PhGd)
  }

  for (amt in seq(1, 750, 15)){
    PhGd = ddply(data[!is.na(data$f1) & data$Word=='uncle',], .(Word, HypType), function(Z){return(exp_f1(Z, amt))})
    colnames(PhGd)[3] = 'pHgD'
    PhGd$Amount = amt
    df1 = rbind(df1, PhGd)
  }
  
  plt = ggplot(df1, aes(Amount, pHgD, color=HypType, shape=HypType)) +
    geom_point() +
    geom_line() +
    facet_grid(~Word, scales='free_x') +
    ylim(0,1) +
    labs(y='Posterior Weighted F1', x='Number of Data Points') +
    guides(shape=F, color=F) +
    theme_bw() +
    theme(strip.background = element_blank(), strip.text = element_blank())
  plt
  ggsave(paste('Figures/', fyle, '-F1.eps', sep=''), width=7, height=2)

}

# Feature Matrix
library(reshape2)
data <- read.csv("featurematrix.csv")
data <- data[1:108]

melted_data <- melt(data)
melted_data$variable =  factor(melted_data$variable, levels = rev(levels(melted_data$variable)))

plt = ggplot(data = melted_data, aes(y=variable, x=X, fill=value)) + 
  geom_tile() + 
  scale_fill_gradient2(low = "white", high = "black", mid = "white",  midpoint = 0, limit = c(-1,1)) +
  theme_bw() +
  xlab('') + ylab('') +
  theme(legend.position="none") +
  theme(axis.text.x=element_blank(), axis.ticks.x=element_blank()) +
  coord_fixed(ratio=1)
plt
ggsave('feature_matrix.svg', plt, width=4.5, height=12)


# OLD
  dpr = NULL
  for (amt in 1:10) {
    for (rat in seq(0.01, 0.99, 0.01)) {
      dt = ddply(data, .(Word), function(Z){return(exp_pri(Z, amt, rat))})
      colnames(dt)[2] = 'pCHAR'
      dt$amount = amt
      dt$ratio = rat
      dpr = rbind(dpr, dt)
    }
  }
  
  plt = ggplot(dpr, aes(ratio, pCHAR, alpha=as.factor(amount))) +
    geom_line(aes(linetype=as.factor(amount)), size=1.25, color='forestgreen') +
    facet_grid(~Word) +
    guides(alpha=F, linetype=F) +
    theme_bw()
  plt
  ggsave(paste('Figures/', fyle, '-Prior.eps', sep=''), width=7, height=2)

