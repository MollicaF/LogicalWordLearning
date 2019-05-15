# Reviewers wanted a recursive call version of the lexicon; however, we were unable to construct a satisfactory hypothesis space. Instead,
# we modified the prior distribution over hypotheses to either favor reuse (a la rational rules Goodman et al., 2008) or compression (which 
# rewards recursion). The analyses follow.

NBOOT = 1000

source('utilities.R')

# Objects
obs = c('Amanda', 'Anne', 'aragorn', 'Arwen', 'Brandy', 'Celebrindal', 'Clarice', 'elrond', 'Eowyn', 'fabio', 'fred', 'frodo', 'Galadriel', 'gandalf', 'han', 'harry', 'Hermione', 'gary', 'james', 'joey', 'Katniss', 'legolas', 'Leia', 'Lily', 'luke', 'Luna', 'Mellissa', 'merry', 'Padme', 'peeta', 'Prue', 'ron', 'Rose', 'Sabrina', 'salem', 'sam', 'Zelda')

# Hypothesis Space
d = read.csv('../Spaces/Space/GenericPriorAnalysis.csv', header=F, strip.white = T)
colnames(d) = c('LexNo', 'Word', 'HPrior', 'LPrior', 'RPrior', 'RzPrior', 'Abstract', 'Reuse', 'Recurse', 'Hypothesis', 'MODE', rep(obs,length(obs)-1))
# The rule is the space has to start at the 9th column
d = d[,c(1:(ncol(d)))]
d = select(d, -Abstract, -Reuse, -Recurse)

# Ground Truth
ground = read.csv('../Spaces/Keys/GenericEnglish_Key.csv', header=F, strip.white = T)
colnames(ground) = c('I','Word', rep(obs,length(obs)-1))
row.names(ground) = ground$Word
ground = as.matrix(ground[3:ncol(ground)])

eng = d %>%
    group_by(Word) %>%
    do(Hyp2Stats(., ground, ground, alpha=0.9, O=length(obs))) %>%
    ungroup() %>%
    mutate(ACC=ifelse(Correct==Proposed & Proposed==Truth, 1, 0),
           Precision=Correct/Proposed,
           Precision=ifelse(is.nan(Precision), 0, Precision),
           Recall=Correct/Truth) %>%
    select(LexNo, Word, LPrior, RPrior, RzPrior, ACC, Precision, Recall)

amboW=NULL
amboWR=NULL
for (j in 1:NBOOT) {
    
    dist = sizePrinciple(ground, N=350, alph = 0.9)
    
    lex = eng %>%
        left_join(data.frame(LexNo=d %>%pull(LexNo)%>%unique(),
                             LLike=as.vector(leval_h(d, ground, dist)[[1]])))
    
    # The exp_stats looks at LPrior and RPrior so lets first do the reuse situation
    data = NULL
    for (amt in seq(0, 350, 1)){
        k = plyr::ddply(lex, c('Word'), function(Z) {exp_stats(Z, amt, 1)})
        data = rbind(data, k)
    }
    rm(k)
    
    amboW = bind_rows(amboW,
                      data %>% mutate(Sim = j))
    
    # The exp_stats looks at LPrior and RPrior so lets switch so it does the recursion
    data = NULL
    for (amt in seq(0, 350, 1)){
        k = plyr::ddply(lex %>% mutate(RPrior=RzPrior), c('Word'), function(Z) {exp_stats(Z, amt, 1)})
        data = rbind(data, k)
    }
    rm(k)
    
    amboWR = bind_rows(amboWR,
                      data %>% mutate(Sim = j,
                                      Prior = ifelse(Prior=='Simplicity', Prior, 'Compression Prior')))

}

feather::write_feather(amboW, 'Feathers/PriorEnglishReuse.feather')
feather::write_feather(amboWR, 'Feathers/PriorEnglishRecursion.feather')

amboW %>%
    mutate(Prior = fct_recode(Prior, 'Simplicity & Reuse'='Simplicity &\nReuse')) %>%
    filter(amount < 226,
           !(Prior!='Simplicity' & amount > 30)) %>%
    gather(measure, value, Accuracy:Recall) %>%
    ggplot(aes(amount, value, color=measure)) +
    facet_grid(Word~Prior, scales='free') +
    labs(y='Proportion', x='Number of Data Points') +
    theme(legend.title=element_blank()) +
    stat_summary(fun.y=mean, 
                 geom='line',
                 size=1,
                 alpha=0.5) +
    stat_summary(fun.y=mean_cl_boot, 
                 geom='ribbon',
                 aes(fill=measure),
                 alpha=0.15) +
    theme_bw() +
    theme(legend.title=element_blank(), legend.position = 'top',
          legend.margin = margin(0,0,-.25,0,unit='cm'))
#ggsave('../Figures/PriorAnalysisReuse.svg', width=6, height=8)

amboWR %>%
    mutate(Prior = fct_recode(Prior, 'Simplicity'='1')) %>%
    filter(amount < 226,
           !(Prior!='Simplicity' & amount > 175)) %>%
    gather(measure, value, Accuracy:Recall) %>%
    ggplot(aes(amount, value, color=measure)) +
    facet_grid(Word~Prior, scales='free') +
    labs(y='Proportion', x='Number of Data Points') +
    theme(legend.title=element_blank()) +
    stat_summary(fun.y=mean, 
                 geom='line',
                 size=1,
                 alpha=0.5) +
    stat_summary(fun.y=mean_cl_boot, 
                 geom='ribbon',
                 aes(fill=measure),
                 alpha=0.15) +
    theme_bw() +
    theme(legend.title=element_blank(), legend.position = 'top',
          legend.margin = margin(0,0,-.25,0,unit='cm'))
#ggsave('../Figures/PriorAnalysisRecursion.svg', width=6, height=8)

amboWR %>%
    gather(measure, value, Accuracy:Recall) %>%
    ggplot(aes(amount, value, color=measure)) +
    facet_grid(Word~Prior, scales='free') +
    labs(y='Proportion', x='Number of Data Points') +
    theme(legend.title=element_blank()) +
    stat_summary(fun.y=mean, 
                 geom='line',
                 size=1,
                 alpha=0.5) +
    theme_bw() +
    theme(legend.title=element_blank(), legend.position = 'top',
          legend.margin = margin(0,0,-.25,0,unit='cm'))
#ggsave('../Figures/EnglishLexiconDS_F1.svg', width=6, height=4)
