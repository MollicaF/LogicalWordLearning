library(ggplot2)
library(gdata)
library(plyr)

data = read.csv('../LearnLexicon/PukaPuka/pukapukaResults.csv', header=F)
colnames(data) = c('HypNo', 'Prior', 'Point_LL', 'Word', 'Correct', 'Proposed', 'Truth')
data$Word = trim(data$Word)

d = subset(data, Word=='kainga')

### Make a GIF top 95% of prob mass
plot_posterior = function(amt) {
  d$post = (d$Prior + d$Point_LL*amt)
  m = max(d$post)
  z = m + log(sum(exp(d$post - m)))
  d$post = d$post - z
  d=d[order(d$post, decreasing=T),]
  d$cs=cumsum(exp(d$post))
  
  d$top = ifelse(d$cs < .95,
                 'b', 'c')
  d$top[d$post==max(d$post)] = 'a'

  g = 
    
    ggplot(d, aes(-Prior, -Point_LL)) +
    geom_point(aes(color=top)) +
    guides(color=F) +
    scale_x_log10() +
    scale_y_log10() +
    scale_color_manual(values=c('red','lawngreen','blue')) +
    geom_point(data=subset(d, top=='a'), aes(-Prior, -Point_LL), size=3, 
               color='red', shape=15) +
    ylab('Uncertainty') +
    xlab('Complexity') +
    ggtitle(paste('Data Points:', toString(amt))) +
    theme_bw()
  
  return(g)
}

folder = 'MovingTopPosterior3'
if (dir.exists(folder)) {
  unlink(folder, recursive = T)
}

dir.create(folder)
for (amt in 1:50) {
  ggsave(paste0(folder,'/Post_',sprintf("%03d", amt),'.png'),
         plot_posterior(amt),
         height=4, width=6)
}

### Make a GIF of entire dist
plot_posterior = function(amt) {
  g = 
    
    ggplot(d, aes(-Prior, -Point_LL)) +
    geom_point(aes(color=(Prior + Point_LL*amt))) +
    guides(color=guide_colorbar(title='Log Posterior')) +
    scale_x_log10() +
    scale_y_log10() +
    scale_color_gradientn(colors=rev(rainbow(3))) +
    ylab('Uncertainty') +
    xlab('Complexity') +
    ggtitle(paste('Data Points:', toString(amt))) +
    theme_bw()
  
  return(g)
}

if (dir.exists('MovingPosterior')) {
  unlink('MovingPosterior', recursive = T)
}

dir.create('MovingPosterior')
for (amt in 1:100) {
  ggsave(paste0('MovingPosterior/Post_',sprintf("%03d", amt),'.eps'),
         plot_posterior(amt),
         height=4, width=6)
}

####################################################
power.fit = function(par, df) {
  alpha = par[1]
  beta = par[2]
  E = alpha * ((-df$Prior)**(-beta))
  sum((-df$Point_LL - E)**2)
}

exp.fit = function(par, df) {
  lambda = par
  E = lambda * exp(lambda * df$Prior)
  sum((-df$Point_LL - E)**2)
}

d$round = .bincode(d$Prior, seq(min(d$Prior), max(d$Prior), 2))
prior = ddply(d, .(round), summarise, Point_LL=max(Point_LL), Prior=mean(Prior))


op = optim(c(1,1), power.fit, df=prior)
oe = optim(c(1), exp.fit, df=prior, method='BFGS')

plot_deriv = function(amt) {
  g = 
    
    ggplot(prior, aes(-Prior, -Point_LL)) +
    geom_point(aes(color=(Prior + Point_LL*amt))) +
    guides(color=guide_colorbar(title='Log Posterior')) +
    scale_x_log10() +
    scale_y_log10() +
    scale_color_gradientn(colors=rev(rainbow(3))) +
    geom_line(aes(x=-Prior, y=(1/(op$par[1]*op$par[2]))*(-Prior)**(op$par[1] + 1))) +
    ylab('Uncertainty') +
    xlab('Complexity') +
    ggtitle(paste('Data Points:', toString(amt))) +
    theme_bw()
  
  ggplot(prior, aes(-Prior, (1/(op$par[1]*op$par[2]))*(-Prior)**(op$par[1] + 1))) +
    geom_line() +
    ylab('Data Points Needed') +
    xlab('Complexity') +
    coord_flip() +
    theme_bw()
  
  return(g)
}

