# Bootsrap Lexicons

args <- commandArgs(TRUE)

NBOOT  <- args[1] # 10
GAMMA = exp(-100)
  

source('utilities.R')

# Objects
obs = c('Amanda', 'Anne', 'aragorn', 'Arwen', 'Brandy', 'Celebrindal', 'Clarice', 'elrond', 'Eowyn', 'fabio', 'fred', 'frodo', 'Galadriel', 'gandalf', 'han', 'harry', 'Hermione', 'gary', 'james', 'joey', 'Katniss', 'legolas', 'Leia', 'Lily', 'luke', 'Luna', 'Mellissa', 'merry', 'Padme', 'peeta', 'Prue', 'ron', 'Rose', 'Sabrina', 'salem', 'sam', 'Zelda')

# Hypothesis Space
d = read.csv('../Spaces/Space/GenericEnglish_Reuse.csv', header=F, strip.white = T)
colnames(d) = c('LexNo', 'Word', 'HPrior', 'LPrior', 'RPrior', 'Abstract', 'Reuse', 'Recurse', 'Hypothesis', 'MODE', rep(obs,length(obs)-1), 'EGO', obs)
d = d[,c(1:9,11:(ncol(d)-1-length(obs)))]

# Ground Truth
ground = read.csv('../Spaces/Keys/GenericEnglish_Key.csv', header=F, strip.white = T)
colnames(ground) = c('I','Word', rep(obs,length(obs)-1))
row.names(ground) = ground$Word
ground = as.matrix(ground[3:ncol(ground)])

eng = d %>% select(-Abstract) %>%
  group_by(Word) %>%
  do(Hyp2Stats(., ground, ground, alpha=0.9, O=length(obs))) %>%
  ungroup() %>%
  select(LexNo, Word, Proposed, Correct, Truth) %>%
  mutate(ACC=ifelse(Correct==Proposed & Proposed==Truth, 1, 0),
         Precision=Correct/Proposed,
         Precision=ifelse(is.nan(Precision), 0, Precision),
         Recall=Correct/Truth) %>%
  select(LexNo, Word, ACC, Precision, Recall)

juntos=NULL
amboW=NULL
amboWR=NULL
for (j in 1:NBOOT) {
  
  dist = sizePrinciple(ground, N=350, alph = 0.9)
  
  lex = d %>%
    #mutate(RPrior=ifelse(grepl('True',Reuse), log(GAMMA)+RPrior, log(1-GAMMA)+RPrior)) %>%
    select(-Reuse) %>%
    do(lHyp2Stats(., dist, ground, alpha=0.9, O=length(obs))) %>%
    mutate(ACC=ifelse(Correct==Proposed & Proposed==Truth, 1, 0),
           Precision=Correct/Proposed,
           Precision=ifelse(is.nan(Precision), 0, Precision),
           Recall=Correct/Truth,
           F1=(2*Precision*Recall)/(Precision+Recall),
           F1=ifelse(is.nan(F1), 0, F1))
  
  data = NULL
  for (amt in seq(0, 350, 1)){
    data = rbind(data, exp_stats(lex %>% mutate(ACC=ifelse(Recurse, 0, ACC)), amt, 1))
  }
  data$Recurse = 'nRecurse'
  
  dataR = NULL
  for (amt in seq(0, 350, 1)){
    dataR = rbind(dataR, exp_stats(lex, amt, 1))
  }
  dataR$Recurse = 'Recursive'
  
  data = rbind(data, dataR)
  data$Sim = j
  juntos = rbind(juntos, data)
  
  lex = lex %>%
    select(-ACC, -Precision, -Recall) %>%
    left_join(eng)

  data = NULL
  for (amt in seq(0, 350, 1)){
    k = plyr::ddply(lex, c('Word'), function(Z) {exp_stats(Z, amt, 1)})
    data = rbind(data, k)
  }
  rm(k)
  
  data$Sim = j
  data$Recurse = 'Recurse'
  amboW = rbind(amboW, data)
  
  data = NULL
  for (amt in seq(0, 350, 1)){
    k = plyr::ddply(lex %>% mutate(ACC=ifelse(Recurse, 0, ACC)), c('Word'), function(Z) {exp_stats(Z, amt, 1)})
    data = rbind(data, k)
  }
  rm(k)
  
  data$Sim = j
  data$Recurse = 'nRecursive'
  amboWR = rbind(amboWR, data)
  
}

feather::write_feather(amboW, 'Feathers/EnglishLexiconDSbyWord.feather')
feather::write_feather(amboWR, 'Feathers/EnglishLexiconDSbyWordR.feather')
feather::write_feather(juntos, 'Feathers/EnglishLexicon.feather')
