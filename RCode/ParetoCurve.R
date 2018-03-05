source('utilities.R')

# Objects
obs = c('Amanda', 'Anne', 'aragorn', 'Arwen', 'Brandy', 'Celebrindal', 'Clarice', 'elrond', 'Eowyn', 'fabio', 'fred', 'frodo', 'Galadriel', 'gandalf', 'han', 'harry', 'Hermione', 'gary', 'james', 'joey', 'Katniss', 'legolas', 'Leia', 'Lily', 'luke', 'Luna', 'Mellissa', 'merry', 'Padme', 'peeta', 'Prue', 'ron', 'Rose', 'Sabrina', 'salem', 'sam', 'Zelda')

# Hypothesis Space
d = read.csv('../Spaces/Space/GenericEnglish.csv', header=F, strip.white = T)
colnames(d) = c('LexNo', 'Word', 'HPrior', 'LPrior', 'RPrior', 'Abstract', 'Recurse', 'Hypothesis', 'MODE', rep(obs,length(obs)-1), obs)
d = d[,c(1:8,10:(ncol(d)-1-length(obs)))]

# Ground Truth
ground = read.csv('../Spaces/Keys/GenericEnglish_Key.csv', header=F, strip.white = T)
colnames(ground) = c('I','Word', rep(obs,length(obs)-1))
row.names(ground) = ground$Word
ground = as.matrix(ground[3:ncol(ground)])

dist = sizePrinciple(ground, N=1000, alph = 0.9)

eng = d %>%
  group_by(Word) %>%
  do(Hyp2Stats(., dist, ground, alpha=0.9, O=length(obs))) %>%
  ungroup() %>%
  select(HypNo=LexNo, Word, HPrior, LPrior, RPrior, HLike, Hypothesis, Abstract, Recurse, Proposed, Correct, Truth) %>%
  mutate(ACC=ifelse(Correct==Proposed & Proposed==Truth, 1, 0),
         Precision=Correct/Proposed,
         Precision=ifelse(is.nan(Precision), 0, Precision),
         Recall=Correct/Truth,
         F1=(2*Precision*Recall)/(Precision+Recall),
         F1=ifelse(is.nan(F1), 0, F1))

lex = d %>%
  do(lHyp2Stats(., dist, ground, alpha=0.9, O=length(obs))) %>%
  mutate(ACC=ifelse(Correct==Proposed & Proposed==Truth, 1, 0),
         Precision=Correct/Proposed,
         Precision=ifelse(is.nan(Precision), 0, Precision),
         Recall=Correct/Truth,
         F1=(2*Precision*Recall)/(Precision+Recall),
         F1=ifelse(is.nan(F1), 0, F1))


mass = function(df, amt){
  
  w = first(df$Word) %>% as.character()
  
  df = df %>%
    mutate(amount=amt, 
           post_score=HPrior + HLike*(amt*engFreq[w]))
  
  lse = logSumExp(df$post_score)
  
  df %>%
    mutate(posterior = exp(post_score - lse)) %>%
    select(-post_score)
}

diseng = eng %>%
  select(-HypNo, -LPrior, -RPrior) %>%
  filter(Recurse==0) %>%
  distinct()

data = NULL
for (amt in seq(0, 300, 2)) {
  k = plyr::ddply(diseng, c('Word'), function(Z) {mass(Z, amt)})
  data = rbind(data, k)
}

massL = function(df, amt){
  
  df = df %>%
    mutate(amount=amt, 
           post_score=LPrior + LLike*amt)
  
  lse = logSumExp(df$post_score)
  
  df %>%
    mutate(posterior = exp(post_score - lse)) %>%
    select(-post_score)
}

Leng = eng %>%
  select(-LPrior, -RPrior) %>%
  left_join(lex %>% select(HypNo=LexNo, LPrior, LLike)) %>%
  select(-HypNo) %>%
  filter(Recurse==0) %>%
  distinct()

dataH = NULL
for (amt in seq(0, 300, 2)) {
  k = plyr::ddply(Leng, c('Word'), function(Z) {massL(Z, amt)})
  dataH = rbind(dataH, k)
}

dataR = bind_rows(
  data %>% select(Word, Hypothesis, HPrior, HLike, ACC, amount, posterior) %>% mutate(Model='Hypothesis'),
  dataH %>% select(Word, Hypothesis, HPrior, HLike, ACC, amount, posterior) %>% mutate(Model='Lexicon')
)

dataR %>% 
  filter(amount==i) %>% 
  group_by(Model) %>% 
  mutate(MAP=ifelse(posterior==max(posterior), 1, 0)) %>% 
  ungroup() %>% 
  group_by(Model, Word) %>%
  arrange(posterior) %>%
  mutate(cPost=cumsum(posterior)) %>%
  ungroup()%>%
  filter(Model=='Hypothesis', Word=='uncle', cPost > 0.05) %>% 
  arrange(cPost) %>%
  head()

for (i in seq(0, 300, 2)) {
  dataR %>% 
    filter(amount==i) %>% 
    group_by(Model) %>% 
      mutate(MAP=ifelse(posterior==max(posterior), 1, 0)) %>% 
    ungroup() %>% 
  ggplot(aes(HPrior, HLike, shape=as.factor(ACC))) +
    facet_grid(Word~Model) +
    geom_point(color='grey80', alpha=0.05, size=3, data=. %>% filter(., MAP==0)) +
    geom_point(aes(color=posterior), size=3, data= . %>% group_by(Model, Word) %>%
                 arrange(posterior) %>%
                 mutate(cPost=cumsum(posterior)) %>%
                 ungroup() %>%
                 filter(cPost >= 0.05)) +
    #scale_color_gradient2(high='red', low='blue', mid='white', midpoint = 0.15) +
    scale_color_gradientn(colors=c('skyblue','red','orange','yellow','green','forestgreen'), limits=c(0,1)) +
    guides(shape=F, color=guide_colorbar(title=paste0('N=',stringr::str_pad(i, 3, pad='0'),'\n\nPosterior\nProbability'))) +
    ylab('Fit to Data') +
    xlab('Simplicity') +
    theme_bw()
  ggsave(paste0('SVG/Pareto_',formatC(i, width=3, format='d', flag=0),'.svg'), width=8, height=7, dpi=300)
}
