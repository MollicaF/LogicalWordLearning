source('utilities.R')

obs = c('Amanda', 'Anne', 'aragorn', 'Arwen', 'Brandy', 'Celebrindal', 'Clarice', 'elrond', 'Eowyn', 'fabio', 'fred', 'frodo', 'Galadriel', 'gandalf', 'han', 'harry', 'Hermione', 'gary', 'james', 'joey', 'Katniss', 'legolas', 'Leia', 'Lily', 'luke', 'Luna', 'Mellissa', 'merry', 'Padme', 'peeta', 'Prue', 'ron', 'Rose', 'Sabrina', 'salem', 'sam', 'Zelda')

# Hypothesis Space
d = read.csv('../Spaces/topIroqLex.csv', header=F, strip.white = T)
colnames(d) = c('LexNo', 'Word', 'HPrior', 'LPrior', 'RPrior', 'Abstract', 'Reuse', 'Recurse', 'Hypothesis', 'MODE', rep(obs,length(obs)-1), 'EGO', obs)
ego = d[,c(1:9, (ncol(d)-length(obs)):ncol(d) )]

data = feather::read_feather('Feathers/PosteriorIroquois600.feather')

ego = ego %>% 
  select(-LexNo, -HPrior, -LPrior, -RPrior, -Abstract, -Recurse, -Reuse, -EGO) %>%
  distinct() %>%
  left_join(data)

pgen = ego %>%
  mutate(Amanda=Amanda*Posterior,
         Anne=Anne*Posterior,
         aragorn=aragorn*Posterior,
         Arwen=Arwen*Posterior,
         Brandy=Brandy*Posterior,
         Celebrindal=Celebrindal*Posterior,
         Clarice=Clarice*Posterior,
         elrond=elrond*Posterior,
         Eowyn=Eowyn*Posterior,
         fabio=fabio*Posterior,
         fred=fred*Posterior,
         frodo=frodo*Posterior,
         Galadriel=Galadriel*Posterior,
         gandalf=gandalf*Posterior,
         han=han*Posterior,
         harry=harry*Posterior,
         Hermione=Hermione*Posterior,
         gary=gary*Posterior,
         james=james*Posterior,
         joey=joey*Posterior,
         Katniss=Katniss*Posterior,
         legolas=legolas*Posterior,
         Leia=Leia*Posterior,
         Lily=Lily*Posterior,
         luke=luke*Posterior,
         Luna=Luna*Posterior,
         Mellissa=Mellissa*Posterior,
         merry=merry*Posterior,
         Padme=Padme*Posterior,
         peeta=peeta*Posterior,
         Prue=Prue*Posterior,
         ron=ron*Posterior,
         Rose=Rose*Posterior,
         Sabrina=Sabrina*Posterior,
         salem=salem*Posterior,
         sam=sam*Posterior,
         Zelda=Zelda*Posterior) %>%
  gather(Person, Prob, Amanda:Zelda) %>%
  group_by(Word, amount, Person) %>%
  summarise(PGen=sum(Prob))


savit = function(df){
  word = first(df$Word)
  amount = first(df$amount)
  fyle = paste0('GenP/',word,'_',amount,'.csv')
  write.csv(df, file=fyle, row.names = F, quote = F, col.names = F)
  df
}

pgen %>%
  group_by(Word, amount) %>%
  do(savit(.))

