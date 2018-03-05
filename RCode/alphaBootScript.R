# Bootstrap Helper

args <- commandArgs(TRUE)

NBOOT  <- as.numeric(args[1]) # 10
ALPHA  <- as.numeric(args[2]) # 0.1, 0.5, 0.9
FOREST <- as.numeric(args[3]) # 0.3, 0.4, 0.5, 0.6
OUT    <- args[4] # 'Feathers/englishBoots.feather'
SOURCE <- '../Spaces/Space/GenericEnglish.csv'
KEY    <- '../Spaces/Keys/GenericEnglish_Key.csv'

source('utilities.R')

# Objects
obs = c('Amanda', 'Anne', 'aragorn', 'Arwen', 'Brandy', 'Celebrindal', 'Clarice', 'elrond', 'Eowyn', 'fabio', 'fred', 'frodo', 'Galadriel', 'gandalf', 'han', 'harry', 'Hermione', 'gary', 'james', 'joey', 'Katniss', 'legolas', 'Leia', 'Lily', 'luke', 'Luna', 'Mellissa', 'merry', 'Padme', 'peeta', 'Prue', 'ron', 'Rose', 'Sabrina', 'salem', 'sam', 'Zelda')

# Hypothesis Space
d = read.csv(SOURCE, header=F, strip.white = T)
colnames(d) = c('LexNo', 'Word', 'HPrior', 'LPrior', 'RPrior', 'Abstract', 'Recurse', 'Hypothesis', 'MODE', rep(obs,length(obs)-1), obs)
d = d[,c(1:8,10:(ncol(d)-1-length(obs)))]

# Ground Truth
ground = read.csv(KEY, header=F, strip.white = T)
colnames(ground) = c('I','Word', rep(obs,length(obs)-1))
row.names(ground) = ground$Word
ground = as.matrix(ground[3:ncol(ground)])

marginalBoots = NULL
for(i in 1:NBOOT){
  
  dist = sizePrinciple(ground, N=1000, alph = FOREST)
  
  eng = d %>%
    group_by(Word) %>%
    do(Hyp2Stats(., dist, ground, alpha=ALPHA, O=length(obs))) %>%
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
  for (amt in seq(0, 600, 1)) {
    k = plyr::ddply(diseng, c('Word'), function(Z) {marg_stats(Z, amt, 1)})
    data = rbind(data, k)
  }
  rm(k)
  
  # Record
  data$Sim = i
  marginalBoots = rbind(marginalBoots, data)
}
beepr::beep('treasure')

feather::write_feather(marginalBoots, OUT)
