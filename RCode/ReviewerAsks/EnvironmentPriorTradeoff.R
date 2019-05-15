# The reviewers wanted to see that both simplicity and ipfian environment are required to see the order of acquisition so here they are parameterically
# manipulated--i.e, uniform vs simplicty prior and CHILDES + tree vs zifpian environment
# The modified bootscript for uniform prior is not included. Just set the prior values to the same number.

source('utilities.R')
tol14rainbow=c("#882E72", "#B178A6", "#D6C1DE", "#1965B0", "#5289C7", "#7BAFDE", "#4EB265", "#90C987", "#CAE0AB", "#F7EE55", "#F6C141", "#F1932D", "#E8601C", "#DC050C")

#marginalBootsA = feather::read_feather('Feathers/BigBoots/UniformPriorSizePrinciple1000.feather')
#marginalBootsB = feather::read_feather('Feathers/BigBoots/ZipfFlatPrior.feather')
#marginalbootsC  = feather::read_feather('Feathers/BigBoots/englishZ0_E0Boots1000.feather')
marginalboots = feather::read_feather('Feathers/BigBoots/englishZ0_E1Boots1000.feather')

mins = marginalBoots %>%
    group_by(Word, Sim) %>%
    filter(Accuracy > 0.99) %>%
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
#ggsave('../Figures/REV/Learn_UP_SP.svg', width=9, height=5.25)
#ggsave('../Figures/REV/Learn_UP_Z.svg', width=9, height=5.25)
#ggsave('../Figures/REV/Learn_S_SP.svg', width=9, height=5.25)
ggsave('../Figures/REV/Learn_S_Z.svg', width=9, height=5.25)

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
#ggsave('../Figures/REV/F1_UP_SP.svg', width=6, height=4)
#ggsave('../Figures/REV/F1_UP_Z.svg', width=6, height=4)
#ggsave('../Figures/REV/F1_S_SP.svg', width=6, height=4)
ggsave('../Figures/REV/F1_S_Z.svg', width=6, height=4)


d = bind_rows(marginalboots %>%  mutate(Prior='Simplicity', Environment='Zipfian'),
              marginalbootsC %>% mutate(Prior='Simplicity', Environment='CHILDES & Tree'),
              marginalBootsB %>% mutate(Prior='Uniform', Environment='Zipfian'),
              marginalBootsA %>% mutate(Prior='Uniform', Environment='CHILDES & Tree'))

orders = d %>%
    group_by(Word, Sim, Environment, Prior) %>%
    filter(Accuracy + rnorm(length(Accuracy), 0.01, 0.005) >= 0.99) %>%
    summarise(amount=min(amount)) %>%
    ungroup() %>%
    arrange(amount) %>% 
    group_by(Sim, Environment, Prior) %>% 
    summarise(Order=paste(Word, collapse='.')) %>%
    mutate(First   = map_chr(Order, function(x) strsplit(x, '.', fixed=T)[[1]][1]),
           Second  = map_chr(Order, function(x) strsplit(x, '.', fixed=T)[[1]][2]),
           Third   = map_chr(Order, function(x) strsplit(x, '.', fixed=T)[[1]][3]),
           Fourth  = map_chr(Order, function(x) strsplit(x, '.', fixed=T)[[1]][4]),
           Fifth   = map_chr(Order, function(x) strsplit(x, '.', fixed=T)[[1]][5]),
           Sixth   = map_chr(Order, function(x) strsplit(x, '.', fixed=T)[[1]][6]),
           Seventh = map_chr(Order, function(x) strsplit(x, '.', fixed=T)[[1]][7]),
           Eighth  = map_chr(Order, function(x) strsplit(x, '.', fixed=T)[[1]][8]),
           Ninth   = map_chr(Order, function(x) strsplit(x, '.', fixed=T)[[1]][9]))

orders %>%
    ungroup() %>%
    mutate(Environment=ifelse(Environment=='CHILDES & Tree', 'Uniform', Environment)) %>%
    gather(Position, Word, First:Ninth) %>%
    group_by(Position, Word, Environment, Prior) %>%
    summarise(N=n()) %>%
    ungroup() %>%
    mutate(Word=fct_relevel(Word, 'cousin', 'uncle','aunt','grandpa','grandma', 'sister', 'brother', 'father', 'mother'),
           Position=fct_relevel(Position, 'First','Second','Third','Fourth','Fifth','Sixth','Seventh','Eighth','Ninth')) %>%
    filter(!is.na(Word)) %>%
    ggplot(aes(Position, Word, color=N)) +
    facet_grid(Prior~Environment) +
    geom_point(aes(size=N), shape=15) +
    scale_size_continuous(range = c(3,15)) + 
    scale_color_gradient(low = "white", high = "black") + 
    guides(size=F) +
    coord_equal() +
    theme_bw()

ggsave('../Figures/REV/OA.svg', width=12.75, height=12)

