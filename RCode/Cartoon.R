library(tidyverse)
library(ggrepel)
library(xkcd)

reliable = data.frame(Order=rep(1:9, 3)) %>%
  mutate (Word=c('W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8', 'W9',
                 'W2', 'W1', 'W5', 'W3', 'W6', 'W4', 'W8', 'W9', 'W7',
                 'W3', 'W5', 'W2', 'W8', 'W4', 'W7', 'W9', 'W6', 'W1'),
          P=c(0.92, 0.94, 0.96, 0.93, 0.95, 0.90, 0.91, 0.89, 0.98,
              0.05, 0.01, 0.03, 0.01, 0.02, 0.07, 0.07, 0.04, 0.01,
              0.03, 0.05, 0.01, 0.06, 0.03, 0.03, 0.01, 0.07, 0.01),
          grop=c(rep(1,9),rep(2,9),rep(3,9)))

ggplot(reliable, aes(Order, P)) +
  geom_line(color='grey90', alpha=0.5, position = position_dodge(.05), aes(group=as.factor(grop))) +
  geom_point(aes(color=as.factor(grop), alpha=as.factor(grop))) +
  geom_text_repel(aes(label=Word, color=as.factor(grop), alpha=as.factor(grop))) +
  ylim(0,1) +
  scale_x_continuous(breaks=1:9) +
  scale_color_manual(values=c('blue','black','black')) +
  scale_alpha_manual(values=c(1,.2,.2)) +
  xlab('Order of Acquisition') +
  ylab('Probability of Acquisition') +
  ggtitle('Accurate Reliable') +
  guides(alpha=F, color=F) +
  theme_xkcd() +
  theme(plot.title = element_text(hjust = 0.5))
#ggsave('../Figures/Acc_Reliable.pdf', width = 6, height=4)

Nreliable = data.frame(Order=rep(1:9, 3)) %>%
  mutate (Word=c('W3', 'W5', 'W2', 'W8', 'W4', 'W7', 'W9', 'W6', 'W1',
                 'W2', 'W1', 'W5', 'W3', 'W6', 'W4', 'W8', 'W9', 'W7',
                 'W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8', 'W9'),
          P=c(0.92, 0.94, 0.96, 0.93, 0.95, 0.90, 0.91, 0.89, 0.98,
              0.05, 0.01, 0.03, 0.01, 0.02, 0.07, 0.07, 0.04, 0.01,
              0.03, 0.05, 0.01, 0.06, 0.03, 0.03, 0.01, 0.07, 0.01),
          grop=c(rep(1,9),rep(2,9),rep(3,9)))


ggplot(Nreliable, aes(Order, P)) +
  geom_line(color='grey90', alpha=0.5, position = position_dodge(.05), aes(group=as.factor(grop))) +
  geom_point(aes(color=as.factor(grop), alpha=as.factor(grop))) +
  geom_text_repel(aes(label=Word, color=as.factor(grop), alpha=as.factor(grop))) +
  ylim(0,1) +
  scale_x_continuous(breaks=1:9) +
  scale_color_manual(values=c('blue','black','black')) +
  scale_alpha_manual(values=c(1,.2,.2)) +
  xlab('Order of Acquisition') +
  ylab('Probability of Acquisition') +
  ggtitle('Inaccurate Reliable') +
  guides(alpha=F, color=F) +
  theme_xkcd() +
  theme(plot.title = element_text(hjust = 0.5))
#ggsave('../Figures/NAcc_Reliable.pdf', width = 6, height=4)


unreliable = data.frame(Order=rep(1:9, 3)) %>%
  mutate (Word=c('W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8', 'W9',
                 'W2', 'W1', 'W5', 'W3', 'W6', 'W4', 'W8', 'W9', 'W7',
                 'W3', 'W5', 'W2', 'W8', 'W4', 'W7', 'W9', 'W6', 'W1'),
          P=c(0.46, 0.35, 0.51, 0.40, 0.45, 0.50, 0.46, 0.51, 0.35,
              0.36, 0.33, 0.25, 0.30, 0.30, 0.25, 0.36, 0.25, 0.33,
              0.18, 0.32, 0.24, 0.30, 0.25, 0.25, 0.18, 0.24, 0.32),
          grop=c(rep(1,9),rep(2,9),rep(3,9)))

ggplot(unreliable, aes(Order, P)) +
  geom_line(color='grey90', alpha=0.5, position = position_dodge(.05), aes(group=as.factor(grop))) +
  geom_point(aes(color=as.factor(grop), alpha=as.factor(grop))) +
  geom_text_repel(aes(label=Word, color=as.factor(grop), alpha=as.factor(grop))) +
  ylim(0,1) +
  scale_x_continuous(breaks=1:9) +
  scale_color_manual(values=c('blue','black','black')) +
  scale_alpha_manual(values=c(1,.2,.2)) +
  xlab('Order of Acquisition') +
  ylab('Probability of Acquisition') +
  ggtitle('Accurate Unreliable') +
  guides(alpha=F, color=F) +
  theme_xkcd() +
  theme(plot.title = element_text(hjust = 0.5))
#ggsave('../Figures/Acc_NReliable.pdf', width = 6, height=4)

Nunreliable = data.frame(Order=rep(1:9, 3)) %>%
  mutate(Word=c('W3', 'W5', 'W2', 'W8', 'W4', 'W7', 'W9', 'W6', 'W1',
                 'W2', 'W1', 'W5', 'W3', 'W6', 'W4', 'W8', 'W9', 'W7',
                 'W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8', 'W9'),
          P=c(0.46, 0.35, 0.51, 0.40, 0.45, 0.50, 0.46, 0.51, 0.35,
              0.36, 0.33, 0.25, 0.30, 0.30, 0.25, 0.36, 0.25, 0.33,
              0.18, 0.32, 0.24, 0.30, 0.25, 0.25, 0.18, 0.24, 0.32),
          grop=c(rep(1,9),rep(2,9),rep(3,9)))

ggplot(Nunreliable, aes(Order, P)) +
  geom_line(color='grey90', alpha=0.5, position = position_dodge(.05), aes(group=as.factor(grop))) +
  geom_point(aes(color=as.factor(grop), alpha=as.factor(grop))) +
  geom_text_repel(aes(label=Word, color=as.factor(grop), alpha=as.factor(grop))) +
  ylim(0,1) +
  scale_x_continuous(breaks=1:9) +
  scale_color_manual(values=c('blue','black','black')) +
  scale_alpha_manual(values=c(1,.2,.2)) +
  xlab('Order of Acquisition') +
  ylab('Probability of Acquisition') +
  ggtitle('Inaccurate Unreliable') +
  guides(alpha=F, color=F) +
  theme_xkcd() +
  theme(plot.title = element_text(hjust = 0.5))
#ggsave('../Figures/NAcc_NReliable.pdf', width = 6, height=4)

