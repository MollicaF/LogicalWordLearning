# Reviewers requested to see the model behavior when we add a primitive for sibling.

source('utilities.R')

# Objects
obs = c('Amanda', 'Anne', 'aragorn', 'Arwen', 'Brandy', 'Celebrindal', 'Clarice', 'elrond', 'Eowyn', 'fabio', 'fred', 'frodo', 'Galadriel', 'gandalf', 'han', 'harry', 'Hermione', 'gary', 'james', 'joey', 'Katniss', 'legolas', 'Leia', 'Lily', 'luke', 'Luna', 'Mellissa', 'merry', 'Padme', 'peeta', 'Prue', 'ron', 'Rose', 'Sabrina', 'salem', 'sam', 'Zelda')

# Hypothesis Space
d = read.csv('../Spaces/Space/SiblingSpace2.csv', header=F, strip.white = T) %>% select(-V7)
colnames(d) = c('LexNo', 'Word', 'HPrior', 'LPrior', 'RPrior', 'Abstract', 'Recurse', 'Hypothesis', 'MODE', rep(obs,length(obs)-1), obs)
d = d[,c(1:8,10:(ncol(d)-1-length(obs)))]

# Ground Truth
ground = read.csv('../Spaces/Keys/GenericEnglish_Key.csv', header=F, strip.white = T)
colnames(ground) = c('I','Word', rep(obs,length(obs)-1))
row.names(ground) = ground$Word
ground = as.matrix(ground[3:ncol(ground)])

marginalBoots = NULL
for(i in 1:10){
    
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

tol14rainbow=c("#882E72", "#B178A6", "#D6C1DE", "#1965B0", "#5289C7", "#7BAFDE", "#4EB265", "#90C987", "#CAE0AB", "#F7EE55", "#F6C141", "#F1932D", "#E8601C", "#DC050C")

mins = marginalBoots %>%
    group_by(Word, Sim) %>%
    filter(Accuracy > 0.98) %>% # Changed this cuz cousin would need even more data (It's being blocked by some really infrequent data)
    summarise(amount=min(amount)) %>%
    ungroup() %>%
    group_by(Word) %>%
    summarise(mins=max(amount))

marginalBoots %>%
    left_join(mins) %>%
    filter(amount <= mins + 5) %>%
    ggplot(aes(x=amount, Accuracy, color=Word)) +
    labs(y='Proportion', x='Number of Data Points') +
    stat_summary(fun.ymin=function(x){quantile(x, .025)},
                 fun.ymax=function(x){quantile(x, .975)},
                 geom='ribbon',
                 aes(fill=Word),
                 alpha=0.15,
                 color=NA) +
    stat_summary(fun.y=mean, 
                 geom='line',
                 size=1,
                 alpha=0.6) +
    geom_text_repel(data=mins, aes(x=mins, y=1.05, label=Word)) +
    geom_point(data=mins, aes(x=mins, y=1), size=2) +
    theme_bw() +
    guides(color=F, fill=F) +
    scale_colour_manual(values=tol14rainbow) +
    scale_fill_manual(values=tol14rainbow) +
    theme(legend.title=element_blank()) 
#ggsave('../Figures/REV/WithSibling_Learn.svg', width=9, height=5.25)

marginalBoots %>%
    left_join(mins) %>%
    filter(amount <= mins + 5) %>%
    gather(variable, value, Accuracy:Recall) %>%
    ggplot(aes(x=amount, value, color=variable, linetype=variable)) +
    facet_wrap(~Word, scales='free_x') +
    labs(y='Proportion', x='Number of Data Points') +
    stat_summary(fun.ymin=function(x){quantile(x, .025)},
                 fun.ymax=function(x){quantile(x, .975)},
                 geom='ribbon',
                 aes(fill=variable),
                 alpha=0.25,
                 color=NA) +
    stat_summary(fun.y=mean, 
                 geom='line',
                 size=1,
                 alpha=0.8) +
    theme_bw() +
    theme(legend.title=element_blank()) 
#ggsave('../Figures/REV/WithSibling_F1.svg', width=6, height=4)

