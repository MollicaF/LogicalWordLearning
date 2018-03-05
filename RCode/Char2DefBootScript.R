# Bootsrap Char2Def

args <- commandArgs(TRUE)

NBOOT  <- args[1] # 10
INFO   <- args[2]
SOURCE_CHAR <- args[3] # '../Spaces/Space/Info1Char.csv'
SOURCE_DEF  <- args[4] # '../Spaces/Space/Info1Def.csv'
SOURCE_GEN  <- args[5] # '../Spaces/Space/Info1Generic.csv'
KEY    <- args[6] # '../Spaces/Keys/Ego/Info1_E_Key.csv' '../Spaces/Keys/Info1_Key.csv'
OUT    <- args[7] # 'Feathers/info1Boots.feather'

source('utilities.R')

# Objects

if(INFO == 1){
  obs = c('Info1', 'A1', 'a2', 'a3', 'A4', 'A5', 'a6', 'a7', 'a8', 'a9',
        'A10', 'A11', 'A12', 'a13', 'A14', 'a15', 'A16', 'A17', 'a18', 'A19', 'A20',
        'a21', 'a22', 'A23', 'a24', 'a25', 'a26', 'A27', 'A28', 'a29', 'A30')
}

if(INFO == 2){
  obs = c('B1', 'b2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'b9', 'B10', 'B11',
          'b12', 'B13', 'B14', 'B15', 'b16', 'B17', 'b18', 'b19', 'b20', 'b21',
          'Info2', 'B22', 'B23')
}

if(INFO == 3) {
  obs = c('info3', 'c1', 'C2', 'C3', 'c4', 'C5', 'c6', 'C7', 'c8', 'c9', 'c10', 'C11', 'c12')
}

if(INFO == 4) {
  obs = c('info4', 'D1', 'd2', 'D3', 'd4', 'd5', 'd6', 'D7', 'd8', 'D9', 'd10', 'd11', 'd12', 'D13', 'D14',
          'D15', 'D16', 'D17', 'd18')
}

# Hypothesis Space
d1 = read.csv(SOURCE_CHAR, header=F, strip.white = T)
colnames(d1) = c('LexNo', 'Word', 'HPrior', 'LPrior', 'RPrior', 'Abstract', 'Char', 'Hypothesis', 'MODE', rep(obs,length(obs)-1),'MODE2', obs)
#d1 = d1[,c(1:8,(ncol(d1)-length(obs)+1):ncol(d1))] # EGO
d1 = d1[,c(1:8,10:(ncol(d1)-1-length(obs)))] # WORLD
d1$Char = 1

d2 = read.csv(SOURCE_DEF, header=F, strip.white = T)
colnames(d2) = c('LexNo', 'Word', 'HPrior', 'LPrior', 'RPrior', 'Abstract', 'Char', 'Hypothesis', 'MODE', rep(obs,length(obs)-1),'MODE2', obs)
#d2 = d2[,c(1:8,(ncol(d2)-length(obs)+1):ncol(d2))] # EGO
d2 = d2[,c(1:8,10:(ncol(d2)-1-length(obs)))] # WORLD
d2$Char = 0

d3 = read.csv(SOURCE_GEN, header=F, strip.white = T)
colnames(d3) = c('LexNo', 'Word', 'HPrior', 'LPrior', 'RPrior', 'Abstract', 'Char', 'Hypothesis', 'MODE', rep(obs,length(obs)-1),'MODE2', obs)
#d3 = d3[,c(1:8,(ncol(d3)-length(obs)+1):ncol(d3))] # EGO
d3 = d3[,c(1:8,10:(ncol(d3)-1-length(obs)))] # WORLD
d3 = d3 %>% filter(Char == 0, Abstract == 1)


d = rbind(d1,d2, d3)
rm(d1, d2, d3)

# Ground Truth
ground = read.csv(KEY, header=F, strip.white = T)
colnames(ground) = c('I','Word')
row.names(ground) = ground$Word
ground = as.matrix(ground[3:ncol(ground)])

Info1Boots = NULL
for(i in 1:NBOOT){
  
  dist = sizePrinciple(ground, N=10000, alph = 0.9)
  
  eng = d %>%
    group_by(Word) %>%
    do(Hyp2Stats(., dist, ground, alpha=0.9, O=length(obs))) %>%
    ungroup() %>%
    select(HypNo=LexNo, Word, HPrior, LPrior, RPrior, HLike, Hypothesis, Abstract, Char, Proposed, Correct, Truth) %>%
    filter(Truth>0) %>%
    mutate(ACC=ifelse(Correct==Proposed & Proposed==Truth, 1, 0),
           Precision=Correct/Proposed,
           Precision=ifelse(is.nan(Precision), 0, Precision),
           Recall=Correct/Truth,
           F1=(2*Precision*Recall)/(Precision+Recall),
           F1=ifelse(is.nan(F1), 0, F1))
  
  diseng = eng %>%
    select(-HypNo, -RPrior, -LPrior) %>%
    group_by(Word, Hypothesis) %>%
    mutate(HPrior=mean(HPrior)) %>%
    ungroup() %>%
    distinct()
  
  data = NULL
  for (amt in seq(0, 600, 1)) {
    k = plyr::ddply(diseng, c('Word'), function(Z) {marg_cd_stats(Z, amt, 1)})
    data = rbind(data, k)
  }
  rm(k)
  
  # Record
  data$Sim = i
  Info1Boots = rbind(Info1Boots, data)
}  
#beepr::beep('treasure')

feather::write_feather(Info1Boots, OUT)
