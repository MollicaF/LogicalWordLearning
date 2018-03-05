library(tidyverse)
library(forcats)
library(ggrepel)
library(matrixStats)

########################################################################################
########################################################################################
########################################################################################
# Utilities

squash = function(x,o){colSums(matrix(x, nrow=o))}
mushroom = function(x,n){matrix(rep(x,each=n), ncol=n, byrow=TRUE)}

nicepow = function(x,s){ifelse(is.infinite(x**s), 0, x**s)}
nicedivide = function(x,y){ifelse(is.nan(x/y), 0, x/y)}

find_min = function(df, lim=0.99, meas='Accuracy'){
  min(df$amount[df$value >= lim & df$variable==meas], na.rm=T)
}

zipfConst = function(spce, s, O){
  Z = t(apply(spce, 1, function(x){squash(nicepow(x,-s),O-1)}))
  matrix(apply(Z, 2, function(x){mushroom(x, O-1)}), nrow=nrow(Z))
}

########################################################################################
########################################################################################
########################################################################################
# Likelihood Functions

correct = function(h, o, alph) { log(alph*(h**-1) + (1-alph)*(o**-2)) }
zcorrect = function(d, n, s, o, alph) { log( alph*((d**-s)/n) + (1-alph)*o**-2 )}
incorrect = function(o, alph) { log((1-alph)*(o**-2)) }

########################################################################################
########################################################################################
########################################################################################
# Distribution Functions

sizePrinciple = function(grnd, alph=0.9, N=100){
  data = matrix(NA, nrow=nrow(grnd), ncol=ncol(grnd))
  rownames(data) = rownames(grnd)
  for(wrd in rownames(grnd)) {
    p = ifelse(grnd[wrd,]==1, alph/sum(grnd[wrd,])+(1-alph)/length(grnd[wrd,]), (1-alph)/length(grnd[wrd,]))
    data[wrd,] = rmultinom(1, N/nrow(data), prob = p)
  }
  data
}

engFreq = c(.19, .16, .10, .15, .07, .09, .08, .09, .05)
names(engFreq) = c('mother','father','grandpa','grandma','brother','sister','uncle','aunt','cousin')

wSizePrinciple = function(grnd, alph=0.9, N=100){
  data = matrix(NA, nrow=nrow(grnd), ncol=ncol(grnd))
  rownames(data) = rownames(grnd)
  for(wrd in rownames(grnd)) {
    p = ifelse(grnd[wrd,]==1, alph/sum(grnd[wrd,])+(1-alph)/length(grnd[wrd,]), (1-alph)/length(grnd[wrd,]))
    data[wrd,] = rmultinom(1, round(N*engFreq[wrd]), prob = p)
  }
  data
}

zipfDraw = function(grnd, spkrs, s=1, O=length(obs), alph=0.9, N=100) {
  core = 1*(grnd > 0)
  card = zipfConst(grnd, s, O)
  refr = nicedivide(nicepow(grnd,-s), card)
  nspeak = nicepow(spkrs,-s)/rowSums(nicepow(spkrs,-s))
  speak = matrix(apply(nspeak, 2, function(x){mushroom(x, O-1)}), nrow=nrow(spkrs))
  p = refr*speak
  
  data = matrix(NA, nrow=nrow(grnd), ncol=ncol(grnd))
  rownames(data) = rownames(grnd)
  for(wrd in rownames(grnd)) {
    pn = p[wrd,]*alph + (1-alph)*O**-2
    data[wrd,] = rmultinom(1, N/nrow(data), prob = pn)
  }
  data
}  

wZipfDraw = function(grnd, spkrs, s=1, O=length(obs), alph=0.9, N=100) {
  core = 1*(grnd > 0)
  card = zipfConst(grnd, s, O)
  refr = nicedivide(nicepow(grnd,-s), card)
  nspeak = nicepow(spkrs,-s)/rowSums(nicepow(spkrs,-s))
  speak = matrix(apply(nspeak, 2, function(x){mushroom(x, O-1)}), nrow=nrow(spkrs))
  p = refr*speak
  
  data = matrix(NA, nrow=nrow(grnd), ncol=ncol(grnd))
  rownames(data) = rownames(grnd)
  for(wrd in rownames(grnd)) {
    pn = p[wrd,]*alph + (1-alph)*O**-2
    data[wrd,] = rmultinom(1, round(N*engFreq[wrd]), prob = pn)
  }
  data
}  

########################################################################################
########################################################################################
########################################################################################
# Evaluation Functions

eval_h = function(df, wrd, grnd, dst, alpha=0.9, O=length(obs)) {
  space = as.matrix(df[,9:ncol(df)])
  #card = rowSums(space)
  card = zipfConst(space, -1, O)
  core = 1*((space == grnd[rep(wrd, nrow(space)),]) & (space == 1))
  like = ifelse(core==1, correct(card, O, alpha), incorrect(O, alpha))
  point_ll = (like %*% dst[wrd,]) / sum(dst[wrd,])
  score = rowSums(core)
  prop = rowSums(space)
  list(point_ll, score, prop)
}

Hyp2Stats = function(df, dst, grnd, alpha=0.9, O=length(obs)){
  Word = as.character(first(df$Word))
  message(Word)
  r = eval_h(as.data.frame(df), Word, grnd, dst, alpha, O)
  df$HLike=as.vector(r[[1]])
  df$Correct=r[[2]]
  df$Proposed=r[[3]]
  df$Truth=sum(1*(grnd[Word,]==1))
  df
}

