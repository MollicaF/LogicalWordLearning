source('utilities.R')

count_post <- function(df, amount, lt) {
  posterior = df$HPrior + (amount*df$HLike)/lt
  lse = logSumExp(posterior)
  p = exp(posterior - lse)
  data.frame(amount=amount, 
             n=sort(p, decreasing = T) %>% cumsum %>% (function(x){ifelse(x<.95, 1, 0)}) %>% sum() + 1,
             u=(df$ACC*sort(p, decreasing = T) %>% cumsum) %>% (function(x){ifelse(x<.95, 1, 0)}) %>% sum() + 1)
}

# Objects
obs = c('Amanda', 'Anne', 'aragorn', 'Arwen', 'Brandy', 'Celebrindal', 'Clarice', 'elrond', 'Eowyn', 'fabio', 'fred', 'frodo', 'Galadriel', 'gandalf', 'han', 'harry', 'Hermione', 'gary', 'james', 'joey', 'Katniss', 'legolas', 'Leia', 'Lily', 'luke', 'Luna', 'Mellissa', 'merry', 'Padme', 'peeta', 'Prue', 'ron', 'Rose', 'Sabrina', 'salem', 'sam', 'Zelda')

d = read.csv('../Spaces/Space/GenericTurkish.csv', header=F, strip.white = T)
colnames(d) = c('LexNo', 'Word', 'HPrior', 'LPrior', 'RPrior', 'Abstract', 'Recurse', 'Hypothesis', 'MODE', rep(obs,length(obs)-1), obs)
d = d[,c(1:8,10:(ncol(d)-1-length(obs)))]

# Ground Truth
ground = read.csv('../Spaces/Keys/GenericTurkish_Key.csv', header=F, strip.white = T)
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

diseng = eng %>%
  select(-HypNo, -RPrior, -LPrior) %>%
  filter(Recurse==0) %>%
  distinct()

data = NULL
for (amt in seq(0, 200, 1)) {
  k = plyr::ddply(diseng, c('Word'), function(Z) {count_post(Z, amt, 1)})
  data = rbind(data, k)
}
rm(k)

data %>%
  filter(amount>0) %>%
  group_by(Word) %>%
  summarise(N=max(n))

data %>%
  filter(amount>0) %>%
  group_by(Word) %>%
  filter(n==max(n)) %>% print(n=nrow(.))
