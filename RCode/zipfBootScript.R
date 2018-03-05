# Bootstrap Zipf

args <- commandArgs(TRUE)

NBOOT  <- as.numeric(args[1]) # 10
ZS     <- as.numeric(args[2]) # 1, 2
FOREST <- as.numeric(args[3])
OUT    <- args[4] # 'Feathers/englishZ1Boots.feather'

source('utilities.R')
obs = c('Amanda', 'Anne', 'aragorn', 'Arwen', 'Brandy', 'Celebrindal', 'Clarice', 'elrond', 'Eowyn', 'fabio', 'fred', 'frodo', 'Galadriel', 'gandalf', 'han', 'harry', 'Hermione', 'gary', 'james', 'joey', 'Katniss', 'legolas', 'Leia', 'Lily', 'luke', 'Luna', 'Mellissa', 'merry', 'Padme', 'peeta', 'Prue', 'ron', 'Rose', 'Sabrina', 'salem', 'sam', 'Zelda')

if(ZS==0){
  d = read.csv('../Spaces/Space/GenericEnglish.csv', header=F, strip.white = T)
} else {
  d = read.csv('../Spaces/ZipfSpace/GenericEnglish_Z.csv', header=F, strip.white = T)
}
colnames(d) = c('LexNo', 'Word', 'HPrior', 'LPrior', 'RPrior', 'Abstract', 'Recurse', 'Hypothesis', 'MODE', rep(obs,length(obs)-1), obs)
d = d[,c(1:8,10:(ncol(d)-1-length(obs)))]

ground = read.csv('../Spaces/Keys/Zipf/GenericEnglish_Z_Key.csv', header=F, strip.white = T)
colnames(ground) = c('I','Word', rep(obs,length(obs)-1))
row.names(ground) = ground$Word
ground = as.matrix(ground[3:ncol(ground)])

speakers = read.csv('../Spaces/Keys/Speaker/GenericEnglish_sZ_Key.csv', header=F, strip.white = T)
colnames(speakers) = c('I','Word', obs)
row.names(speakers) = speakers$Word
speakers = as.matrix(speakers[3:ncol(speakers)])

s=ZS

marginalBoots = NULL
for(i in 1:NBOOT){

  if(FOREST==0){
    dist = sizePrinciple(ground>0, N=1000, alph = 0.9)
  } else {
    dist = wZipfDraw(ground, speakers, FOREST, N=1000)
  }

  if(ZS==0){
    eng = d %>%
      group_by(Word) %>%
      do(Hyp2Stats(., dist, ground>0, alpha=0.9, O=length(obs))) %>%
      ungroup() %>%
      select(HypNo=LexNo, Word, HPrior, LPrior, RPrior, HLike, Hypothesis, Abstract, Recurse, Proposed, Correct, Truth) %>%
      mutate(ACC=ifelse(Correct==Proposed & Proposed==Truth, 1, 0),
             Precision=Correct/Proposed,
             Precision=ifelse(is.nan(Precision), 0, Precision),
             Recall=Correct/Truth,
             F1=(2*Precision*Recall)/(Precision+Recall),
             F1=ifelse(is.nan(F1), 0, F1))
  } else {
    eng = d %>%
      group_by(Word) %>%
      do(zHyp2Stats(., dist, ground, s=s, alpha=0.9, O=length(obs))) %>%
      ungroup() %>%
      select(HypNo=LexNo, Word, HPrior, LPrior, RPrior, HLike, Hypothesis, Abstract, Recurse, Proposed, Correct, Truth) %>%
      mutate(ACC=ifelse(Correct==Proposed & Proposed==Truth, 1, 0),
             Precision=Correct/Proposed,
             Precision=ifelse(is.nan(Precision), 0, Precision),
             Recall=Correct/Truth,
             F1=(2*Precision*Recall)/(Precision+Recall),
             F1=ifelse(is.nan(F1), 0, F1))
  }
  
  diseng = eng %>%
    select(-HypNo, -LPrior, -RPrior) %>%
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