# Zipf Eval Functions

zeval_h = function(df, wrd, grnd, dst, s=1, alpha=0.9, O=length(obs)) {
  space = as.matrix(df[,9:ncol(df)])
  core = 1*((space == grnd[rep(wrd, nrow(space)),]) & (space > 0))
  card = zipfConst(space, s, O)
  like = ifelse(core==1, zcorrect(space, card, s, O, alpha), incorrect(O, alpha))
  point_ll = (like %*% dst[wrd,]) / sum(dst[wrd,])
  score = rowSums(core)
  prop = rowSums((space>0))
  list(point_ll, score, prop)
}

zHyp2Stats = function(df, dst, grnd, s=1, alpha=0.9, O=length(obs)){
  Word = as.character(first(df$Word))
  message(Word)
  r = zeval_h(as.data.frame(df), Word, grnd, dst, s, alpha, O)
  df$HLike=as.vector(r[[1]])
  df$Correct=r[[2]]
  df$Proposed=r[[3]]
  df$Truth=sum(1*(grnd[Word,]>0))
  df
}

# Lexicon Eval
leval_h = function(df, grnd, dst, alpha=0.9, O=length(obs)) {
  v = nrow(grnd)
  space = as.matrix(df[,9:ncol(df)])
  space = t(matrix(t(space), nrow=v*ncol(space)))
  grnd = t(matrix(t(grnd), nrow=v*ncol(grnd)))
  card = apply(space, 1, function(x){squash(x, O-1)}) # Collapse over O
  card = matrix(colSums(matrix(t(matrix(card, nrow=O)),nrow=v)), nrow=nrow(space)) # Align and collapse over W
  card = matrix(apply(card, 2, function(x){mushroom(x, (O-1))}), nrow=nrow(card)) # Scale back up to objects
  card = matrix(replicate(v, card, simplify = T), nrow=nrow(card)) # Scale back up to words
  core = 1*((space == grnd[rep(1, nrow(space)),]) & (space == 1))
  like = ifelse(core==1, correct(card, (v**.5)*O, alpha), incorrect((v**.5)*O, alpha))
  dst = t(matrix(t(dst), nrow=v*ncol(dst)))
  point_ll = (like %*% dst[1,]) / sum(dst)
  score = rowSums(core)
  prop = rowSums(space)
  list(point_ll, score, prop)
}

lHyp2Stats = function(df, dst, grnd, alpha=0.9, O=length(obs)){
  r = leval_h(as.data.frame(df), grnd, dst, alpha, O)
  df = df %>% 
    group_by(LexNo) %>% 
      summarise(LPrior=first(LPrior), 
                RPrior=first(RPrior), 
                Abstract=1*sum(Abstract)>0, 
                Recurse=1*sum(Recurse)>0) %>%
    ungroup()
  df$LLike=as.vector(r[[1]])
  df$Correct=r[[2]]
  df$Proposed=r[[3]]
  df$Truth=sum(grnd)
  df
}

########################################################################################
########################################################################################
########################################################################################
# Convolution Functions

exp_stats <- function(df, amount, lt) {
  posterior = df$LPrior + (amount*df$LLike)/lt
  postR = df$RPrior + (amount*df$LLike)/lt
  lse = logSumExp(posterior)
  lseR = logSumExp(postR)
  p = exp(posterior - lse)
  pR = exp(postR - lseR)
  data.frame(amount=amount, 
             Prior=c('Simplicity', 'Simplicity &\nReuse'),
             Accuracy=c(sum(p*df$ACC), sum(pR*df$ACC)), 
             Precision=c(sum(p*df$Precision),sum(pR*df$Precision)), 
             Recall=c(sum(p*df$Recall), sum(pR*df$Recall))
  )
}

marg_stats <- function(df, amount, lt) {
  posterior = df$HPrior + (amount*df$HLike)/lt
  lse = logSumExp(posterior)
  p = exp(posterior - lse)
  data.frame(amount=amount, 
             Prior=c('Simplicity'),
             Accuracy=c(sum(p*df$ACC)), 
             Precision=c(sum(p*df$Precision)), 
             Recall=c(sum(p*df$Recall)))
}

marg_post <- function(df, amount, lt) {
  posterior = df$HPrior + (amount*df$HLike)/lt
  lse = logSumExp(posterior)
  p = exp(posterior - lse)
  data.frame(Hypothesis=df$Hypothesis,
             amount=amount, 
             Posterior=p)
}

marg_cd_stats <- function(df, amount, lt) {
  charZ = logSumExp(df$HPrior[df$Char==1])
  defZ = logSumExp(df$HPrior[df$Char==0])
  #posterior = ifelse(df$Char==1, df$HPrior-charZ, df$HPrior-defZ) + (amount*df$HLike)/lt
  posterior = df$HPrior + (amount*df$HLike)/lt
  lse = logSumExp(posterior)
  p = exp(posterior - lse)
  data.frame(amount=amount, 
             Prior=c('Simplicity'),
             Char=c(sum(p*df$Char)),
             Accuracy=c(sum(p*df$ACC)), 
             Precision=c(sum(p*df$Precision)),
             Recall=c(sum(p*df$Recall)))
}
